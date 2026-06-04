# Qwen3.5-Omni 方案

## 架构

```
音频输入 → Qwen3.5-Omni API (ASR + 说话人识别 + 时间戳，一步完成) → 输出
```

## 组件

| 组件 | 模型/工具 | 职责 |
|------|----------|------|
| ASR + Diarization | Qwen3.5-Omni (阿里云 Model Studio API) | 语音转文字 + 说话人映射 + 时间戳 |

## 能力亮点（官方宣称）

- 脚本级字幕：带时间戳、场景切换、说话者映射
- 原生支持最多 10 小时音频
- 识别 113 种语言（口语）
- 训练数据 1 亿+ 小时
- SOTA：音频表现优于 Gemini-3.1 Pro

## 依赖

- API: 阿里云 Model Studio（需要 API key）
- API 文档: https://alibabacloud.com/help/en/model-studio/qwen-omni
- 变体: Plus / Flash / Light

## 优势与劣势

**优势:**
- 一步完成 ASR + 说话人识别，无需组合多个模型
- 中文为母语模型，ASR 质量可能优于 AssemblyAI
- 支持超长音频（10h）
- 可能是目前最接近"端到端解决问题"的方案

**劣势:**
- 纯 API，无开源权重，无法本地部署
- 需要阿里云账号和 API key
- 费用待确认
- speaker mapping 的具体效果未验证

## 状态

待运行 — 需要先开通阿里云 Model Studio API key。
