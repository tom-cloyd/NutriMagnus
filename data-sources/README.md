# Bundled reference-data source documents

Primary source documents for reference data compiled into NuMa. These are the
*inputs* to the build scripts, kept here so `gi_data.json` and its kin can be
regenerated years from now without re-hunting the originals — several of the
publisher pages that host them are bot-gated and cannot be fetched
programmatically.

Nothing here is read at runtime, and none of it is bundled into a packaged
build. These files exist for the developer and for provenance only.

---

## Glycemic index — Atkinson et al. 2021 (current source)

### Citation

> Atkinson, F. S., Brand-Miller, J. C., Foster-Powell, K., Buyken, A. E., &
> Goletzke, J. (2021). International tables of glycemic index and glycemic load
> values 2021: A systematic review. *The American Journal of Clinical
> Nutrition, 114*(5), 1625–1632. https://doi.org/10.1093/ajcn/nqab233

Publisher page (AJCN moved from Oxford University Press to Elsevier in 2022, so
the DOI now resolves to ScienceDirect):
<https://www.sciencedirect.com/science/article/pii/S0002916522004944>
PubMed record: <https://pubmed.ncbi.nlm.nih.gov/34258626/> (PMID 34258626)

### Files

| File | What it is |
|---|---|
| `atkinson-2021-supplemental-table-1-iso-consistent.pdf` | Supplemental Table 1 — values from studies whose method was consistent with ISO 26642:2010. Food numbers 1–2091. 139 pages. |
| `atkinson-2021-supplemental-table-2-method-deviations.pdf` | Supplemental Table 2 — values from studies that deviated from that standard, or whose results showed wide variability. Food numbers 2092–4018. 136 pages. |

Both are the article's own online supplemental material, reached from the
"Supplementary data" link on the publisher's article page. The copies here were
retrieved 2026-09-27 from a third-party mirror
(`nutritotal.com.br/pro/wp-content/uploads/2021/09/Tabela{1,2}_IG.pdf`) because
the publisher's page is bot-gated; they carry the correct citation header and
the expected food-number ranges, but **if you are re-verifying provenance, fetch
them again from the publisher's own Supplementary data link.**

### Ingested by

`scripts/build_gi_data.py` → `gi_data.json`. Run it with both PDFs as arguments,
in table order:

```bash
python3 scripts/build_gi_data.py \
    data-sources/atkinson-2021-supplemental-table-1-iso-consistent.pdf \
    data-sources/atkinson-2021-supplemental-table-2-method-deviations.pdf
```

Expect 4,017 entries from 4,018 printed food numbers, plus whatever 2008-edition
rows the merge carries forward from the existing `gi_data.json`. See that
script's docstring for the parsing approach and the source quirks it works
around, and the "GI reference table lookup" passage in
`README-numa-documentation.md` for the data model.

### Licensing — UNRESOLVED

The PDFs themselves contain **no copyright or licence text**. The 2008 edition
(below) was explicitly Creative Commons licensed, and that was the stated basis
for embedding it in NuMa; **that basis does not automatically extend to the 2021
edition.** PubMed marks the article "Free article", which means free to read at
the publisher — not a grant of redistribution rights. Confirm the 2021 article's
actual licence terms on the publisher's page before any public release that
ships `gi_data.json` built from it.

---

## Glycemic index — earlier editions, for the record

### 2008 — the edition NuMa shipped previously

> Foster-Powell, K., Holt, S. H. A., & Brand-Miller, J. C. (2008).
> International table of glycemic index and glycemic load values: 2008.
> *Diabetes Care, 31*(12), 2281–2283.

A Creative Commons licensed table, published as two online-only appendix tables
(A1, normal glucose tolerance; A2, impaired glucose tolerance, small subject
numbers, or wide variability) — split by **subject population**, unlike 2021,
which splits by method compliance. Its PDFs are **not** kept here; the few
hundred of its foods that 2021 does not appear to cover survive inside
`gi_data.json` tagged `edition: 2008`, and the ingest script
`scripts/build_gi_data_2008.py` is retained in case those appendices ever need
re-parsing from source.

### 2002 — evaluated and rejected

> Foster-Powell, K., Holt, S. H. A., & Brand-Miller, J. C. (2002).
> International table of glycemic index and glycemic load values: 2002.
> *The American Journal of Clinical Nutrition, 76*(1), 5–56.
> https://doi.org/10.1093/ajcn/76.1.5

Not used. The 2008 edition above is its direct revision and absorbed it, so
adding it would mainly contribute duplicate food names carrying *older* values
for the same studies — worse than omitting it, since the Annotate lookup shows
every plausible match for the user to choose between.

---

## Other bundled reference datasets

These are compiled from sources not stored here, each by its own script. If you
ever need their inputs archived the same way, this is the place.

| Dataset | Built by | Source |
|---|---|---|
| `cofid_data.json` | `scripts/build_cofid_data.py` | UK Composition of Foods Integrated Dataset (CoFID) |
| `afcd_data.json` | `scripts/build_afcd_data.py` | Australian Food Composition Database (AFCD) |
| `ciqual_data.json` | `scripts/build_ciqual_data.py` | French CIQUAL food composition table |
| `oxalate.db` | `build_oxalate_db.py` | Harvard T.H. Chan School of Public Health oxalate table |
