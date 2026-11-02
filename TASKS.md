# Tasks

One problem, start to finish. A colleague's draft, `reports/draft_report.md`, says 3.1% of the patients at our three
clinics had a rapid decline in kidney function. It goes to the quality committee tomorrow. Is it right? Fix it if not,
and back every number with evidence.

You direct; the agent does the legwork. Each step says what to ask (paste ours, or use your own words), what done
looks like, and which idea from the lecture it uses. Check its work as you go: it can be confidently wrong. And if it
stops before it's done, as gpt-oss sometimes does, type *Go on.* (Extra 2 is about why, and what helps.)

## 1. Plan before it acts (plan mode)

Start `opencode` in this folder and press **Tab**: the Plan agent can read, but it can't change anything.

```
How would you check the draft's 3.1% before it goes to the committee? Plan the steps; don't run anything yet.
```

**Done when** you've read its plan and told it what you'd change. Notice it already knows the question and the rules:
OpenCode loaded AGENTS.md, the memory file, before you typed. Press **Tab** again to switch back to Build.

## 2. Look before you compute (a subagent)

```
Use the site-qc subagent on data/site_A.csv, then site_B.csv, then site_C.csv, and give me one table: date format, units, repeated rows, anything odd. Show me a line from the file for each finding.
```

It takes a few minutes: three subagents, one after another. **Done when** you can say what each site does
differently, and you've checked one finding yourself (for example, `grep -c umol data/site_C.csv`). Each subagent
starts with a fresh context, can only read, and sends back a short report; your session sees only the reports.
Subagents make mistakes too.

## 3. What counts as rapid? (MCP)

```
Use the pubmed tools: what fall in eGFR, over how long, do studies treat as clinically meaningful? Start with the 2014 papers behind the 30% threshold: Coresh et al. in JAMA, and Levey et al. on the FDA-NKF workshop. Quote each sentence word for word with its PMID, and tell me whether the definition in AGENTS.md is defensible.
```

**Done when** you've opened at least one paper it cites (https://pubmed.ncbi.nlm.nih.gov/ and the PMID) and checked
that the paper defines a decline the way it says: real papers, wrong claims about them, is a common slip. If it asks
to open a PubMed page (a web fetch), say yes. The pubmed tools come from `tools/pubmed.py`, a 70-line MCP server you
can read. Its opinion is input; the definition is your call.

## 4. Recompute it, checkably (tests and a check)

```
Recompute the rapid decliners from the raw files, handling what step 2 found. Put the code in egfr.py so that `uv run pytest` passes without changing the tests, write results/ as AGENTS.md says, then run `uv run checks/check.py` and fix what it reports until it says PASS. Show me the checker's last output.
```

**Done when** you've seen the checker's own output say PASS: in our test, once, it said the checker passed without
running it, and gave numbers that weren't in results/. If in doubt, run `uv run checks/check.py` yourself. It asks
before it writes a file: answer *once*, or *always* for the rest of the session. Watch the loop: it runs the tests,
reads what failed, fixes, runs them again. If the checker says NOT YET, its hint says where to look.

## 5. A second opinion (another model)

Open a second agent beside the first (in herdr: ctrl+b, then v; then `opencode` in this folder). Type `/models`, pick
**Nemotron 3 Super**, and ask:

```
Review reports/draft_report.md against the data, AGENTS.md and results/. What would you change before it goes to the committee? Show me how you checked.
```

**Done when** it has found what's wrong with the draft, and you've checked that against the files yourself. A
different model, with different blind spots, checking work it didn't write.

## 6. Write it up, with the evidence

Back in the first agent:

```
Write reports/report.md for the committee: the corrected result, how it was checked, what changed from the draft, and whether the rate is plausible next to the papers from step 3, quoting them with PMIDs.
```

Then have it check the report against the evidence:

```
Now check the report against the evidence. Every number: compare it with results/summary.json and the output of `uv run checks/check.py`. Every paper: fetch its abstract with the pubmed tools, and quote word for word the sentence that supports what the report says about it. Fix anything that doesn't match, and tell me what you changed.
```

