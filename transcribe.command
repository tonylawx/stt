#!/bin/zsh

set -euo pipefail

if [[ "$(uname -s)" == "Darwin" && "$(uname -m)" == "arm64" ]]; then
  CURRENT_ARCH="$(arch)"
  if [[ "$CURRENT_ARCH" != "arm64" ]]; then
    exec /usr/bin/arch -arm64 "$0" "$@"
  fi
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_PYTHON="$SCRIPT_DIR/.venv/bin/python"

if [[ ! -x "$VENV_PYTHON" ]]; then
  echo "Creating virtual environment..."
  /usr/bin/arch -arm64 python3 -m venv "$SCRIPT_DIR/.venv"
fi

if ! /usr/bin/arch -arm64 "$VENV_PYTHON" -c "import av; import faster_whisper" >/dev/null 2>&1; then
  echo "Installing dependencies..."
  /usr/bin/arch -arm64 "$VENV_PYTHON" -m pip install -r "$SCRIPT_DIR/requirements.txt"
fi

INPUT_PATH="${1:-}"

if [[ -z "$INPUT_PATH" ]]; then
  echo "Drag your mp4 file into this window, then press Enter:"
  read -r INPUT_PATH
fi

/usr/bin/arch -arm64 "$VENV_PYTHON" "$SCRIPT_DIR/transcribe.py" "$INPUT_PATH"

echo
echo "Done. Press Enter to close."
read -r
