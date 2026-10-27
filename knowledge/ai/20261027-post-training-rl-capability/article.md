# Post-Training 变革（中）：RL 到底学会了新能力，还是只把已有能力“压”进 pass@1？

- 作者/公众号：Jason的算法日志
- 发布日期：2026-08-23 21:12
- 发布地点：北京
- 来源：https://mp.weixin.qq.com/s/sgrJ_S9NBh_A_9rB-7xvPA?mpshare=1&scene=1&srcid=1002hGtmRRuxpxyrIUnDRvaV&sharer_shareinfo=b142a00b7effd0a9da1b6a53fd03e045&sharer_shareinfo_first=b142a00b7effd0a9da1b6a53fd03e045&version=5.0.12.95037&platform=mac#rd
- 获取方式：2026-10-27 通过浏览器无障碍文本快照提取并结构化保存
- 提取限制：第二节的一处公式未被文本层提取；文中〔1〕—〔7〕脚注未在页面文本层展开。

## 导语

2026 年 post-training 的争论焦点已从“是否做 RL”转向四个问题：RL 应从怎样的 SFT policy 出发、RLVR 是否创造新能力、蒸馏与 RL 谁决定小模型上限，以及如何把单次成功实验变为可持续训练系统。

## 一、2026 年的共同答案：SFT、RL、蒸馏已经合并成一个循环

早期 post-training 是顺序流水线：预训练模型先做 SFT，再交给 RLHF，最后进行安全对齐和评测。现在更常见的是循环结构：模型生成多个候选，reward 选择更好的轨迹，再把成功经验固化回模型。Rejection Sampling、ReST 和 STaR 是这一思路的早期形式；reasoning model 把循环扩展到更长的 CoT、更复杂的工具调用和持续更新的环境。

文章以两条路线为例：

- Qwen3：长 CoT 冷启动 → reasoning RL → 思考/非思考模式融合 → 通用领域 RL。
- DeepSeek-R1：少量冷启动 → 可验证 RL → rejection sampling → 通用 RL。

作者归纳出的共同分工：

- SFT 让模型进入“可以探索”的状态。
- RL 改变高奖励轨迹的出现概率，并在环境中发现策略。
- 蒸馏把强教师、多条成功路径和不同 reasoning effort 压回可部署模型。

任何单项无限扩张都会遇到上限：SFT 太重会使策略熵消失；RL 缺乏好环境会退化成刷 verifier；完全离线的蒸馏会让学生模仿它自身无法访问的教师状态。

## 二、第一非共识：RL 前的 SFT 到底应该多重

“RL 前的 SFT 不要太重”源于真实问题：若为了 benchmark 把输出压成固定模式，RL rollout 会缺乏探索空间。但“数据越少、epoch 越少越好”同样不成立；一个连格式、工具调用和最低任务能力都不稳定的 policy，也难以只靠稀疏 reward 学会全部能力。

作者把目标定义为在“可用性”和“可探索性”之间平衡。原文此处含一个公式，但公式变量未被浏览器文本层完整提取；正文解释其中涉及 policy entropy 和进入环境所需的最低协议通过率。

文章引用《Quagmires in SFT-RL Post-Training》支持以下判断：SFT 阶段得分更高，并不保证后续 RL 更好；部分情况下，从更强 SFT checkpoint 出发的 RL 结果反而更差。held-out reasoning generalization 与大 k 下的 pass@k，可能比当前 SFT 榜单分更能预测后续 RL 潜力。

选择 RL checkpoint 时，文章建议同时监控：

1. pass@1：当前可用性。
2. pass@k：潜在能力边界。
3. rollout entropy：路径是否过度收缩。
4. format/tool pass rate：能否稳定进入环境。
5. held-out generalization loss：是否在记忆训练分布。

作者的总结是：“轻 SFT”的本质不是训练量少，而是保留 RL 可以利用的能力分布。

## 三、第二非共识：RLVR 创造新能力，还是重排已有能力

文章并列两类证据。

第一类研究认为 RLVR 主要进行 capability elicitation：把 base model 中已经存在、但概率很低的正确轨迹推向 pass@1。被引用的一项 NeurIPS 2025 研究观察到，RL 模型在小 k 时更强；当增加 base model 的采样次数时，base 的 pass@k 可以接近甚至超过 RL 模型。因此 RL 可能主要是在重分配概率，同时缩窄 reasoning boundary。

第二类研究认为 pass@k 不能充分定义能力边界，因为最终答案碰巧正确不代表推理路径正确。使用同时检查 reasoning path 和最终答案的 CoT-Pass@k 后，有研究发现 RLVR 能提高正确推理的泛化；文章还引用 ACL 2026 的视觉迷宫研究，称 RLVR 解决了 base policy 在高采样预算下仍为 0% 的问题，并迁移到真实导航任务。

| 判断 | 支持证据 | 可能的边界 |
|------|----------|------------|
| RL 主要做能力 elicitation | base 在大 pass@k 下已含成功轨迹；RL 后分布变窄 | pass@k 可能把错误 CoT 得到的正确答案误算作能力 |
| RL 可以带来 capability gain | CoT-Pass@k 提升；部分受控任务突破 base 可达边界 | 取决于 base competence、任务结构和 verifier 质量 |

作者给出的工程判据是：不能用单一指标裁决。如果 RL 后 pass@1 上升而 pass@k 下降，可能只是在压缩已有能力；如果 held-out task、CoT 正确性和可解决的环境难度同时提高，才更像真正的 capability expansion。

文章还强调 base model 的能力门槛：引用的因果推理实验显示，RLVR 的泛化收益只在模型已有足够初始能力时出现。base 太弱时，RL 没有可放大的正确轨迹。这也解释了小模型为何常常蒸馏优于直接 RL：问题不一定是 RL 理论无效，而是学生自身探索不到足够高质量的状态。

