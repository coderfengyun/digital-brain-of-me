# 语音转文字方案对比

对同一段音频使用不同方案转录，对比 ASR 质量和说话人识别效果。

## 测试音频

- 文件：`~/Downloads/新录音 2.m4a`
- 时长：约 23 分钟（8491 秒）
- 场景：多人会议录音（约 5 人）
- 语言：中文
- 大小：135MB

## 方案列表

| 方案 | 目录 | ASR 模型 | 说话人识别 | 状态 |
|------|------|----------|-----------|------|
| FunASR (Paraformer + cam++) | `funasr-paraformer-campp/` | speech_seaco_paraformer_large | cam++ | 已完成 |
| AssemblyAI + Qwen3-ASR | `assemblyai-qwen3/` | Qwen3-ASR-1.7B-4bit | AssemblyAI universal-3-pro | 已完成 |
| AssemblyAI + MIMO-v2.5-ASR | `assemblyai-mimo/` | MIMO-v2.5-ASR | AssemblyAI universal-3-pro | 待运行 |
| FunASR VAD + cam++ + Qwen3-ASR | `funasr-vad-campp-qwen3/` | Qwen3-ASR-1.7B-4bit | fsmn-vad + cam++ 聚类 | 待运行 |
| pyannote + Qwen3-ASR | `pyannote-qwen3/` | Qwen3-ASR-1.7B-4bit | pyannote/speaker-diarization-3.1 | 已完成 |
| Qwen3-ASR (MLX) | - | Qwen3-ASR-1.7B-4bit | 无 | 仅转录，无说话人 |

## 评估维度

1. **ASR 准确率** — 转录文字与实际内容的一致性
2. **说话人识别** — 能否区分不同说话人
3. **时间戳精度** — 时间对齐是否准确
4. **运行性能** — 耗时、内存占用
5. **部署便利性** — 本地运行难度、依赖复杂度