**Done when** the report gives the result the checker passed, every number in it traces to results/ or a paper, and
each paper says what the report claims (open one or two yourself).

## 7. Make it last (a skill)

```
Add what we learned about each site's file to the egfr-qc skill, and say so in its description, so the next session finds it without looking at the data again.
```

Read what it added before you trust it: a wrong note in a skill misleads every session after this one. Then quit,
start `opencode` again (a fresh session), and ask: *Without opening the data, what should I watch out for in site
B's file?*

**Done when** the new session answers from the skill. Anything you had to work out twice belongs in a skill or in
AGENTS.md.

## Extra 1: find the data yourself (the web, with your OK)

```
Read public/QUESTION.md. Which NHANES files and variables answer it? Check their codebooks on CDC's site, then download only those files into public/raw/.
```

Check what it chose against the codebooks before it goes on. Then:

```
Now answer the question with those files: write results/public.json, run `uv run checks/check_public.py` and fix what it reports until it says PASS.
```

Then quit and start a fresh session for the papers, so its earlier guesses don't steer it:

```
Use the pubmed tools to find the two papers named in public/QUESTION.md. Fetch each abstract, and quote word for word what it says about CKD prevalence and race, with its PMID. Then give me three sentences comparing results/public.json with them.
```

**Done when** the checker says PASS, each PMID opens to the paper it names, and you can say in a sentence what
changed and for whom. In our test, asked for papers at the end of a long session, it quoted its own numbers as if
published, under invented PMIDs. It asks before every web request and download: that's the permissions in
opencode.json at work.

## Extra 2: one big request, and a rule for the memory file

Steps 1 to 7 ask for one thing at a time. Ask for the whole job at once instead, in a fresh copy of the lab so it
starts from scratch (`git clone https://github.com/lix229/egfr-lab egfr-try`, then `cd egfr-try` and `opencode`):

```
Check the draft before it goes to the committee: look at each site's file, recompute the rapid decliners from the raw files with egfr.py so that `uv run pytest` passes, write results/ as AGENTS.md says, run `uv run checks/check.py` until it says PASS, then write reports/report.md with the corrected result.
```

When it says it's done, check for yourself: `ls reports/`. Is the report it describes there?

If not, it's a correction you'd make every time, so try the memory file. Add this to the end of AGENTS.md in a second
fresh copy (`egfr-try2`), then start `opencode` there: AGENTS.md loads when a session starts, not in the middle of one.

```
## Finish what you start
- When I ask for several things, do every one before you stop.
- Before you say you're done, prove each part with a command's output: `ls -l` every file I asked you to write, and
  `uv run checks/check.py` for the results. If something is missing, do it, then prove it again.
- Don't end a reply with what you'll do next: do it. Stop early only for a decision only I can make.
```

Give it the same big request, and check `ls reports/` again. Then, in whichever copy is still missing its report, ask
for the proof in the conversation instead:

```
Go back over my request part by part. For each part, show me the command output that proves it's done (ls -l for files). Do whatever is missing.
```

**Done when** you know which of the two made it finish, and why. In our tests the big request skipped the report in 8
of 9 runs, usually saying it had written it; with the rule in AGENTS.md it wrote it in 1 of 6, and never ran the
`ls -l` the rule asks for; the follow-up fixed it both times, in seconds. A memory file is good for facts it can't
know (the date range in AGENTS.md ended its "future dates" mistakes); a rule about how to work is a request it may
skip. Asking for one thing at a time, and for the proof, is what worked. About 15 cents.

## Extra 3: plant the answer (a positive control)

```
Copy data/ to control/ and give 5 patients of your choice at site B an eGFR drop of 40% within six months. Run the analysis on control/ and show me that it finds exactly those 5 on top of the original decliners.
```

**Done when** it finds the 5 you planted and still finds the original ones. That is how you test code you couldn't
have written yourself.

## Extra 4: have it teach you

```
Make egfr.html: one page that shows how CKD-EPI 2021 eGFR changes with creatinine, age and sex, with sliders. Then add five lines on what I learned to notes.md.
```

**Done when** egfr.html opens in your browser, the sliders move, and a 50-year-old woman with creatinine 1.0 mg/dL
reads about 69.
