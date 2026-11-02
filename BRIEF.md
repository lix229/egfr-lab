# The brief

*A message from Sam, who chairs the clinics' quality committee. You started this week.*

---

Hi, and welcome. I'm afraid your first job is a real one, and it's due tomorrow.

At 9 tomorrow the quality committee decides whether to fund a nurse-led follow-up for patients whose kidney function is
falling fast. The case rests on one number: how many of our patients had a rapid decline in eGFR between 2023 and 2025.
A draft from last month says 3.1% (`reports/draft_report.md`). An agent session wrote it and nobody checked it, and I'm
not putting it in front of the committee until we have.

Here's what they'll ask, so it's what I need from you:

- **The number, and who.** How many patients, out of how many, and which ones: if they fund it, the nurses start from
  your list.
- **Why we believe it.** What you checked, and how. The extract comes from our three sites, each with its own lab
  system, and I wouldn't assume they agree on much.
- **Why "rapid" means what we say.** We use a fall of more than 30% within a year (it's in `AGENTS.md`). Someone always
  asks where that comes from; I'd like to answer with the papers, not a shrug.
- **That we can do it again.** If they fund it, we'll rerun this on every quarter's extract. I don't want anyone
  starting from scratch each time.

The data team audited this extract. Their script, `uv run checks/check.py`, tells you whether your numbers match
theirs, and gives a hint if they don't. Results go where `AGENTS.md` says; the report for the committee goes in
`reports/report.md`: one page, plain words.

There's an agent set up in this folder, with a few tools (the README lists them). It's fast, and it can be confidently
wrong. Check it the way you'd check a new colleague.

Thanks,
Sam

---

## If there's time

The committee's follow-ups, and one of my own:

- **A national view.** A committee member asked whether the 2021 equation, the one without the race term, changed who
  counts as having low kidney function across the US. There's public data for that; `public/QUESTION.md` has the
  question and a starting point. The agent can go online, but it asks you first.
- **Would it find them?** Before the nurses rely on the list, I'd like to know the analysis finds rapid decliners when
  they're there. You can't tell by looking at real results. How would you test it?
- **Your own explainer.** If eGFR is new to you, have the agent build you something that shows how it moves with
  creatinine, age and sex. You'll explain it to the committee better.
- **An experiment on the agent.** In a fresh copy of the lab, ask for the whole job in one message, then check whether
  it really did all of it. If it didn't, can a line in `AGENTS.md` fix that, or does something else work better?

## When you're stuck

Ask the agent. It has hints for this brief, in three layers: a nudge, then the workflow we used, then example prompts.
Ask for one layer at a time; it asks before opening the deeper ones, because they're spoilers.
