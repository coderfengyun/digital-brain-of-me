# pyannote-audio Diarization + Qwen3-ASR 方案

## 架构

```
音频输入 → pyannote-audio (说话人识别 + 时间区间) → ffmpeg (按区间切片) → Qwen3-ASR (逐段转文字) → 输出
```

## 组件

| 组件 | 模型/工具 | 职责 |
|------|----------|------|
| Diarization | pyannote/speaker-diarization-3.1 | 说话人识别，输出每个说话人的时间区间 |
| 音频切片 | ffmpeg | 按时间区间切割音频为 16kHz mono WAV |
| ASR | Qwen3-ASR-1.7B-4bit (MLX) | 对每段音频做语音转文字 |

## 协作方式

1. pyannote Pipeline 对整段音频做 speaker diarization，输出 RTTM 格式（speaker + start + duration）
2. ffmpeg 根据每段时间区间切出独立音频片段
3. Qwen3-ASR 对每个片段独立转录
4. 合并：每段文本标注 speaker ID + 时间戳

## 依赖

- Python 包: pyannote.audio, torch, mlx-audio
- HuggingFace token（需要在 HF 上接受 pyannote 模型使用条款）
- 本地模型: ~/Models/Qwen3-ASR-1.7B-4bit
- 工具: ffmpeg

## 优势与劣势

**优势:**
- 完全开源，无 API 费用
- 本地运行，无网络依赖
- pyannote 是学术界主流 diarization 方案，社区活跃

**劣势:**
- 模型需要 HuggingFace 授权（接受使用条款）
- GPU 加速效果明显，纯 CPU 可能较慢
- 需要较多本地资源（模型 + torch）
