# TSE (Target Speaker Extraction) + MIMO-v2.5-ASR 方案

## 核心思路

不按时间切片（避免重叠问题），而是用声纹从信号层面分离每个说话人的声音，再分别 ASR。

## 架构

```
音频输入 ──┬── AssemblyAI diarization ──→ speakers.json（说话人时间区间）
           │                                    │
           │                            自动选取参考片段（RMS 能量过滤）
           │                                    │
           │                                    ↓
           ├── 参考音频 × N ──→ 声纹提取（WeSpeaker/3D-Speaker）──→ speaker embeddings
           │
           └── TSE 模型（SpEx+ / pBSRNN）──→ 每个说话人独立音轨 ──→ MIMO ASR ──→ 输出
               (输入: 混合音频 + 目标 embedding)
```

## 组件

| 组件 | 模型/工具 | 职责 |
|------|----------|------|
| Diarization | AssemblyAI universal-3-pro | 初步说话人识别 + 时间区间（用于选取参考片段） |
| 参考片段提取 | extract_references.py | 从 diarization 结果中自动选取每人最干净的音频段（RMS 能量过滤） |
| 声纹提取 | WeSpeaker campplus-cn-common-200k | 从参考片段提取 speaker embedding（中文优化） |
| 语音分离 | SpEx+（ClearerVoice-Studio）或 pBSRNN（WeSep） | 给定目标 embedding，从混合音频中提取该说话人的声音 |
| ASR | MIMO-v2.5-ASR-MLX (4bit) | 对分离后的干净音轨做语音转文字 |

## 协作方式

1. AssemblyAI 对整段音频做 speaker diarization，输出 utterances
2. 从 diarization 结果中，为每个说话人自动选取一段"干净"的参考音频（3-8 秒，前后有间隔，RMS 能量高于阈值）
3. 用 WeSpeaker 从参考音频提取 speaker embedding
4. TSE 模型对整段音频做 N 次 target extraction（N = 说话人数），每次输入目标 embedding，输出只包含该人声音的音轨
5. 对每条分离后的音轨用 MIMO ASR 转录
6. 合并：根据各音轨的有声/无声时间段，还原对话时序

## 参考片段选取策略

```
候选过滤: 时长 3-8秒 + 前后间隔 ≥ 200ms
排序: 按前后间隔总和降序
验证: RMS 能量 ≥ 阈值（排除静音段）
回退: 若无候选满足阈值，选 RMS 最高的
```

## 依赖

- API: AssemblyAI（仅用于初始 diarization，可复用缓存结果）
- Python 包: assemblyai, wespeaker, clearvoice (或 wesep), numpy
- 本地模型: 
  - MIMO-v2.5-ASR-MLX (4bit, ~/Models/)
  - WeSpeaker campplus-cn-common-200k
  - SpEx+ 预训练权重（ClearerVoice-Studio 提供）
- 工具: ffmpeg

## 优势

- **从信号层解决重叠问题** — 不依赖时间边界切割，即使两人同时说话也能分离
- **声纹引导精准** — 明确知道"要提取谁"，不像盲分离需要后续匹配身份
- **参考音频自动获取** — 不需要人工准备，从 diarization 结果自动选取
- **中文声纹成熟** — WeSpeaker 有 20 万中文说话人训练的模型
- **ASR 输入质量高** — 分离后的音轨只有单人声音，ASR 准确率更高

## 风险与待验证

- **TSE 模型中文效果未知** — 现有预训练均基于英文合成数据（WSJ0-2mix），中文会议场景需实测
- **ClearerVoice SpEx+ 仅 8kHz** — 可能需要降采样处理，分离质量受限
- **计算量** — N 个说话人 × 全音频长度的 TSE 推理 + ASR
- **真实会议 vs 合成数据** — 远场、混响、噪声等条件下效果待验证
- **WeSpeaker embedding 与 TSE 模型对接** — 需确认维度兼容性

## 备选 TSE 模型

| 模型 | 来源 | 特点 |
|------|------|------|
| SpEx+ | ClearerVoice-Studio | pip install 即用，有权重，8kHz |
| pBSRNN | WeSep | 原生集成 WeSpeaker，权重待发布 |
| TSExcalibur | GitHub | 多架构可选，HuggingFace 有权重 |
| MossFormer2 MLX + 声纹匹配 | mlx-community | Apple Silicon 原生，但为盲分离 |

## 状态

待实施 — 参考音频提取已完成（extract_references.py），下一步安装 ClearerVoice-Studio 验证 TSE 效果。
