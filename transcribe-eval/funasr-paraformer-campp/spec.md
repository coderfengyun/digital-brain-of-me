# FunASR: Paraformer + cam++ 方案

## 架构

```
音频输入 → fsmn-vad (语音活动检测) → Paraformer-large (ASR) → ct-punc (标点恢复) → cam++ (说话人识别) → 输出
```

## 组件

| 组件 | 模型 | 参数量 | 职责 |
|------|------|--------|------|
| VAD | fsmn-vad | - | 检测语音段落，切分静音区间 |
| ASR | speech_seaco_paraformer_large | ~220M | 语音转文字 + 时间戳 |
| 标点 | ct-punc | ~1GB | 恢复标点符号 |
| 说话人 | cam++ | 7.2M (26.7MB) | 说话人向量提取 + 聚类 |

## 协作方式

FunASR 内部流水线：
1. fsmn-vad 将整段音频切成语音片段（max_single_segment_time: 30000ms）
2. Paraformer 对每个片段做 ASR，输出文字 + 字级时间戳
3. ct-punc 对 ASR 输出做标点恢复
4. cam++ 提取每个语音片段的说话人 embedding，通过聚类分配 speaker ID

说话人识别依赖 Paraformer 的时间戳输出（SenseVoiceSmall 不支持时间戳，无法配合 cam++）。

## 运行配置

```python
from funasr import AutoModel

model = AutoModel(
    model='iic/speech_seaco_paraformer_large_asr_nat-zh-cn-16k-common-vocab8404-pytorch',
    vad_model='fsmn-vad',
    vad_kwargs={'max_single_segment_time': 30000},
    spk_model='cam++',
    punc_model='ct-punc',
    device='cpu',
)

res = model.generate(
    input='<audio_file>',
    cache={},
    batch_size_s=60,
)
```

## 依赖

- Python 包：funasr, torchaudio, modelscope
- 模型缓存：~/.cache/modelscope/hub/models/iic/
- 运行设备：CPU（Apple Silicon，未使用 MPS）

## 运行结果

- 耗时：1812s（约 30 分钟），RTF 0.204
- 总句数：4295
- 说话人识别：5 人（Speaker 0: 2959, Speaker 1: 292, Speaker 2: 434, Speaker 3: 429, Speaker 4: 181）
- 峰值内存：未测量

## 已知问题

1. **ASR 质量不如 Qwen3-ASR** — 多处识别错误：
   - "高亮" → "高粱"
   - "不能" → "孤独"
   - "亮" → "量"
   - 专业术语识别较弱（prompt、板书等上下文相关词）

2. **说话人分布不均** — Speaker 0 占 69%，可能存在误分类

3. **运行速度较慢** — 30 分钟处理 23 分钟音频，RTF > 1（CPU 模式）

## 输出格式

每句包含：speaker ID、起止时间（ms）、文字内容

```
[Speaker 0] 360ms-1500ms: 要不应该都可以做明白。
[Speaker 2] 1600ms-3190ms: 对啊，
```
