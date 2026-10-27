# egfr-lab: an agent on kidney labs

A hands-on exercise from the guest lecture *AI agents for biomedical research*. You run an agent (OpenCode, with one
of UF's models through the NaviGator Toolkit) on a small EHR extract and watch the lecture's ideas happen: a memory
file, tools in a loop, a skill, subagents, permissions, an MCP tool, a check you can trust, and a second opinion from
another model.

The data are synthetic: 12,408 creatinine results for 1,204 made-up patients at three clinic sites. No real patients.

## What it costs

Every UF student, faculty and staff member gets monthly NaviGator Toolkit credit for UF's own models ($25 a month when
this was written). This lab runs on gpt-oss-120b, hosted on HiPerGator: $0.06 per million tokens in, $0.15 per million
out. In our test run all seven tasks together cost about 12 cents. OpenCode shows the running cost of each session.

## Set up (once, about 10 minutes)

On Windows, do all of this inside WSL (Ubuntu): in PowerShell as administrator run `wsl --install`, restart, and open
Ubuntu.

1. **Install OpenCode and uv** (uv runs this lab's Python):

   ```
   curl -fsSL https://opencode.ai/install | bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

   Then open a new terminal.

2. **Get a NaviGator key.** Go to https://api.ai.it.ufl.edu/ui and sign in with your GatorLink. Click
   **Create New Key**. Give it a **Key Name** (say, egfr-lab) and, under **Models**, pick gpt-oss-120b
   and nemotron-3-super-120b-a12b. Leave the optional settings. Click **Create Key** and copy the key:
   this is the only time it is shown.

3. **Give the key to OpenCode, not to your shell.** Run `opencode`, type `/connect`, choose **Other**, enter the ID
   `navigator`, and paste the key. OpenCode keeps it in `~/.local/share/opencode/auth.json`, a file only you can read.
   Don't put it in a project file, a notebook or a chat, or export it in your shell: every program you start, the
   agent's own commands included, could read it from there.

4. **Get the lab, and check the key works:**

   ```
   git clone https://github.com/lix229/egfr-lab
   cd egfr-lab
   opencode run "Reply with one word: ready"
   ```

   It should print *ready*. No git? On this page, **Code → Download ZIP**; unzip it and go into `egfr-lab-main`.

## Start

In the `egfr-lab` folder, run `opencode`. Then work through [TASKS.md](TASKS.md).

## What's here

| | |
|---|---|
| `AGENTS.md` | The project's memory: the question, the rules, where things are. OpenCode loads it at every start. |
| `opencode.json` | This project's settings: the NaviGator models and their prices, what the agent may do without asking, and the PubMed tool. |
| `.opencode/skills/egfr-qc/` | The lab's QC protocol, as a skill: loaded only when needed. |
| `.opencode/agents/site-qc.md` | A read-only subagent that checks one site's file. |
| `tools/pubmed.py` | A small MCP server: search PubMed and read abstracts. |
| `data/` | The synthetic extract. Read-only: the settings won't let the agent change it. |
| `tests/` | What "done" means for `egfr.py`. |
| `checks/check.py` | Checks your results against the planted answer, and hints where to look if they're off. |
| `reports/draft_report.md` | An earlier write-up, with a mistake in it. |
