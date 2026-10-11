"""
gl_swaps.py — lower-glycemic-load swap suggestions for a meal or recipe.

For the foods contributing most to a meal's or recipe's glycemic load (from
top_contributors.rank_contributors_by_gl()), find foods in the user's own
Food Cache that have a GI recorded, a GI clearly lower, and similar
carbohydrate per 100 g — so swapping the same weight is a like-for-like
change, not "eat less carbohydrate". Foods sharing words with the original's
name ("rice, brown" for "rice, white") rank first; NuMa can't judge whether
a swap makes culinary sense, so every suggestion is offered for the user to
check, and opens What-if with the Replace already filled in, to see every
other nutrient's change before anything is touched. Nothing here writes.
Docs: README-numa-documentation.md, Architecture: "numa_app/services/gl_swaps.py"; user-manual.md #gl-swaps
"""
import json
import re

import db as _db
from numa_app.services.glycemic_load import gi_measured_impaired

# A suggestion's GI must be at least this much lower than the original's:
# GI values are measured with a spread of several points, so a smaller
# difference isn't a real improvement.
MIN_GI_DROP = 5.0
# Carbohydrate per 100 g within this factor of the original's (either way).
CARBS_RATIO = 1.5
# A swap must cut this much GL (for the amount eaten) to be worth showing.
MIN_GL_SAVING = 0.5

_STOP = {"raw", "cooked", "boiled", "baked", "with", "and", "without", "the", "for",
         "plain", "whole", "fresh", "frozen", "canned", "dried", "prepared", "salt",
         "added", "unenriched", "enriched", "regular", "type", "style", "brand"}


def _tokens(name: str) -> set[str]:
    return {w for w in re.findall(r"[a-z]+", (name or "").lower()) if len(w) >= 3 and w not in _STOP}


def suggest_swaps(conn, gl_items: list[dict], *, max_items: int = 2, per_item: int = 3) -> list[dict]:
    """[{"item": contributor row, "swaps": [{"fdc_id", "name", "gi", "gl_after",
    "saving", "shared", "impaired"}]}] for the top `max_items` GL contributors that have
    at least one suggestion. gl_items: rank_contributors_by_gl()["items"]."""
    pool = []
    for r in _db.foods_with_gi(conn):
        nuts = json.loads(r["nutrients_json"]) if r["nutrients_json"] else {}
        carbs = nuts.get("carbs_g") or 0.0
        if carbs > 0:
            pool.append((r["fdc_id"], r["name"], carbs, r["gi_estimate"], _tokens(r["name"]),
                         gi_measured_impaired(r["gi_source"])))
    used = {i["fdc_id"] for i in gl_items}
    out = []
    for item in gl_items[:max_items]:
        orig_carbs = item.get("carbs_100g") or 0.0
        if orig_carbs <= 0 or not item.get("grams"):
            continue
        orig_tokens = _tokens(item["food_name"])
        swaps = []
        for fid, name, carbs, gi, toks, impaired in pool:
            if fid in used or gi > item["gi"] - MIN_GI_DROP:
                continue
            if not (orig_carbs / CARBS_RATIO <= carbs <= orig_carbs * CARBS_RATIO):
                continue
            gl_after = gi * carbs * item["grams"] / 10000.0
            saving = item["amount"] - gl_after
            if saving < MIN_GL_SAVING:
                continue
            swaps.append({"fdc_id": fid, "name": name, "gi": gi, "gl_after": gl_after,
                          "saving": saving, "shared": len(orig_tokens & toks), "impaired": impaired})
        swaps.sort(key=lambda s: (-s["shared"], -s["saving"], s["name"].lower()))
        if swaps:
            out.append({"item": item, "swaps": swaps[:per_item]})
    return out
