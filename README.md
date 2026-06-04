# Local Subtitle Generator

A local, offline speech-to-text tool that transcribes video files (`.mp4`, `.mov`, etc.) into `.srt` subtitle and `.txt` plain-text files. Uses `faster-whisper` with `ctranslate2` under the hood — no network required after the first model download.

## Quick Start

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

- Python 3.10+
- macOS, Linux, or Windows

Dependencies are listed in `requirements.txt`:

| Package       | Purpose                        |
| ------------- | ------------------------------ |
| faster-whisper | Whisper model inference       |
| ctranslate2   | Quantized inference runtime    |
| tqdm          | Progress bars                  |

## Usage

```bash
python transcribe.py /path/to/video.mp4 [options]
```

### Common Options

| Option            | Default            | Description                                      |
| ----------------- | ------------------ | ------------------------------------------------ |
| `--language`      | auto-detect        | Force a language code: `zh`, `en`, `ja`, etc.    |
| `--model`         | `turbo`            | Whisper model: `tiny`, `base`, `small`, `medium`, `turbo` |
| `--output-dir`    | same as input      | Where to write `.srt` / `.txt` files             |
| `--cpu-threads`   | auto               | Number of CPU threads for inference              |

### Model Notes

- `turbo` is the default and maps to `large-v3-turbo`. It offers a strong accuracy/speed balance.
- On first use the model weights are downloaded automatically. This can take a few minutes.
- If your machine lacks a GPU the tool still works — it will run entirely on CPU.

### Apple Silicon (M1 / M2 / M3 / M4)

On Apple Silicon Macs the tool defaults to CPU + `int8` quantized inference with automatic thread tuning. The launcher scripts (`stt` and `transcribe.command`) force `arm64` so you never accidentally launch under Rosetta.

```bash
# Manual thread override if needed
python transcribe.py /path/to/video.mp4 --cpu-threads 8
```

### Without a GPU

The tool works fine CPU-only — it is just slower. The `base` or `small` models can help if `turbo` feels too heavy.

---

# 本地字幕生成器

一个完全离线的语音转文字工具。将视频文件（`.mp4`、`.mov` 等）转为 `.srt` 字幕和 `.txt` 纯文本。基于 `faster-whisper` + `ctranslate2`，模型首次下载后无需网络。

## 快速开始

```bash
# 1. 创建虚拟环境并安装依赖
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 2. 转写视频
python transcribe.py /absolute/path/to/video.mp4
```

也可以使用附带的启动脚本：

```bash
# 短命令 (macOS / Linux)
./stt /absolute/path/to/video.mp4

# 双击启动 (macOS)
# 在 Finder 中打开 transcribe.command，然后把 mp4 文件拖进终端窗口回车即可。
```

运行完成后，输入文件旁边会生成 `video.srt` 和 `video.txt`（或通过 `--output-dir` 指定目录）。

## 环境要求

- Python 3.10+
- macOS、Linux 或 Windows

依赖项见 `requirements.txt`：

| 包名            | 用途               |
| --------------- | ------------------ |
| faster-whisper  | Whisper 模型推理    |
| ctranslate2     | 量化推理运行时      |
| tqdm            | 进度条             |

## 使用方式

```bash
python transcribe.py /absolute/path/to/video.mp4 [选项]
```

### 常用选项

| 选项              | 默认值          | 说明                                      |
| ----------------- | --------------- | ----------------------------------------- |
| `--language`      | 自动检测        | 指定语言：`zh`、`en`、`ja` 等             |
| `--model`         | `turbo`         | 模型选择：`tiny`、`base`、`small`、`medium`、`turbo` |
| `--output-dir`    | 与输入文件相同   | `.srt` / `.txt` 输出目录                  |
| `--cpu-threads`   | 自动            | 推理使用的 CPU 线程数                      |

### 模型说明

- `turbo` 是默认模型，对应 `large-v3-turbo`，在速度和精度之间取得了较好平衡。
- 首次使用时会自动下载模型权重，可能需要几分钟。
- 没有 GPU 也没关系，工具会完全在 CPU 上运行。

### Apple Silicon (M1 / M2 / M3 / M4)

Apple Silicon Mac 上默认使用 CPU + `int8` 量化推理，并自动调节线程数。启动脚本（`stt` 和 `transcribe.command`）会强制走 `arm64`，不会意外跑在 Rosetta 下。

```bash
# 如需手动指定线程数
python transcribe.py /absolute/path/to/video.mp4 --cpu-threads 8
```

### 纯 CPU 环境

没有 GPU 也完全可以运行，只是慢一些。如果 `turbo` 感觉太重，可以试试 `base` 或 `small`。

## 常见用例

自动检测中文：

```bash
python transcribe.py /absolute/path/to/video.mp4
```

强制中文：

```bash
python transcribe.py /absolute/path/to/video.mp4 --language zh
```

选择更小的模型：

```bash
python transcribe.py /absolute/path/to/video.mp4 --model base
```

指定输出目录：

```bash
python transcribe.py /absolute/path/to/video.mp4 --output-dir /path/to/output
```

## License

MIT
