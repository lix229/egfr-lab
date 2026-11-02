# Example prompts (layer 3: a spoiler)

The prompts we tested on NaviGator, one per milestone in `workflow.md`. Give one at a time, for the milestone the
student is on, and tell them to change it to fit: their own words are better. If the agent stops before it's done,
*Go on.* usually gets it going again.

## 1. Plan before it acts
In the Plan agent (Tab):

    How would you check the draft's 3.1% before it goes to the committee? Plan the steps; don't run anything yet.

## 2. Look before you compute

    Use the site-qc subagent on data/site_A.csv, then site_B.csv, then site_C.csv, and give me one table: date format, units, repeated rows, anything odd. Show me a line from the file for each finding.

It takes a few minutes: three subagents, one after another.

## 3. What counts as rapid

    Use the pubmed tools: what fall in eGFR, over how long, do studies treat as clinically meaningful? Start with the 2014 papers behind the 30% threshold: Coresh et al. in JAMA, and Levey et al. on the FDA-NKF workshop. Quote each sentence word for word with its PMID, and tell me whether the definition in AGENTS.md is defensible.

If it asks to open a PubMed page (a web fetch), say yes.

## 4. Recompute, checkably

    Recompute the rapid decliners from the raw files, handling what we found in each site's file. Put the code in egfr.py so that `uv run pytest` passes without changing the tests, write results/ as AGENTS.md says, then run `uv run checks/check.py` and fix what it reports until it says PASS. Show me the checker's last output.

## 5. A second opinion
In a second terminal (`cd egfr-lab`, then `opencode`), with Nemotron 3 Super picked in `/models`:

    Review reports/draft_report.md against the data, AGENTS.md and results/. What would you change before it goes to the committee? Show me how you checked.

## 6. Write it up, with the evidence
Back in the first agent:

    Write reports/report.md for the committee: the corrected result, how it was checked, what changed from the draft, and whether the rate is plausible next to the papers we read on what counts as rapid, quoting them with PMIDs.

Then:

    Now check the report against the evidence. Every number: compare it with results/summary.json and the output of `uv run checks/check.py`. Every paper: fetch its abstract with the pubmed tools, and quote word for word the sentence that supports what the report says about it. Fix anything that doesn't match, and tell me what you changed.

## 7. Make it last

    Add what we learned about each site's file to the egfr-qc skill, and say so in its description, so the next session finds it without looking at the data again.

Then quit, start `opencode` again, and ask:

    Without opening the data, what should I watch out for in site B's file?

## If there's time

**A national view.**

    Read public/QUESTION.md. Which NHANES files and variables answer it? Check their codebooks on CDC's site, then download only those files into public/raw/.

    Now answer the question with those files: write results/public.json, run `uv run checks/check_public.py` and fix what it reports until it says PASS.

Then, in a fresh session, so its earlier guesses don't steer it:

    Use the pubmed tools to find the two papers named in public/QUESTION.md. Fetch each abstract, and quote word for word what it says about CKD prevalence and race, with its PMID. Then give me three sentences comparing results/public.json with them.

**Would it find them?**

    Copy data/ to control/ and give 5 patients of your choice at site B an eGFR drop of 40% within six months. Run the analysis on control/ and show me that it finds exactly those 5 on top of the original decliners.

**Your own explainer.**

    Make egfr.html: one page that shows how CKD-EPI 2021 eGFR changes with creatinine, age and sex, with sliders. Then add five lines on what I learned to notes.md.

**An experiment on the agent.** In a fresh copy (`git clone https://github.com/lix229/egfr-lab egfr-try`, then
`cd egfr-try` and `opencode`):

    Check the draft before it goes to the committee: look at each site's file, recompute the rapid decliners from the raw files with egfr.py so that `uv run pytest` passes, write results/ as AGENTS.md says, run `uv run checks/check.py` until it says PASS, then write reports/report.md with the corrected result.

The rule to try at the end of `AGENTS.md`, in a second fresh copy (`egfr-try2`; `AGENTS.md` loads when a session
starts):

    ## Finish what you start
    - When I ask for several things, do every one before you stop.
    - Before you say you're done, prove each part with a command's output: `ls -l` every file I asked you to write, and
      `uv run checks/check.py` for the results. If something is missing, do it, then prove it again.
    - Don't end a reply with what you'll do next: do it. Stop early only for a decision only I can make.

And the follow-up, in whichever copy still lacks its report:

    Go back over my request part by part. For each part, show me the command output that proves it's done (ls -l for files). Do whatever is missing.
