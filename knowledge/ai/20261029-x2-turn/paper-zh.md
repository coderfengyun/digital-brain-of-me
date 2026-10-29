# X2-Turn：用于流式 ASR 与轮次状态联合预测的帧同步双头建模

作者：Kaiqi Fu、Rime Wen、Altman Lin、Shawn Qin、Roy Gan、Hao Wang、Qian Wang（X Square Robot）

## 摘要

准确而及时的轮次交接对口语对话系统至关重要。系统必须实时区分用户打断、应被忽略的附和以及一句话真正结束。既有模块化方法通常在整句或固定音频块上优化轮次状态，与连续状态估计不匹配，并常依赖额外 ASR，限制响应速度、增加复杂度。

本文提出 X2-Turn：一种基于延迟流建模的帧同步轮次预测方法。它以预训练 Voxtral Realtime 为基础，在共享流式表示上，让帧同步 Turn Head 与 ASR Head 并行工作，逐帧联合预测 ASR token 与细粒度轮次状态。中英双语 EasyTurn 和 Full-Duplex-Bench 实验显示，该方法能在状态准确率与决策延迟间取得有效平衡。

## 1. 引言

自然语音对话必须无缝处理连续讲话、附和和用户打断，并保持低延迟。细粒度轮次状态是实时控制的基础：决定何时停止 TTS、何时取得话轮，以及何时忽略附和。

现有方法分为端到端与级联两类。端到端全双工模型联合学习语音理解、交互时机和回答生成，例如 Moshi 同时生成双方文本与音频 token；但在有限的全双工数据上联合优化所有组件，可能限制对话主干的规模和通用能力。

级联方法把交互控制与回答生成分离。典型 VAD→ASR→轮次检测链路先切分语音、再转写、最后根据文本判断状态，因此产生顺序延迟和误差传播。EasyTurn、JAL-Turn、FastTurn 和 SoulX-Duplug 做了更紧密的声学—语义融合，但大多仍工作在整句或音频块级别，或在推理时依赖外部 ASR。

Voxtral Realtime 基于延迟流建模，以固定 80ms 帧率同步输出转写 token。X2-Turn 在其 ASR Head 旁增加 Turn Head，二者共享因果 decoder 表示。为对齐任务，作者提出 ASR 锚定监督：把词级轮次标签投影到对应 ASR token 的帧位置。

贡献有三点：在预训练延迟流 ASR 上添加平行 Turn Head；设计五类轮次状态并把词级标签对齐到 ASR 的 80ms 时间线；在 EasyTurn 与 Full-Duplex-Bench 上验证不同目标延迟 τ 下的权衡。

## 2. 方法

### 2.1 双头建模

Voxtral Realtime 包含：把 16kHz 波形映射为帧级特征的因果音频编码器、降采样到 12.5Hz 的时间适配器，以及每 80ms 输出一个 token 的 decoder-only 语言模型。

在第 i 步，decoder 输入当前音频嵌入与上一 ASR token 的文本嵌入之和，产生共享隐藏状态 hᵢ。ASR Head 从 hᵢ 预测下一个转写 token：

`L_asr = -Σ log P_asr(yᵢ_asr | x_≤i, y_<i_asr)`

ASR 词表除普通 subword 外还有填充符 `[P]` 和词边界符 `[W]`。输出相对音频延迟可配置的 τ；τ 通过 AdaRMSNorm 注入 decoder，使同一模型支持多个 80ms 倍数的延迟。

Turn Head 与 ASR Head 平行，都读取 hᵢ：

`L_turn = -Σ log P_turn(yᵢ_turn | x_≤i, y_<i_asr)`

`L = L_asr + λL_turn`

推理时，自回归解码仅由 ASR Head 驱动。Turn Head 独立从 hᵢ 预测状态，结果不反馈进解码循环，因此 Turn 错误不会进一步污染 ASR；两类输出仍在同一次前向中产生。

### 2.2 轮次状态 token

训练定义五种状态：`idle`（静音）、`noidle`（已有语音但尚无足够语义）、`incomplete`（语义未完成）、`complete`（语义完整）、`backchannel`（附和或填充词）。其中 noidle 不代表背景噪声。

### 2.3 ASR 锚定监督

每个词表示为 `[W]` 加一个或多个 subword。设词起始时间为 sᵢ，帧宽 Δ=80ms，目标延迟帧数 nτ=τ/Δ，则 `[W]` 位置为 `pᵢ = round(sᵢ/Δ) + nτ`。

