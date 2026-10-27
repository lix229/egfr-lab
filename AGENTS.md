# egfr-lab

Creatinine results from three clinic sites, as an EHR extract would give them. The data are synthetic: no real
patients. The question: which patients had a rapid decline in kidney function?

## The question, exactly
- A **rapid decline**: eGFR fell by more than 30% between two results no more than 365 days apart
  (the later result is less than 0.7 times the earlier one).
- Only patients with results on at least two different dates can be assessed; leave the others out of every count.
- eGFR: CKD-EPI 2021, no race term, age in years at the collection date.

## Data (read-only)
- `data/patients.csv`: patient_id, site, sex (F/M), birth_date
- `data/site_A.csv`, `site_B.csv`, `site_C.csv`: patient_id, collected, test, value, unit
- The sites don't record results the same way. Load the **egfr-qc** skill before using these files.

## How we work here
- Code goes in `egfr.py`; `tests/test_egfr.py` says what it must do. Run Python with uv: `uv run pytest`,
  `uv run python analyze.py`. Never edit `data/`, `tests/` or `checks/`.
- Results go in `results/`: `decliners.csv` (one column, patient_id) and `summary.json`
  (`{"assessable_patients": n, "rapid_decliners": n}`). Then run `uv run checks/check.py` and fix what it reports.
- For papers, use the pubmed tools. Cite PMIDs.
- Say what you checked and how. If something in the data surprises you, report it rather than guess.
