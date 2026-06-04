# 本地字幕生成器

> [English](README.md)

**STT** 即 **S**peech **t**o **T**ext（语音转文字）。一个完全离线的语音转文字工具。将视频文件（`.mp4`、`.mov` 等）转为 `.srt` 字幕和 `.txt` 纯文本。基于 `faster-whisper` + `ctranslate2`，模型首次下载后无需网络。

## 快速开始

### 预编译二进制（无需安装 Python）

从 [GitHub Releases](https://github.com/tonylawx/stt/releases) 下载对应平台的压缩包，解压后把 `stt` 放到 PATH 里即可全局使用：

**macOS / Linux**

```bash
# 下载并解压
tar -xzf stt-macos-arm64.tar.gz        # Apple Silicon — 或 stt-macos-x86_64 / stt-linux-x86_64

# 安装到 PATH
sudo cp stt /usr/local/bin/
# 或者不用 sudo：
mkdir -p ~/.local/bin && cp stt ~/.local/bin/

# 安装完成，任意目录使用
stt /absolute/path/to/video.mp4
```

**Windows (PowerShell)**

```powershell
# 下载并解压 stt-windows-x86_64.zip
Expand-Archive stt-windows-x86_64.zip -DestinationPath .
# 复制到 PATH 中的目录，例如：
cp stt.exe C:\Windows\System32\
# 或将当前目录加入 PATH 后直接使用：
.\stt.exe C:\videos\example.mp4
```

二进制文件自带所有依赖，无需安装 Python、pip 或虚拟环境。首次运行时会自动下载 Whisper 模型。

### 从源码安装 (pip)

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

- Python 3.10+（仅从源码安装时需要）
- macOS、Linux 或 Windows

依赖项见 `requirements.txt`：

| 包名            | 用途              |
| --------------- | ----------------- |
| faster-whisper  | Whisper 模型推理   |
| ctranslate2     | 量化推理运行时     |
| tqdm            | 进度条            |

## 使用方式

```bash
# 二进制安装后
stt /absolute/path/to/video.mp4 [选项]

# 从源码
python transcribe.py /absolute/path/to/video.mp4 [选项]
```

### 常用选项

| 选项              | 默认值          | 说明                                          |
| ----------------- | --------------- | --------------------------------------------- |
| `--language`      | 自动检测        | 指定语言：`zh`、`en`、`ja` 等                  |
| `--model`         | `turbo`         | 模型选择：`tiny`、`base`、`small`、`medium`、`turbo` |
| `--output-dir`    | 与输入文件相同   | `.srt` / `.txt` 输出目录                       |
| `--cpu-threads`   | 自动            | 推理使用的 CPU 线程数                           |

### 模型说明

- `turbo` 是默认模型，对应 `large-v3-turbo`，在速度和精度之间取得了较好平衡。
- 首次使用时会自动下载模型权重，可能需要几分钟。
- 没有 GPU 也没关系，工具会完全在 CPU 上运行。

### Apple Silicon (M1 / M2 / M3 / M4)

Apple Silicon Mac 请下载 `stt-macos-arm64.tar.gz`。默认使用 CPU + `int8` 量化推理，并自动调节线程数。

```bash
stt /absolute/path/to/video.mp4 --cpu-threads 8
```

### 纯 CPU 环境

没有 GPU 也完全可以运行，只是慢一些。如果 `turbo` 感觉太重，可以试试 `base` 或 `small`。

## 常见用例

自动检测语言：

```bash
stt /absolute/path/to/video.mp4
```

强制指定语言：

```bash
stt /absolute/path/to/video.mp4 --language zh
```

选择更小的模型：

```bash
stt /absolute/path/to/video.mp4 --model base
```

指定输出目录：

```bash
stt /absolute/path/to/video.mp4 --output-dir /path/to/output
```

## 进阶：LLM 校准 & 双语字幕

STT 生成 `.srt` 字幕后，丢给大模型（ChatGPT、Claude、DeepSeek 等）就能一条龙完成校准和翻译，输出标准双语字幕。自己转录、自己校准、自己翻译，从此告别字幕下载网站。

**三步走：**

1. **校准** — 大模型结合上下文修正语音识别的错词和断句问题
2. **翻译** — 逐句翻译为中文（或其他目标语言）
3. **输出双语 SRT** — 保持原始时间轴，原文和译文交替排列

把下面这段 prompt 和你的 `.srt` 内容一起发给大模型即可：

```
你是一个专业的字幕校对和翻译助手。请处理以下 SRT 字幕，保持时间轴不变：

1. 结合上下文修正所有识别错误（专有名词、断句、同音词）
2. 将英文逐句翻译为简体中文，放在对应原文的下方
3. 用标准 SRT 格式输出，翻译行与原文行交替排列

以下是字幕内容：

[在此粘贴 .srt 文件内容]
```

> 提示：如果字幕较长，可以分段发送，每段 50-100 条即可。ChatGPT、Claude、DeepSeek 等模型都能胜任。



## License

MIT
