# AssemblyAI Diarization + MIMO-v2.5-ASR 方案

## 架构

```
音频输入 → AssemblyAI (说话人识别 + 时间区间) → ffmpeg (按区间切片) → MIMO-v2.5-ASR (逐段转文字) → 输出
```

## 组件

| 组件 | 模型/工具 | 职责 |
|------|----------|------|
| Diarization | AssemblyAI universal-3-pro | 说话人识别，输出每个说话人的时间区间 |
| 音频切片 | ffmpeg | 按时间区间切割音频为 16kHz mono WAV |
| ASR | MIMO-v2.5-ASR | 对每段音频做语音转文字 |

## 协作方式

1. AssemblyAI 对整段音频做 speaker diarization，输出 utterances（speaker + start/end）
2. ffmpeg 根据每个 utterance 的时间区间切出独立音频片段
3. MIMO-v2.5-ASR 对每个片段独立转录，输出纯文本
4. 合并：每段文本标注 speaker ID + 时间戳

## 依赖

- API: AssemblyAI（需要 ASSEMBLYAI_API_KEY）
- Python 包: assemblyai, transformers（或 MLX 版本，待确认）
- 本地模型: XiaomiMiMo/MIMO-v2.5-asr（待下载）
- 工具: ffmpeg

## 优势与劣势

**优势:**
- ASR 模型更新，可能在中文识别上有进一步提升
- 说话人识别由 AssemblyAI 商业 API 保证质量
- 可复用 assemblyai-qwen3 方案的 speaker segments（跳过 API 调用）

**劣势:**
- 依赖外部 API（成本、网络延迟）
- MIMO-v2.5-ASR 本地部署方式待确认（是否有 MLX 版本）
- 两阶段串行，总耗时 = API 耗时 + 本地转录耗时

## 状态

待运行 — 需要先确认模型下载和推理方式。
