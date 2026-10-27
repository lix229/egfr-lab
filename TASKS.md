# Tasks

Do them in order; each takes a few minutes. Each one says what done looks like, so you can check it yourself,
and which idea from the lecture it shows. Paste the prompts as they are.

## 1. What does it already know? (a memory file)

Start `opencode` in this folder and ask:

```
What is this project, and what rules do I need to follow?
```

**Done when** its answer matches AGENTS.md. Open the file and compare: OpenCode loads it at every start.

## 2. Build a tool against its tests (say what done looks like)

```
Write egfr.py, then run `uv run pytest` and fix it until all the tests pass. Don't change the tests.
```

**Done when** `uv run pytest` reports 8 passed. Watch the loop: it writes, runs the tests, reads the failures, fixes.
It asks before it writes a file: answer *once*, or *always* for the rest of the session.

## 3. Answer the question, checkably (a skill, and a check)

```
Find the rapid decliners across all three sites, using egfr.py. Write results/ as AGENTS.md says, then run `uv run checks/check.py` and fix what it reports until it says PASS.
```

**Done when** the checker says PASS. Each site hides a trap; the egfr-qc skill (it should load it first) describes
them. If the checker says NOT YET, its hint names the site to look at.

## 4. A subagent checks one site (subagents)

```
Use the site-qc subagent to check data/site_C.csv, and tell me what it found.
```

**Done when** it reports that site C mixes mg/dL and umol/L, with counts (2,418 and 1,237 rows). The subagent starts
with a fresh context, can only read, and sends back a short report; your main session only sees that report.
In our test it also reported one "malformed" row whose unit was the word *unit*: that's the CSV's header line. Check
its work.

Then try all three at once: *Use the site-qc subagent once for each site file, then give me one table.* Site A sends
results twice; site B writes dates day-first. Check its counts against the files: subagents make mistakes too.

## 5. Look it up (MCP)

```
Use the pubmed tools to find the 2014 JAMA study that linked a 30% decline in eGFR over two years to later kidney failure. Give its PMID and one sentence from its abstract.
```

**Done when** it gives PMID 24892770 (Coresh et al., JAMA 2014): check at https://pubmed.ncbi.nlm.nih.gov/24892770/.
The pubmed tools come from `tools/pubmed.py`, a 70-line MCP server you can read.

## 6. A second opinion from another model

Open a second agent beside the first (in herdr: ctrl+b, then v; then `opencode` in this folder). Type `/models`,
pick **Nemotron 3 Super**, and ask:

```
Review reports/draft_report.md against the data and AGENTS.md. Is the decline rate right? Show me how you checked.
```

**Done when** it finds that the 52 patients with a single result are still in the denominator: 37 of 1,152 (3.2%),
not 37 of 1,204 (3.1%). A different model, with different blind spots, checking work it didn't write.

## 7. Have it teach you, then keep notes

```
Make egfr.html: one page that shows how CKD-EPI 2021 eGFR changes with creatinine, age and sex, with sliders. Then add five lines on what I learned to notes.md.
```

**Done when** egfr.html opens in your browser, the sliders move, and a 50-year-old woman with creatinine 1.0 mg/dL
reads about 69.

## Extra: plant the answer (a positive control)

```
Copy data/ to control/ and give 5 patients of your choice at site B an eGFR drop of 40% within six months. Run the analysis on control/ and show me that it finds exactly those 5 on top of the original decliners.
```

**Done when** it finds the 5 you planted and still finds the original ones. That is how you test code you couldn't
have written yourself.
