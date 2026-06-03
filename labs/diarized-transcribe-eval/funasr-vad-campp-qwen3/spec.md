# FunASR VAD + cam++ 聚类 + Qwen3-ASR 方案

## 架构

```
音频输入 → fsmn-vad (语音活动检测，切段) → ffmpeg (按区间切片) → cam++ (提取 speaker embedding) → AgglomerativeClustering (聚类分配 speaker ID) → Qwen3-ASR (逐段转文字) → 输出
```

## 组件

| 组件 | 模型/工具 | 职责 |
|------|----------|------|
| VAD | fsmn-vad (FunASR) | 检测语音段落，输出时间区间 |
| 音频切片 | ffmpeg | 按时间区间切割音频为 16kHz mono WAV |
| Speaker Embedding | cam++ (FunASR) | 对每段音频提取 192-dim speaker embedding |
| 聚类 | sklearn AgglomerativeClustering | 基于 embedding 余弦相似度聚类，分配 speaker ID |
| ASR | Qwen3-ASR-1.7B-4bit (MLX) | 对每段音频做语音转文字 |

## 协作方式

1. fsmn-vad 对整段音频做 VAD，输出时间区间列表（起止 ms）
2. ffmpeg 根据每个区间切出独立 WAV 片段
3. cam++ 对每个片段提取 192 维 speaker embedding
4. AgglomerativeClustering 对所有 embedding 聚类，分配 speaker ID
5. Qwen3-ASR 对每个片段独立转录
6. 合并：每段文本标注 speaker ID + 时间戳

## 依赖

- Python 包: funasr, mlx-audio, scikit-learn, numpy
- 本地模型: ~/Models/Qwen3-ASR-1.7B-4bit, fsmn-vad, cam++ (自动从 ModelScope 下载)
- 工具: ffmpeg

## 优势与劣势

**优势:**
- 完全本地，无 API 费用，无网络依赖
- 不需要 HuggingFace 授权（cam++ 从 ModelScope 下载）
- cam++ 极轻量（26.7MB），embedding 提取很快
- fsmn-vad 切段粒度适中（~600 段 vs pyannote 4000+ 段），转录速度快
- ASR 质量由 Qwen3-ASR 保证

**劣势:**
- 聚类需要预设 speaker 数量（或用自动估计）
- VAD 切段粒度可能不如专门的 diarization 模型精准
- cam++ 在噪声环境下 embedding 质量可能下降
