# The workflow we used (layer 2: a spoiler)

One way through Sam's task, in seven milestones. Each uses one idea from the lecture. Give the student the next
milestone only, unless they ask for all of it: what to aim for, how they'll know it's done, and, if it helps, the
pitfall.

## 1. Plan before it acts (plan mode)
- **Aim:** a plan for checking the draft's 3.1%, read and corrected before anything runs. In OpenCode, Tab switches to
  the Plan agent, which can read but not change anything; Tab again switches back to Build.
- **Done when:** they've read its plan and told it what they'd change.
- **Worth noticing:** it already knew the job and the rules before they typed: OpenCode loaded `AGENTS.md`, the memory
  file. In our test, its first plan assumed `egfr.py` existed and that every site used the same units: both worth
  correcting.

## 2. Look before you compute (subagents)
- **Aim:** what each site's file does differently (dates, units, repeated rows), with a line from the file for each
  finding. The `site-qc` subagent checks one site's file, read-only, in a fresh context, and sends back a short report.
- **Done when:** they can say what each site does differently, and they've checked one finding themselves (for example
  `grep -c umol data/site_C.csv`).
- **Pitfall:** subagents make mistakes too. In our test one invented an example line and called 2024 dates
  "future-dated" (the model's own sense of today); the data run from 2023 to 2025.

## 3. What counts as rapid (MCP)
- **Aim:** where "more than 30% within a year" comes from. The pubmed tools (an MCP server, `tools/pubmed.py`) search
  PubMed and read abstracts. Good starting points: Coresh et al. (JAMA 2014) and Levey et al. (the FDA–NKF workshop,
  2014), the papers behind the 30% threshold. Quote each sentence word for word with its PMID.
- **Done when:** they've opened at least one cited paper themselves (pubmed.ncbi.nlm.nih.gov/ and the PMID) and it
  says what the agent claims.
- **Pitfall:** real papers, wrong claims about them. Asked an open question, it once cited two real papers it never
  opened, and both define a rapid decline differently from what it said. Its opinion is input; the definition is the
  committee's call.

## 4. Recompute, checkably (tests and a check)
- **Aim:** the rapid decliners recomputed from the raw files, handling what milestone 2 found: code in `egfr.py` that
  passes `uv run pytest` without changing the tests, results in `results/` as `AGENTS.md` says, and the data team's
  checker, `uv run checks/check.py`, saying PASS.
- **Done when:** they've seen the checker's own output say PASS.
- **Pitfall:** once, in our test, it said the checker passed without running it, and gave numbers that weren't in
  `results/`. If in doubt, run `uv run checks/check.py` themselves. Watch the loop: run the tests, read what failed,
  fix, run again. If the checker says NOT YET, its hint says where to look. It asks before writing a file: *once*, or
  *always* for the rest of the session.

## 5. A second opinion (another model)
- **Aim:** a different model, with different blind spots, reviews the draft against the data, `AGENTS.md` and
  `results/`, and shows how it checked. A second agent beside the first: in herdr, ctrl+b then v, `opencode` in this
  folder, `/models`, **Nemotron 3 Super**.
- **Done when:** it has found what's wrong with the draft, and they've confirmed it against the files.

## 6. Write it up, with the evidence
- **Aim:** `reports/report.md` for the committee (the corrected result, how it was checked, what changed from the
  draft, and whether the rate is plausible next to the papers), then a check of the report itself: every number
  against `results/summary.json` and the checker's output, every paper re-fetched and quoted.
- **Done when:** the report gives the result the checker passed, every number traces to `results/` or a paper, and
  each paper says what the report claims.
- **Pitfall:** asked for papers at the end of a long session, it once quoted its own numbers as if published, under
  invented PMIDs.

## 7. Make it last (a skill)
- **Aim:** what they learned about each site's file, added to the `egfr-qc` skill (and said so in its description), so
  next quarter's session finds it without looking at the data again. Read what it adds: a wrong note in a skill
  misleads every session after it.
- **Done when:** a fresh session (quit, start `opencode` again), asked what to watch out for in site B's file without
  opening the data, answers from the skill.

## If there's time
- **A national view (the web, with their OK).** `public/QUESTION.md`: which NHANES files and variables, checked
  against CDC's codebooks; download only those into `public/raw/`; answer in `results/public.json` until
  `uv run checks/check_public.py` says PASS; then, in a fresh session, the two named papers, quoted with PMIDs. Done
  when the checker passes, each PMID opens to the paper it names, and they can say what changed and for whom.
- **Would it find them? (a positive control).** Copy `data/` to `control/`, plant a few rapid decliners at one site,
  run the analysis on the copy, and check it finds exactly those on top of the original ones.
- **Your own explainer.** One page, `egfr.html`, with sliders for creatinine, age and sex; then a few lines on what
  they learned in `notes.md`. Done when a 50-year-old woman with creatinine 1.0 mg/dL reads about 69.
- **An experiment on the agent.** In a fresh copy (`git clone https://github.com/lix229/egfr-lab egfr-try`), the whole
  job in one message; then `ls reports/`: is the report it describes there? Then a rule in `AGENTS.md` in a second
  fresh copy, and the same request. Then, in whichever copy still lacks the report, a follow-up asking for proof of
  each part. In our tests the one big request skipped the report in 8 of 9 runs, usually saying it had written it; the
  rule fixed it in 1 of 6; the follow-up fixed it both times. A memory file is good for facts the agent can't know (the
  date range in `AGENTS.md` ended its "future dates" mistake); a rule about how to work is a request it may skip.
  Asking for one thing at a time, and for the proof, is what worked.
