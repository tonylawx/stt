# Local Subtitle Generator

> [中文文档](README.zh.md)

**STT** stands for **S**peech **t**o **T**ext. A local, offline speech-to-text tool that transcribes video files (`.mp4`, `.mov`, etc.) into `.srt` subtitle and `.txt` plain-text files. Uses `faster-whisper` with `ctranslate2` under the hood  --  no network required after the first model download.

## Quick Start

### Pre-built binary (no Python required)

Download the archive for your platform from [GitHub Releases](https://github.com/tonylawx/stt/releases), extract it, and install the `stt` binary:

**macOS / Linux**

```bash
# Download and extract
tar -xzf stt-macos-arm64.tar.gz        # Apple Silicon  --  or stt-macos-x86_64 / stt-linux-x86_64

# Install to PATH
sudo cp stt /usr/local/bin/
# or, without sudo:
mkdir -p ~/.local/bin && cp stt ~/.local/bin/

# Ready to use  --  anywhere
stt /path/to/video.mp4
```

**Windows (PowerShell)**

```powershell
# Download and extract stt-windows-x86_64.zip
Expand-Archive stt-windows-x86_64.zip -DestinationPath .
# Copy to a directory in your PATH, e.g.:
cp stt.exe C:\Windows\System32\
# or add the current directory to PATH and use:
.\stt.exe C:\path\to\video.mp4
```

The binary bundles everything  --  no Python, no pip, no venv. The Whisper model is downloaded automatically on first run.

### From source (pip)

```bash
# 1. Create a virtual environment and install dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 2. Transcribe a video
python transcribe.py /path/to/video.mp4
```

Or use the bundled launcher scripts:

```bash
# Short command (macOS / Linux)
./stt /path/to/video.mp4

# Double-clickable launcher (macOS)
# Open transcribe.command in Finder, then drag your mp4 file into the Terminal window.
```

After the run finishes, you will find `video.srt` and `video.txt` alongside the input file (or in whatever directory you chose with `--output-dir`).

## Requirements

- Python 3.10+ (if installing from source)
- macOS, Linux, or Windows

Dependencies are listed in `requirements.txt`:

| Package        | Purpose                     |
| -------------- | --------------------------- |
| faster-whisper | Whisper model inference     |
| ctranslate2    | Quantized inference runtime |
| tqdm           | Progress bars               |

## Usage

```bash
# If installed via binary
stt /path/to/video.mp4 [options]

# From source
python transcribe.py /path/to/video.mp4 [options]
```

### Common Options

| Option           | Default         | Description                                                   |
| ---------------- | --------------- | ------------------------------------------------------------- |
| `--language`     | auto-detect     | Force a language code: `zh`, `en`, `ja`, etc.                 |
| `--model`        | `turbo`         | Whisper model: `tiny`, `base`, `small`, `medium`, `turbo`     |
| `--output-dir`   | same as input   | Where to write `.srt` / `.txt` files                          |
| `--cpu-threads`  | auto            | Number of CPU threads for inference                           |

### Model Notes

- `turbo` is the default and maps to `large-v3-turbo`. It offers a strong accuracy/speed balance.
- On first use the model weights are downloaded automatically. This can take a few minutes.
- If your machine lacks a GPU the tool still works  --  it will run entirely on CPU.

### Apple Silicon (M1 / M2 / M3 / M4)

On Apple Silicon Macs pick `stt-macos-arm64.tar.gz` from Releases. The tool defaults to CPU + `int8` quantized inference with automatic thread tuning.

```bash
stt /path/to/video.mp4 --cpu-threads 8
```

### Without a GPU

The tool works fine CPU-only  --  it is just slower. The `base` or `small` models can help if `turbo` feels too heavy.

## Common Examples

Auto-detect language:

```bash
stt /path/to/video.mp4
```

Force a language:

```bash
stt /path/to/video.mp4 --language zh
```

Choose a smaller model:

```bash
stt /path/to/video.mp4 --model base
```

Write output to a different directory:

```bash
stt /path/to/video.mp4 --output-dir /path/to/output
```

## License

MIT
