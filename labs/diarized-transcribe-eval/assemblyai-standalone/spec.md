# AssemblyAI 独立方案

## 架构

```
音频输入 → AssemblyAI (ASR + 说话人识别，一步完成) → 输出
```

## 组件

| 组件 | 模型/工具 | 职责 |
|------|----------|------|
| ASR + Diarization | AssemblyAI universal-3-pro | 语音转文字 + 说话人识别，全部由 API 完成 |

## 协作方式

1. 上传音频到 AssemblyAI
2. API 同时完成 ASR 和 speaker diarization
3. 返回带 speaker label 的 utterances

## 依赖

- API: AssemblyAI（需要 ASSEMBLYAI_API_KEY）
- Python 包: assemblyai

## 优势与劣势

**优势:**
- 最简单，无本地模型依赖
- ASR + diarization 一步完成，无需串联多个组件
- 商业级质量保证

**劣势:**
- 完全依赖外部 API（成本、网络、隐私）
- 无法离线使用
- 中文 ASR 质量待验证（对比 Qwen3-ASR）
