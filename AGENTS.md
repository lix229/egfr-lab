# egfr-lab

Creatinine results from three clinic sites, as an EHR extract would give them. The data are synthetic: no real
patients.

## The job
It arrives as a message from Sam, who chairs the quality committee: the student types `/start`, and the lab-start
skill delivers it. In short: the committee decides tomorrow whether to fund a nurse-led follow-up for patients whose
kidney function is falling fast, and a draft, `reports/draft_report.md`, says 3.1% of our patients had a rapid decline.
Nobody has checked it. The committee will want the number and who, why we believe it, where the definition comes from,
and a way to rerun it every quarter. The corrected report goes in `reports/report.md`.

## The question, exactly
- A **rapid decline**: eGFR fell by more than 30% between two results no more than 365 days apart
  (the later result is less than 0.7 times the earlier one).
- Only patients with results on at least two different dates can be assessed; leave the others out of every count.
- eGFR: CKD-EPI 2021, no race term, age in years at the collection date. The egfr-qc skill has the formula.

## Data (read-only)
- `data/patients.csv`: patient_id, site, sex (F/M), birth_date
- `data/site_A.csv`, `site_B.csv`, `site_C.csv`: patient_id, collected, test, value, unit
- The results were collected between January 2023 and December 2025.
- Three sites, three lab systems: look at each file before you trust it. Load the **egfr-qc** skill first.

## How we work here
- Code goes in `egfr.py`; `tests/test_egfr.py` says what it must do. Run Python with uv: `uv run pytest`,
  `uv run python analyze.py`. Never edit `data/`, `tests/` or `checks/`.
- Results go in `results/`: `decliners.csv` (one column, patient_id) and `summary.json`
  (`{"assessable_patients": n, "rapid_decliners": n}`). Then run `uv run checks/check.py` and fix what it reports.
- For papers, use the pubmed tools. Cite PMIDs, and quote the sentence that supports each claim.
- Say what you checked and how. If something in the data surprises you, report it rather than guess.

## If they ask for help
The person at the keyboard is learning to direct an agent, and Sam's task is theirs to plan. If they ask for help with
how to go about it, or what to ask you, load the **lab-help** skill yourself (not in a subagent) and follow it, one
layer at a time: a nudge; then, if they ask, the next milestone from its `workflow.md`; then, if they ask what to type,
one prompt from its `prompts.md`. Give those as they are written there, not a plan or prompt of your own. Don't offer
hints they didn't ask for, and never use that skill or its files to plan or do the work yourself.
