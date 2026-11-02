#!/usr/bin/env bash
# Installs the two programs this lab needs, if you don't have them yet: OpenCode (the agent's harness) and uv (it runs
# the lab's Python, with the right packages). Run it from this folder: bash setup.sh. On Windows, run it inside WSL.
# It uses each program's own installer (opencode.ai/docs, docs.astral.sh/uv), so you could also run those two lines yourself.
set -euo pipefail

# where the two installers put them, so this script can check them before you open a new terminal
export PATH="$HOME/.opencode/bin:${XDG_BIN_HOME:-$HOME/.local/bin}:$PATH"

if command -v opencode >/dev/null; then
  echo "OpenCode is already installed."
else
  echo "Installing OpenCode..."
  curl -fsSL https://opencode.ai/install | bash
fi

if command -v uv >/dev/null; then
  echo "uv is already installed."
else
  echo "Installing uv..."
  curl -LsSf https://astral.sh/uv/install.sh | sh
fi

echo
echo "OpenCode $(opencode --version)"
uv --version
echo
echo "Done. Open a new terminal, come back to this folder (cd egfr-lab), and go on to step 2: a key."
