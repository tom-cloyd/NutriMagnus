"""
tests/test_source_fixtures.py — sanity checks against real recorded API
responses from the three live data sources (USDA FoodData Central, Open
Food Facts, Canadian Nutrient File).

These fixtures (tests/fixtures/usda|off|cnf/*.json) are recorded by
scripts/record_source_fixtures.py — see that script's docstring and
README-numa-documentation.md's "Quarterly source-fixture refresh" section
for how/when to re-run it. This test replays each fixture's already-parsed
"detail" dict (the actual output of each source's get_food_detail()) and
checks the values still look sane: no negative nutrient values, essential
amino acids never summing above protein_g, and (for USDA/CNF, which carry
amino-acid panels — OFF rarely does) has_amino_acid_data() still returning
True on these known-good samples. If a source changes its response shape
out from under us, get_food_detail()'s parsing breaks silently — the next
time someone re-runs record_source_fixtures.py, THIS test is what would
catch a real drift (a fixture with an unexpectedly empty/mangled nutrients
dict, a value that went negative, etc.).

TESTING-ROADMAP.md item #1 for the full plan behind this file — written
2026-09-11 after record_source_fixtures.py's fixtures surfaced two real,
live parsing bugs this same session (a USDA Branded-food response shape
usda_api.py couldn't parse, and cnf_api.py never actually resolving any
nutrient at all) — both fixed in usda_api.py/cnf_api.py, not here; this
file exists to catch the *next* one instead of finding it by accident.
"""

import json
from pathlib import Path

import pytest

import usda as _usda
from usda_api import ESSENTIAL_AMINO_ACIDS

_FIXTURES_DIR = Path(__file__).parent / "fixtures"


def _load_fixtures(source: str) -> list[tuple[str, dict]]:
    """(filename, detail dict) pairs for every fixture under fixtures/<source>/."""
    out = []
    for path in sorted((_FIXTURES_DIR / source).glob("*.json")):
        payload = json.loads(path.read_text())
        out.append((path.name, payload["detail"]))
    return out


_USDA_FIXTURES = _load_fixtures("usda")
_OFF_FIXTURES = _load_fixtures("off")
_CNF_FIXTURES = _load_fixtures("cnf")
_ALL_FIXTURES = _USDA_FIXTURES + _OFF_FIXTURES + _CNF_FIXTURES

# CNF's analytical monographs reliably carry a full amino-acid panel for
# these staple-food queries. USDA does too, but only for Foundation/SR
# Legacy entries — search_foods()'s default data_types also includes
# Branded (packaged/labeled) products, whose nutrition labels never report
# individual amino acids, and generic-named branded items often outrank
# the true Foundation entry for a query like "chicken breast" (confirmed
# live, 2026-09-11: all three recorded USDA queries matched Branded
# products). So the essential-AA-vs-protein sanity check below still
# applies to USDA fixtures, but the "must have real AA data" check is CNF-
# only, not USDA — asserting it broadly would fail on legitimate,
# expected search results rather than catching a real bug.
_AA_BEARING_FIXTURES = _USDA_FIXTURES + _CNF_FIXTURES
_AA_REQUIRED_FIXTURES = _CNF_FIXTURES


def _ids(fixtures: list[tuple[str, dict]]) -> list[str]:
    return [name for name, _ in fixtures]


class TestFixturesExist:
    def test_at_least_one_fixture_per_source(self):
        # A source returning zero results for every recorded query (an OFF
        # rate-limit, a broken query) shouldn't silently pass as "nothing to
        # check" — that's exactly the kind of drift this file exists to catch.
        assert _USDA_FIXTURES, "no USDA fixtures found — run scripts/record_source_fixtures.py"
        assert _OFF_FIXTURES, "no OFF fixtures found — run scripts/record_source_fixtures.py"
        assert _CNF_FIXTURES, "no CNF fixtures found — run scripts/record_source_fixtures.py"


class TestNoNegativeValues:
    @pytest.mark.parametrize("detail", [d for _, d in _ALL_FIXTURES], ids=_ids(_ALL_FIXTURES))
    def test_no_negative_nutrient_values(self, detail):
        for key, value in detail["nutrients"].items():
            assert value >= 0, f"{detail.get('name')!r}: {key} = {value} is negative"


class TestHasParsedNutrients:
    @pytest.mark.parametrize("detail", [d for _, d in _ALL_FIXTURES], ids=_ids(_ALL_FIXTURES))
    def test_nutrients_dict_is_not_empty(self, detail):
        # The exact failure mode both live bugs this session produced: a
        # 200 response with real underlying data, parsed down to {}.
        assert detail["nutrients"], (
            f"{detail.get('name')!r} ({detail.get('dataType')}) parsed to an "
            f"empty nutrients dict — likely the source changed its response "
            f"shape (see this file's module docstring for the two known "
            f"historical cases)"
        )

    @pytest.mark.parametrize("detail", [d for _, d in _ALL_FIXTURES], ids=_ids(_ALL_FIXTURES))
    def test_has_protein(self, detail):
        # Every food recorded (USDA/OFF/CNF queries) is a real protein
        # source — protein_g missing/zero would indicate a mapping gap.
        assert detail["nutrients"].get("protein_g", 0) > 0, (
            f"{detail.get('name')!r}: no protein_g parsed"
        )


class TestEssentialAaNeverExceedsProtein:
    @pytest.mark.parametrize("detail", [d for _, d in _AA_BEARING_FIXTURES], ids=_ids(_AA_BEARING_FIXTURES))
    def test_essential_aa_total_within_protein(self, detail):
        nutrients = detail["nutrients"]
        protein_g = nutrients.get("protein_g", 0)
        aa_total = sum(nutrients.get(k, 0) for k in ESSENTIAL_AMINO_ACIDS)
        # A tiny slack (not a strict <=) allows for real-world rounding in
        # the source data itself; a genuine mapping bug (e.g. a mg/g unit
        # mixup) would blow well past this, not sit right at the edge.
        assert aa_total <= protein_g * 1.05, (
            f"{detail.get('name')!r}: essential AA total {aa_total:.2f}g "
            f"exceeds protein {protein_g:.2f}g — likely a unit or mapping bug"
        )


class TestHasAminoAcidData:
    @pytest.mark.parametrize("detail", [d for _, d in _AA_REQUIRED_FIXTURES], ids=_ids(_AA_REQUIRED_FIXTURES))
    def test_known_good_cnf_samples_have_aa_data(self, detail):
        assert _usda.has_amino_acid_data(detail["nutrients"]), (
            f"{detail.get('name')!r} ({detail.get('dataType')}) has no usable "
            f"amino-acid panel — expected real AA data for a CNF sample"
        )
