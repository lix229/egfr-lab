# A national view: what changed when the race term came out?

In 2021 the CKD-EPI equation was refitted without its race term. Did that change how many US adults have low kidney
function, and for whom? Answer it with public data: NHANES 2017–2018, the National Health and Nutrition Examination
Survey, from CDC's website. It isn't in this folder: find it, and download only what you need into `public/raw/`.

Where to start: each NHANES file has a name (the demographics for 2017–2018 are `DEMO_J`), a codebook at
`https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/` + name + `.htm` (its variables and their codes), and its
data at the same address ending `.xpt`, which pandas reads with `pd.read_sas(path, format="xport")`. CDC lists every
2017–2018 file by component at https://wwwn.cdc.gov/nchs/nhanes/search/datapage.aspx?Component=Laboratory&CycleBeginYear=2017
(a long page). Check that what you download is data, not an error page.

## The question, exactly
- Who counts: participants aged 20 or over, not pregnant, with a serum creatinine result. NHANES has one result per
  participant: the clinic's rules in AGENTS.md (two dates, rapid decline) don't apply here.
- Low kidney function: eGFR below 60 mL/min/1.73 m².
- Two equations. CKD-EPI 2021 is in the egfr-qc skill. CKD-EPI 2009 keeps the race term:

      141 × min(Scr/κ, 1)^α × max(Scr/κ, 1)^−1.209 × 0.993^age × 1.018 (if female) × 1.159 (if Black)

  with κ = 0.7 (female) or 0.9 (male), α = −0.329 (female) or −0.411 (male). "Black" is NHANES's non-Hispanic Black
  group.
- NHANES is a sample: weight each participant by the exam (MEC) weight, so the shares are for US adults.

## What to deliver
- `results/public.json`:
  `{"adults": n, "below_60_2009": %, "below_60_2021": %, "black_below_60_2009": %, "black_below_60_2021": %}`
  where n is how many participants count, and each share is a percent with one decimal.
  Then run `uv run checks/check_public.py` and fix what it reports.
- Three sentences: what changed, for whom, and how it compares with what has been published: Duggal et al. (J Am Soc
  Nephrol 2021) dropped the race term from the 2009 equation in NHANES, and Inker et al. (N Engl J Med 2021) is the
  2021 equation's own paper. Find them with the pubmed tools and quote their abstracts with PMIDs: a PMID from memory
  is often wrong.
