# egfr-lab: an agent on kidney labs

A hands-on exercise from the guest lecture *AI agents for biomedical research*. You get a research task the way it
would arrive at work, a message with a deadline and a question that matters, and an agent (OpenCode, with one of UF's
models through the NaviGator Toolkit) to do it with. How you go about it is up to you; the lecture's ideas are all in
this folder: a memory file, tools in a loop, a skill, subagents, permissions, an MCP tool, a check you can trust, and
a second model for a second opinion.

The data are synthetic: 12,408 creatinine results for 1,204 made-up patients at three clinic sites. No real patients.

## What it costs

Every UF student, faculty and staff member gets monthly NaviGator Toolkit credit for UF's own models ($25 a month when
this was written). This lab runs on gpt-oss-120b, hosted on HiPerGator: $0.06 per million tokens in, $0.15 per million
out. In our test run, the whole task cost about 17 cents. OpenCode shows the running cost of each session.

## Set up (once, about 10 minutes)

On Windows, do all of this inside WSL (Ubuntu): in PowerShell as administrator run `wsl --install`, restart, and open
Ubuntu.

1. **Get the lab, and let it install what it needs:**

   ```
   git clone https://github.com/lix229/egfr-lab
   cd egfr-lab
   bash setup.sh
   ```

   `setup.sh` installs OpenCode (the agent's harness) and uv (it runs this lab's Python), if you don't have them yet,
   with each one's own installer. Then open a new terminal and go back into `egfr-lab`.
   No git? On this page, **Code → Download ZIP**; unzip it, go into `egfr-lab-main`, and run `bash setup.sh` there. On a
   Mac, your first `git` may offer to install Apple's developer tools, which takes a few minutes: the ZIP is quicker.

2. **Get a NaviGator key.** Go to https://api.ai.it.ufl.edu/ui and sign in with your GatorLink. Click
   **Create New Key**. Give it a **Key Name** (say, egfr-lab) and, under **Models**, pick gpt-oss-120b
   and nemotron-3-super-120b-a12b. Leave the optional settings. Click **Create Key** and copy the key:
   this is the only time it is shown.

3. **Give the key to OpenCode, not to your shell.** Run `opencode`, type `/connect`, choose **Other**, enter the ID
   `navigator`, and paste the key. OpenCode keeps it in `~/.local/share/opencode/auth.json`, a file only you can read.
   Don't put it in a project file, a notebook or a chat, or export it in your shell: every program you start, the
   agent's own commands included, could read it from there.

4. **Check the key works.** In the `egfr-lab` folder:

   ```
   opencode run "Reply with one word: ready"
   ```

   It should print *ready*. It works here because this folder's `opencode.json` tells OpenCode where `navigator` is:
   NaviGator's address and its two models. In any other folder OpenCode doesn't know that yet; to use UF's models
   there too, see [Use NaviGator outside the lab](#use-navigator-outside-the-lab).

## Start

In the `egfr-lab` folder, run `opencode`, then type `/start`. Your task arrives the way it would at work: a message
from the chair of the clinics' quality committee, with tomorrow's question and what they need from you. There are no
steps to follow: plan it the way you would a real task, use what's in this folder, and check what the agent tells you.
Type `/start` again whenever you want to reread the message.

Stuck? Ask the agent for a hint. It gives help in three layers, one at a time: a nudge, then the workflow we used,
then example prompts. If it stops before it's done, type *Go on.*

## What's here

| | |
|---|---|
| `setup.sh` | Installs OpenCode and uv, if you don't have them yet. |
| `AGENTS.md` | The project's memory: the question, the rules, where things are. OpenCode loads it at every start. |
| `opencode.json` | This project's settings: the NaviGator models and their prices, what the agent may do without asking, and the PubMed tool. |
| `.opencode/commands/start.md` | `/start`: your task arrives, as a message. |
| `.opencode/skills/` | Three skills, each loaded only when needed: `lab-start` (the scene and the message), `egfr-qc` (the lab's QC protocol), `lab-help` (hints, when you ask). |
| `.opencode/agents/site-qc.md` | A read-only subagent that checks one site's file. |
| `tools/pubmed.py` | A small MCP server: search PubMed and read abstracts. |
| `data/` | The synthetic extract. Read-only: the settings won't let the agent change it. |
| `public/QUESTION.md` | The committee's follow-up, on real public data (NHANES) that the agent finds and downloads, with your OK. |
| `tests/` | What "done" means for `egfr.py`. |
| `checks/check.py` | The data team's check: compares your results with their audit, and hints where to look if they're off. |
| `checks/check_public.py` | The same, for the follow-up. |
| `reports/draft_report.md` | The draft the committee is waiting on: written by an agent, never checked. |

## Use NaviGator outside the lab

Your key works in any folder, but OpenCode only knows where `navigator` is from an `opencode.json`. This lab has its
own, and a project's `opencode.json` applies only inside that project. Elsewhere, OpenCode doesn't stop with an error:
it quietly uses a free model of its own (in our test, `big-pickle`, from OpenCode's own service), so your prompts and
anything the agent reads go off UF's servers.

To use UF's models everywhere, put the same provider lines in your own settings file, `~/.config/opencode/opencode.json`,
which OpenCode reads in every folder. Create it if it isn't there (`mkdir -p ~/.config/opencode` first); if it is, add
the `"provider"` entry to what's in it.

```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "navigator/gpt-oss-120b",
  "provider": {
    "navigator": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "UF NaviGator",
      "options": {
        "baseURL": "https://api.ai.it.ufl.edu/v1"
      },
      "models": {
        "gpt-oss-120b": {
          "name": "gpt-oss-120b (HiPerGator)",
          "tool_call": true,
          "reasoning": true,
          "limit": { "context": 128000, "output": 16384 },
          "cost": { "input": 0.06, "output": 0.15 }
        },
        "nemotron-3-super-120b-a12b": {
          "name": "Nemotron 3 Super (HiPerGator)",
          "tool_call": true,
          "reasoning": true,
          "limit": { "context": 262144, "output": 16384 },
          "cost": { "input": 0.06, "output": 0.24 }
        }
      }
    }
  }
}
```

- `navigator` must match the ID you gave `/connect`; that's how OpenCode pairs the key with the address.
- `baseURL` is NaviGator's address. `cost` is UF's price per million tokens, so OpenCode can show what a session costs.
- A model answers only if you picked it when you made your key. To add another of UF's models, add it to your key
  in the NaviGator portal, then add an entry under `"models"` with its ID.

Then check it from any folder that isn't the lab, for example your home folder:

```
cd ~
opencode run "Reply with one word: ready"
```

It should print *ready*, under a line that names the model: `gpt-oss-120b`, not `big-pickle`. In OpenCode itself, the
model's name is at the bottom of the screen.

The lab's other settings stay in the lab. Out of the box OpenCode lets the agent edit files and run commands without
asking; the lab makes it ask first. For the same everywhere, add this to your settings file, next to `"provider"`:

```json
"permission": { "edit": "ask", "bash": "ask" }
```
