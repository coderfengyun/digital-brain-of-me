# Skill 调用 Skill：Skills 的乐高式组合

> 来源：宝玉AI（微信公众号）
> 原文链接：https://mp.weixin.qq.com/s/uVMd9HNbWvQjOFOa5abPKw

写 Skill 的时候遇到一个问题：我的漫画生成 Skill 需要画图，但用户可能装了 Nano Banana Pro 的 Skill，也可能装了 Midjourney 的。我要在代码里写死调用哪个吗？

不用。这正是 Agent Skills 设计的精妙之处。

## 原理：启动即感知

Claude 调用 Skill 时会加载 SKILL.md、注入指令、修改执行环境。但更关键的是启动阶段——Agent 启动时就预加载了所有已安装 Skill 的名称和描述。

换句话说：Agent 一启动就知道自己有哪些能力。

## 实践：松耦合调用

我的漫画 Skill 里，画图环节是这样写的：

> Check available image generation skills. If multiple skills available, ask user preference.
> 检查可用的画图 Skill，如果有多个则提示用户选择

好处是解耦。我不依赖任何特定的画图实现，用户装了什么画图 Skill，Claude 就调用什么。

更妙的是 Claude 能动态适配目标 Skill 的能力：
- 支持参考图 → 传角色设计图
- 只支持文本 → 传文字描述

所以我只需要说："帮我画张图"，而不用："用 Nano Banana Pro 的 API 帮我画张图"。

## 为什么这样更好

这种松耦合带来几个实际好处：

1. 可替换：换画图引擎不用改上游 Skill
2. 可扩展：新画图 Skill 自动可被调用
3. 低维护：Skill 作者不用追踪下游依赖
4. 用户自主：用户选自己喜欢的工具

Skill 间相互调用是基于能力描述的松耦合。你只描述"需要什么能力"，Claude 在运行时自动匹配。

这让 Skills 成了真正的乐高积木——独立模块，自由组合，构建复杂工作流。