原 Voxtral 把 `[W]` 放在词结束处；本文改为词起始处，再紧接 subword，其余位置填 `[P]`。作者使用强 LLM 给每个词标注状态，并把标签赋给 `[W]` 及其 subword。未占用位置，包括句中停顿，都标为 idle。状态因此与 ASR token 使用同一表示；complete 后连续 idle 的数量可供下游做端点检测。

## 3. 实验设置

第一阶段 ASR 数据约 2.6 万小时：中文 1.4 万、英文 1.2 万小时。第二阶段轮次数据包括约 126 小时中文 EasyTurn 和 249 小时英文 Fisher。Qwen3-ForceAligner 生成词级时间戳，Qwen3.5-Plus 生成词级轮次标签。

主干为 Voxtral-Mini-4B-Realtime，完整微调因果音频编码器和语言 decoder。第一阶段适配延迟流 ASR；第二阶段加入 Turn Head 联合微调。Turn Head 由 ASR Head 副本初始化，λ=0.1。两阶段均在 80–2400ms 范围按 batch 采样 τ。

对时间区间 `[sᵢ,eᵢ]` 的词，相对词结束的决策延迟为 `Lᵢ = τ - (eᵢ-sᵢ)`。若词长大于 τ，状态可在词说完前产生。该指标与级联系统的推理时间加 VAD 延迟并不严格相同。

## 4. 结果与分析

完整系统由 X2-Turn、Qwen2.5-7B-Instruct 和 Qwen3-TTS-Streaming 级联。X2-Turn 在中英文 Pause TOR 上均最低；中文 Backchannel RsR 最高，英文仅次于 Gemini Live；打断 RpR 在两种语言均最高。整体准确率英语 0.860、中文 0.975，延迟分别为 0.769s 和 0.903s。

系统不是看到 complete 就立刻说话，而是要求其后出现一小段连续 idle。这减少停顿中的误接话，但增加少量延迟。

### EasyTurn 模块结果（τ=480ms）

| 语言/方法 | 完整 | 未完成 | 附和 | 延迟 |
|---|---:|---:|---:|---:|
| 中文 SoulX-Duplug | 89.33 | 79.33 | — | 295ms |
| 中文 X2-Turn | 91.00 | 93.00 | 96.00 | 288ms |
| 英文 SoulX-Duplug | 77.67 | 88.96 | — | 205ms |
| 英文 X2-Turn | 92.10 | 84.60 | — | 225ms |

X2-Turn 不需要辅助 ASR。级联方案因看到完整 VAD 片段可能更准，但其推理时间没有完整包含前端等待。

### 起点/终点锚定与 τ

中文起点锚定、τ=480ms 时平均准确率 93.25%、平均延迟 288ms；英文为 88.49%、225ms，整体优于终点锚定。

| 语言 | τ | 完整 | 未完成 | 平均 | 延迟 |
|---|---:|---:|---:|---:|---:|
| 中文 | 480 | 91.00 | 93.00 | 92.00 | 288ms |
| 中文 | 320 | 87.33 | 94.00 | 90.67 | 128ms |
| 英文 | 480 | 92.10 | 84.60 | 88.49 | 225ms |
| 英文 | 320 | 82.70 | 87.60 | 85.09 | 65ms |

减小 τ 显著降低延迟，但准确率有所下降，且不同类别方向不同。

### 流式 ASR

第一阶段 ASR 多数测试集优于 Uni-ASR 和 Freeze-Omni。加入轮次联合训练后，部分 WER 变差：AISHELL-1 从 2.57% 升至 3.94%，AISHELL-4 从 18.72% 升至 22.79%，WenetSpeech Meeting 从 9.25% 升至 12.18%。这显示多任务优化存在可见干扰。

## 5. 结论

X2-Turn 是对预训练延迟流 ASR 的帧同步双头扩展。Turn Head 与 ASR Head 共享因果 decoder 表示，ASR 锚定监督把词级状态投影到原生 80ms token 时间线。τ 控制轮次准确率、响应延迟与 ASR 质量之间的权衡。未来工作将继续平衡两个目标，并提高困难对话环境下的鲁棒性。

## 参考文献

原论文引用 33 项工作，完整书目信息保留在同目录 `paper.pdf` 与 `paper.html` 中。
