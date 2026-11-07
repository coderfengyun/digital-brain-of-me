---
title: "Critical thinking when agents do the work / 当智能体替你工作时，如何保持批判性思考"
author: "Addy Osmani"
source: "https://x.com/addyosmani/status/2117512471930167377"
published: "2026-11-03"
retrieved: "2026-11-07"
language: "en-zh"
translation: "AI-assisted Chinese translation"
---

# Critical thinking when agents do the work

> # 当智能体替你工作时，如何保持批判性思考

Back in the day, critical thinking was taught as approaching new info with humble curiosity and a healthy dose of skepticism - take in different views, form your own opinion. Still true, but **increasingly, nothing in my day-to-day forces critical thinking on me now that so much of my work runs through agents**. For the engineers and product people who have fully bought into agentic workflows (running multiple sessions in parallel and expecting the models to improve), I'm here to say: I'm a big fan of these tools. I'm not writing this to advocate for less agentic workflows.

> 过去，人们教导我们：面对新信息时，要怀着谦逊的好奇心，同时保持适度的怀疑——听取不同观点，再形成自己的判断。这一点依然正确。但**随着越来越多工作交给智能体处理，我的日常工作中已经很少有事情会迫使我进行批判性思考**。对于那些已经全面拥抱智能体工作流的工程师和产品人员——同时运行多个会话，并期待模型持续改进——我想先说明：我非常喜欢这些工具。写这篇文章，并不是为了呼吁大家减少使用智能体工作流。

My goal is to help you maintain critical thinking in a world where it's easy to offload anything to an agent.

> 我的目标，是帮助你在一个几乎任何事情都可以卸载给智能体的世界里，依然保持批判性思考。

In the past, most of our cognitive and aesthetic processing happened in the space between question and answer. That space is now measured in seconds. The more you use agentic workflows, the more difficult it becomes (though not in the way I think people expected): as the models improve, the percentage of obvious errors is lower. Many (most?) outputs will be well-written and mostly correct, but they won't demand a second look.

> 过去，我们大部分的认知加工和审美判断，都发生在提出问题与得到答案之间。如今，这段间隔已经缩短到以秒计算。智能体工作流用得越多，保持思考反而越困难——但困难的方式可能与人们预想的不同：随着模型变得更好，明显错误所占的比例越来越低。许多（甚至大多数？）输出写得很好，也基本正确，因此不会自然地促使你再看一遍。

Even if you are running many agents at a time, you still only have one pair of eyes on the outputs.

> 即使你同时运行许多个智能体，审视所有输出的仍然只有你这一双眼睛。

**You have to build critical thinking into your day, because by default nothing will do it for you.**

> **你必须主动把批判性思考嵌入日常工作，因为在默认情况下，没有任何机制会替你这样做。**

Part of the reason it's hard to self-correct for this is that agentic workflows are pleasant. Getting fast, pleasant, often-correct answers is refreshing in a busy day, but that's also why it's easy to relax your vigilance.

> 这种问题之所以很难靠自我纠正来解决，部分原因在于智能体工作流的体验实在太舒服了。在忙碌的一天里，快速、顺畅而且通常正确的答案让人如释重负；但也正因如此，你很容易放松警惕。

## Offloading, deferral and surrender

> ## 认知卸载、延后判断与认知投降

When discussing this with people, I describe it as a spectrum:

> 和别人讨论这个问题时，我通常把它描述成一条连续光谱：

At the top: cognitive offloading, the act of delegating tasks to the AI, but maintaining ownership of the result. I do this all day. You should, too. In the middle: deferral, where the output of the tool becomes your new input; the result has ceased to be a hypothesis. At the bottom: [cognitive surrender](https://addyosmani.com/blog/cognitive-surrender/) - the AI's output quietly becomes your own, you feel no need to check it.

> 光谱的上端是“认知卸载”：把任务交给 AI，但仍然对结果保有所有权。我整天都在这么做，你也应该这么做。中间是“延后判断”：工具的输出直接成为你的新输入，结果不再被视为一个有待验证的假设。最下端则是[认知投降](https://addyosmani.com/blog/cognitive-surrender/)——AI 的输出悄无声息地变成了你的观点，而你不再觉得有必要检查它。

Cognitive surrender is a term coined by [Steven Shaw and Gideon Nave](https://ssrn.com/abstract_id=6097646) at Wharton. It fits neatly what I've been seeing: as trust (or laziness) increases, people drift down the spectrum. The transition is rarely observed, because the steps are each gradual and seem reasonable. You read the last answer well, so you skim the next one. You just scan the skeleton of the one after that. Then you get asked about a line and can't explain it, even with your agent's help.

> “认知投降”一词由沃顿商学院的 [Steven Shaw 和 Gideon Nave](https://ssrn.com/abstract_id=6097646) 提出。它恰好概括了我观察到的现象：随着信任增加（或者人变得更懒），人们会沿着这条光谱逐渐下滑。这个转变很少被察觉，因为每一步都很细微，而且看起来合情合理。你认真读了上一个答案，于是下一个答案只略读一下；再下一个只扫一眼骨架。后来有人问起其中某一行，你却发现自己解释不了，即使让智能体帮忙也说不清。

That's cognitive surrender. It's how cognitive debt accumulates. It's usually discovered when you try to apply a mental model of the system and it doesn't exist. [Margaret-Anne Storey](https://margaretstorey.com/blog/2026/02/09/cognitive-debt/) has written about how this shows up in teams as an eroding understanding of a shared system theory. I've written about the code equivalent, [comprehension debt](https://addyosmani.com/blog/comprehension-debt/) (a term coined by Jeremy Twei). In the moment, it's completely invisible. The codebase looks pristine and the tests pass. It doesn't become obvious until you have to make a change to the system and realize that nobody understands it anymore. The same applies when you've read the table of contents of a strategy doc or spec and signed off on it.

> 这就是认知投降，也是认知债务积累的方式。通常，直到你试图运用自己对系统的心智模型，却发现这个模型根本不存在时，问题才会暴露。[Margaret-Anne Storey](https://margaretstorey.com/blog/2026/02/09/cognitive-debt/) 写过这种现象如何在团队中表现为：大家对共享系统理论的理解逐渐流失。我也写过它在代码领域的对应物——[理解债务](https://addyosmani.com/blog/comprehension-debt/)（这个词由 Jeremy Twei 提出）。在债务形成的当下，它完全不可见：代码库看上去干干净净，测试全部通过。直到你必须修改系统，才突然意识到已经没人真正理解它了。同样的事情也会发生在你只读了一份战略文档或规格说明的目录，就签字批准的时候。

To be clear, I'm not advocating for the impossible. It's impossible to maintain the full mental model of a large modern codebase. [The Claude Code team has said publicly](https://claude.dev/blog/solving-code-review-at-anthropic/) that they rebuild understanding on demand: when they need to understand a part, they ask Claude to explain that slice, rather than holding the full model in their heads. As I've [written about before](https://addyosmani.com/blog/intent-debt/), this sort of debt is more recoverable than most engineers expect. You don't need to maintain the full model as long as you can rebuild it locally as needed. You just need to know what you don't have.

> 需要说明的是，我并不是在倡导不可能做到的事。要在脑中维持一个大型现代代码库的完整心智模型，本来就不现实。[Claude Code 团队曾公开表示](https://claude.dev/blog/solving-code-review-at-anthropic/)，他们会按需重建理解：当需要弄懂某一部分时，就让 Claude 解释那一小块，而不是把完整模型一直装在脑子里。正如我[此前写过的](https://addyosmani.com/blog/intent-debt/)，这种债务比多数工程师想象的更容易修复。你不必始终保有完整模型，只要能在需要时局部重建即可。关键是，你必须知道自己缺少什么。

**Where the stakes are low, feel free to delegate entirely. When you can't explain the answer to a question, even by way of your agent, you've ceded ownership.**

> **风险很低时，完全可以把事情全部委托出去。但当你无法解释一个问题的答案——哪怕借助智能体也解释不了——你就已经放弃了对结果的所有权。**

This isn't always a problem, either. Just recently, I was recording a course and had to select one out of three similarly-rated hotels to use as a recording location. I didn't have time to manually review all the reviews, so I delegated the decision to an AI. It worked, and I'd do the same thing again. However, I wouldn't do that when deciding how to invest our money, how to advise our kids on their careers, or at work: what we should build, what changes affect what users, whether it's safe to ship. Take the handoff where being wrong is cheap, keep the reasoning where others will have to deal with the consequences.

> 当然，这并不总是一个问题。不久前，我录制一门课程，需要从三家评分相近的酒店中选一家作为拍摄地点。我没时间逐条查看所有评论，于是把这个决定交给了 AI。结果很好，下次我还会这么做。但如果是决定如何投资我们的钱、怎样给孩子的职业发展提建议，或者在工作中判断该做什么、某项改动会影响哪些用户、是否可以安全发布，我就不会这样做。在犯错成本很低的地方完成交接；在后果需要由别人承担的地方，把推理权留在自己手里。

## The questions I ask myself

> ## 我会问自己的问题

When I didn't know what I thought, I'd usually go back to a basic list of questions like these: How do I know that I'm working on the right problem? How do I know that I'm solving it the right way? Is there evidence that supports my conclusion? How do I know that I'm finished? Most times, this is just [who, what, where, why, when and how](https://addyo.substack.com/p/critical-thinking-during-the-age). When written out, it looks absurdly child-like, but it forces you to think in terms of categories that you'd otherwise ignore. These days, it's too easy to simply skip all of this and ask your agent what it thinks you should do. These are the new versions of these questions that I ask myself now.

> 当我不清楚自己究竟怎么想时，通常会回到一组基本问题：我怎么知道自己处理的是正确的问题？我怎么知道解决方式是对的？有没有证据支持我的结论？我怎么知道工作已经完成？多数时候，这无非就是[谁、什么、哪里、为什么、何时、如何](https://addyo.substack.com/p/critical-thinking-during-the-age)。写出来看似幼稚得可笑，却会迫使你思考那些原本可能忽略的类别。如今，人们太容易跳过整个过程，直接问智能体“你觉得我该怎么做”。下面是我现在会问自己的新版本问题。

**Did I formulate a hypothesis before asking?** Before I run an agent on any non-trivial task, I write down, even just in my head, what I think the answer might be. It's OK if it's a bad guess. You're always welcome to change your mind in light of new information. Once you've read a well-written response, though, it's hard to imagine any other possibility. If you have no guidance whatsoever, ask for what Thariq Shihipar calls a [blind spot pass](https://claude.com/blog/a-field-guide-to-claude-fable-finding-your-unknowns): give the model what you know and have it find your unknown unknowns.

> **我在提问前形成假设了吗？** 在让智能体处理任何非琐碎任务之前，我都会先写下——哪怕只是在脑中想一下——我认为答案可能是什么。猜错也没关系；面对新信息，你随时可以改变想法。但一旦读过一份文笔流畅的回答，就很难再想象其他可能性。如果你完全没有方向，可以请模型做一次 Thariq Shihipar 所说的[“盲点扫描”](https://claude.com/blog/a-field-guide-to-claude-fable-finding-your-unknowns)：把你已知的内容告诉模型，让它寻找那些你不知道自己不知道的东西。

**Am I asking it to help me think or to offload thinking from me?** Both are OK, as long as you know which one you're doing.

> **我是在请它帮助我思考，还是把思考本身卸载给它？** 两种做法都可以，只要你清楚自己正在做哪一种。

**What would have to be true for this to be wrong?** Then go find out. A model's self-assessment of confidence is much less valuable than an actual test you can perform, so give it one.

> **要满足什么条件，这个结论才会是错的？** 然后去查明这些条件是否成立。模型对自身信心的评估，远不如一项你能真正执行的测试有价值，所以给它一个可执行的测试。

**Have I heard the counter argument from a different angle?** When I've taken a hard stance on something that's somewhat open-ended, I'll ask more than one model to argue the opposite side, then review the output and form my own opinion. This takes longer, but I end up knowing much more about the subject.

> **我是否从不同角度听过反方论证？** 当我对某个开放性问题持有强烈立场时，会请多个模型分别站到对立面进行论证，然后审阅它们的输出，再形成自己的看法。这会花更多时间，但最终我对这个主题的理解也会深得多。

**Would I bet on this in front of the person who has to maintain it?** This applies to code and to anything else that you're delivering. I believe that this is the bar for answerability.

> **我敢在未来负责维护它的人面前为这个结论下注吗？** 这既适用于代码，也适用于你交付的任何东西。我认为，这就是“能够为答案负责”的门槛。

**What am I no longer practicing?** Maybe it's some of the routine debugging. I'm OK with letting some of that go, but I want it to be intentional.

> **有哪些能力是我已经不再练习的？** 也许是某些日常调试工作。我可以接受放下一部分，但希望这是一个有意识的决定。

## Verification as a habit

> ## 把验证变成习惯

I've been writing a lot about verification lately because I believe that [the bottleneck has shifted from coding to being sure you're right](https://addyo.substack.com/p/agentic-verification). When you give an agent the means to verify what it's doing, whether that be by way of end-to-end tests, property tests, or by way of actual app interactions, it can make a change, run the verification test, read the output, and attempt again all before you've looked at anything. This is what Boris Cherny calls ["give Claude a way to verify its work"](https://x.com/bcherny/status/2007179861115511237) and I believe that this is one of the most critical components of achieving great results. Rather than reading every line, you'll be building these loops and reviewing the evidence.

> 最近我写了很多关于验证的内容，因为我相信，[瓶颈已经从“写出代码”转移到“确认自己是对的”](https://addyo.substack.com/p/agentic-verification)。如果你为智能体提供验证自身工作的手段——无论是端到端测试、性质测试，还是让它实际操作应用——它就能在你看任何东西之前，完成修改、运行验证、读取结果并再次尝试的整个循环。这就是 Boris Cherny 所说的[“给 Claude 一种验证自己工作的方式”](https://x.com/bcherny/status/2007179861115511237)。我认为，这是取得出色结果最关键的组成部分之一。你不再需要逐行阅读，而是构建这些闭环，并审查其中的证据。

You can also surrender verification. "Is there evidence that supports my conclusion?" becomes "Did the check turn green?" Agents make it so cheap to create tests that you'll see a lot of green, and you could have a passing test that doesn't catch a broken feature. If the test is written with the same mistake as the feature, it'll pass. And a green check only conveys one property. It's too easy to imagine it covers everything.

> 但你同样可能在验证环节发生认知投降。“有没有证据支持我的结论？”会退化成“检查项变绿了吗？”智能体让编写测试的成本低到几乎可以忽略，于是你会看到大量绿色结果；然而，一个通过的测试完全可能没有捕捉到已经损坏的功能。如果测试和功能犯了同一个错误，它照样会通过。而一个绿色勾号只证明了一项属性，人们却很容易想象它已经覆盖了一切。

**When a check goes green, ask what it proved. Then ask what it didn't.**

> **当检查项变绿时，先问它证明了什么，再问它没有证明什么。**

Define "verified" upfront, because post-facto, you'll rationalize any outcome.

> 预先定义“已验证”的含义，因为事后你总能为任何结果找到合理化解释。

The finish line for agent work should be something tangible: a test passing, a screenshot, a log or trace. This ensures that the criteria for finishing the work is factual, and not up for interpretation (and surrender) based on something like "it looks like it's done." When you receive a finish notification from an agent, before you look at the summary, first review the code snippet of the command executed and its output.

> 智能体工作的终点应当是某种有形证据：一项通过的测试、一张截图、一段日志或一次追踪记录。这样，完成标准就是事实性的，而不是根据“看起来已经完成了”之类的印象任意解释——甚至发生认知投降。当你收到智能体的完成通知时，在阅读摘要之前，先检查它实际执行的命令片段及其输出。

Claude Code can also self-critique (via a subagent in a fresh context) its own work as a sanity check, and it's worth baking that into the loop so it runs every time, not just when you remember. I still ask at the end "Did I miss anything?" That sounds silly, but so often, when I finish some complex feature work using a frontier model, look at it, review it, and then ask, "Did I miss anything?" It will then come back with two or three more things. That's why I always ask.

> Claude Code 还可以通过一个处在全新上下文中的子智能体，对自己的工作进行自我批评，作为合理性检查。值得把它固化进流程，让它每次都运行，而不是只在你偶尔想起来时才做。结束时，我仍然会问一句：“我漏掉什么了吗？”听起来有些傻，但很多时候，我用前沿模型完成了一项复杂功能，查看并审查之后，再问“我漏掉什么了吗？”，它往往还会补充两三项问题。这就是我每次都问的原因。

None of this needs to be the norm, of course; knowing when to go deep is a skill. My favorite rule of thumb from our [write-up on how the Claude Code team does code review](https://claude.dev/blog/solving-code-review-at-anthropic/) is: "If you can't say what the checks would miss, ask for a real review rather than a quick approval."

> 当然，并不是每件事都需要如此严格；知道什么时候该深入，本身也是一种能力。我们在[介绍 Claude Code 团队如何进行代码审查的文章](https://claude.dev/blog/solving-code-review-at-anthropic/)里给出了一条我很喜欢的经验法则：“如果你说不出这些检查会漏掉什么，就应该要求一次真正的审查，而不是快速批准。”

This applies beyond code as well. If an agent has synthesized fifty customer calls for you, or a competitive analysis, check a couple of the source documents to make sure the summary is accurate. Check a number that your recommendation depends on to make sure it's being calculated correctly.

> 这同样适用于代码之外的工作。如果智能体替你综合了 50 通客户电话，或者完成了一份竞品分析，就抽查几份原始材料，确认摘要是否准确。再检查一个你的建议所依赖的关键数字，确认它的计算确实正确。

**Agents have made verification cheap to set up. What's difficult for you is knowing what good verification looks like.**

> **智能体已经让搭建验证机制变得很便宜。真正困难的是，你是否知道“好的验证”究竟是什么样子。**

## Actually paying attention to what's generated

> ## 真正关注生成出来的内容

Say an agent gives you a 600-line PR. You roughly look at the structure. You don't read every line. The variable names look reasonable and the tests pass, so you approve it. But somewhere in the middle there's a subtle ordering change in a transaction boundary, or a flipped default on an edge case you never thought about. You did review it, I guess, but only for what you already knew you'd find.

> 假设智能体给了你一个 600 行的 PR。你大致看了结构，没有逐行阅读。变量名看起来合理，测试也通过了，于是你批准合并。但在中间某处，事务边界中的执行顺序发生了细微变化；或者在一个你从没想过的边缘情况下，默认值被反转了。你确实“审查”了它，但只检查了那些你本来就知道要找的东西。

Writing code and reviewing it are different skills, and [there's a point where reviewing turns into rubber stamping](https://addyo.substack.com/p/the-80-problem-in-agentic-coding). So read the diff as if the AI didn't write it, and then look past the diff at what the agent decided. Over a long session it makes a lot of small decisions for you: the defaults, what's out of scope, which requirement it reinterprets when two of them clash.

> 写代码和审代码是两种不同的能力，而且[审查总有一个临界点，会退化为机械盖章](https://addyo.substack.com/p/the-80-problem-in-agentic-coding)。因此，阅读 diff 时要假设它并不是 AI 写的；然后再越过 diff 本身，观察智能体替你做了哪些决定。在一次长会话中，它会替你完成许多小决策：默认值是什么、哪些内容不在范围内、两项需求冲突时重新解释哪一项。

You won't see any of that in a summary that says everything went well, so ask it to list the decisions and assumptions it made. Then quiz yourself. Pick a few lines at random and ask, what about this line? What about that one? For a document, close it and try to write out the main argument from memory. Some have a habit I like for long sessions: have Claude write a report on the change, and then give you a quiz at the bottom, where the rule is ["I only merge after I pass the quiz perfectly."](https://claude.com/blog/a-field-guide-to-claude-fable-finding-your-unknowns)

> 在一份“一切顺利”的摘要中，你看不到这些决定。因此，要让智能体列出它做过的决定和采用的假设，然后考考自己。随机挑几行，问自己：“这一行是什么意思？那一行又为什么存在？”如果交付物是一份文档，就把它关掉，尝试凭记忆写出核心论点。有些人在长会话中采用一个我很喜欢的习惯：让 Claude 写一份变更报告，并在底部出一份测验，规则是：[“只有满分通过测验，我才会合并。”](https://claude.com/blog/a-field-guide-to-claude-fable-finding-your-unknowns)

**Understand what you're shipping well enough to defend it. Because at some point, someone could ask.**

> **你必须充分理解自己正在交付的东西，达到能够为它辩护的程度。因为总有一天，会有人问起。**

Agents can also guard your attention. For example, I have an open source project that receives a lot of pull requests. I'll use agents to help determine what's incoming, what's contrary to our guidelines, and where my attention is likely required. I rarely let the agents self-determine this, but they can narrow it down to where I should focus my attention, and then I can actually think about whether these changes are solving the right problem in the right way.

> 智能体也可以替你守护注意力。例如，我有一个开源项目，每天会收到很多拉取请求。我会让智能体帮助判断新提交的内容是什么、哪些违背了项目规范、哪些地方可能需要我亲自关注。我很少让智能体独自作出最终判断，但它们可以缩小范围，告诉我应该把注意力放在哪里。这样，我才能真正思考这些改动是否在用正确的方式解决正确的问题。

Then there's volume, and you have to be honest with yourself about it. I've called this [the orchestration tax](https://addyosmani.com/blog/orchestration-tax/). It's the gap between what your agents generate and what you'd feel comfortable putting your name on. If finished work is piling up faster than you can get through it, another session won't help until you've fixed that: tighten the checks so less of it needs you, or slow down.

> 接下来是产出规模问题，你必须对此诚实面对。我把它称为[编排税](https://addyosmani.com/blog/orchestration-tax/)：智能体生成的内容，与那些你愿意署上自己名字的内容之间，存在一道差距。如果已完成的工作堆积速度超过你的审查速度，那么在解决这个问题之前，再开一个会话也没有用。你要么收紧检查机制，让需要人工处理的内容更少；要么降低速度。

**When you're producing more than you can stand behind, you're no longer reviewing. You're hoping.**

> **当你的产出已经多到无法逐一为之负责时，你做的就不再是审查，而是在碰运气。**

## Quality in, quality out

> ## 高质量输入，高质量输出

The human mental model is still involved, but instead of in the middle, it's at the front and end. You're putting your energy into the front-end of the task description and context, as well as the back-end of reviewing the output. This is why good input is so important to the quality of output, and I view good prompting as a critical thinking skill.

> 人类的心智模型仍然参与其中，只是不再位于过程中央，而是被移动到了前端和后端。你需要把精力放在前端的任务描述与上下文准备上，以及后端的输出审查上。这就是为什么高质量输入对输出质量如此重要，也是为什么我把好的提示词写作视为一种批判性思考能力。

Historically, if you made a non-specific request, someone would challenge it, and you might realize, "Oh wait, I actually didn't figure this out." An agent often won't stop you there. It fills in what you left out and hands back something that looks done, even though the idea behind it is still fuzzy. I've written about this as [intent debt](https://oreillyradar.substack.com/p/the-intent-debt), the implicit goals, constraints and rationale that may exist in artifacts you didn't write. Unlike other kinds of debt, nobody else can fix this one for you. The intent has to come from you.

> 过去，如果你提出一个含糊的请求，别人往往会质疑它，而你可能突然意识到：“等等，我其实还没把这件事想清楚。”智能体通常不会在这里叫停。它会自动补全你遗漏的部分，然后交回一个看似完成的结果，即使背后的想法仍然模糊。我把这种现象称为[意图债务](https://oreillyradar.substack.com/p/the-intent-debt)：在那些并非由你亲自编写的产物中，潜藏着隐含的目标、约束和理由。与其他债务不同，没有人能替你偿还这种债务。意图只能来自你自己。

**Your prompt is a reflection of your understanding of the problem, and if you can't express it clearly, it may not be clear in your own mind.**

> **你的提示词反映了你对问题的理解。如果你无法清楚表达，问题本身在你脑中可能也并不清楚。**

Write your own request brief in your own words before you ask for help. Describe the audience, out-of-scope items, and the definition of done. When your second round of corrections hasn't got you there, stop tweaking and rewrite your prompt.

> 在寻求帮助之前，先用自己的语言写一份需求简报。说明受众、不在范围内的事项，以及完成标准。如果第二轮修改仍然没有达到目标，就不要继续小修小补，而应重写提示词。

You can have the agent help you with this too. I like the distinction Andy Clark makes between delegating to an AI system and [collaborating](https://pubmed.ncbi.nlm.nih.gov/40389440/) with it. In the latter case, you're in a virtuous cycle of mutual amplification: your prompts sharpen your output, sharpen your next prompt and sharpen your mental model of the problem. If it's not clear, ask the agent to interview you about what it doesn't understand. If you close the session having refined your own mental model, that's a sign of success.

> 你也可以让智能体帮助你完成这一过程。我很喜欢 Andy Clark 对“把任务委托给 AI 系统”和“与 AI [协作](https://pubmed.ncbi.nlm.nih.gov/40389440/)”所作的区分。在后一种情况下，你进入了一个相互增强的正循环：提示词让输出更清晰，输出又让下一轮提示词和你对问题的心智模型更清晰。如果还有不明确的地方，就让智能体针对它不理解的部分采访你。如果结束会话时，你自己的心智模型也变得更加精确，那就是成功的信号。

Also be careful about the input. It's easy for each agent to just pass the previous agent's summary into its context, and before long the third agent hasn't read the original document.

> 同时也要谨慎对待输入。每个智能体都很容易直接把上一个智能体的摘要传进自己的上下文；用不了多久，第三个智能体可能根本没有读过原始文档。

You also need your own standards for output. I've played around with AI in lots of different creative mediums, and most of it never gets shown because it doesn't meet my standards. Things are all coming out nicely formatted and confident, so polish is no longer a useful signal.

> 你还需要为输出建立自己的标准。我用 AI 尝试过很多不同的创作媒介，其中大多数成果从未展示给别人，因为它们没有达到我的标准。现在生成的内容通常排版精美、语气自信，因此“看起来很精致”已经不再是一个有用的质量信号。

**AI may have made it faster to produce, but if I wouldn't feel comfortable attributing the output to myself, I won't output it.**

> **AI 也许让生产速度更快，但如果我不愿意把自己的名字署在一份产出上，我就不会发布它。**

When something doesn't meet your standards, note why in shared config, a hook or a test so that it doesn't happen again. That's how [taste compounds](https://addyo.substack.com/p/agentic-verification), and noting why something didn't make the cut is good practice on its own.

> 当某项产出不符合标准时，把原因记录进共享配置、钩子或测试里，避免同样的问题再次发生。这就是[品味复利](https://addyo.substack.com/p/agentic-verification)的形成方式；而记录一项内容为什么没有入选，本身也是很好的练习。

## "But the models will be better at this than me"

> ## “但模型以后会比我更擅长这些事”

If you're as bullish on the future of this space as many people around me are, you've probably had this thought for a couple of sections. In a year or two, the model will be able to detect what I'd be able to detect, so why bother maintaining the skill?

> 如果你和我身边的许多人一样，看好这个领域的未来，那么读到前几节时，你可能已经产生了这样的想法：再过一两年，模型就能发现我现在能发现的问题，那我为什么还要费力维持这项能力？

You may be right on a lot of that detection, and I've been arguing for increasingly pushing detection to agents myself. But here's why I think it still matters: at the end of the day, someone is responsible for what ships. Regardless of how much AI helped, [a human has to take responsibility](https://addyo.substack.com/p/code-review-in-the-age-of-ai).

> 对许多检测任务来说，你可能是对的；我自己也一直主张把越来越多的检测工作交给智能体。但我仍然认为这些能力很重要，原因是：最终，总得有人对发布出去的东西负责。无论 AI 帮了多少忙，[责任仍然必须由人承担](https://addyo.substack.com/p/code-review-in-the-age-of-ai)。

The question of how much to trust an agent for any given task is itself a judgment call. Part of staying calibrated is reviewing the work, because what the models get wrong keeps changing. Anthropic's own research on its engineers and researchers [calls out the trap](https://www.anthropic.com/research/how-ai-is-transforming-work-at-anthropic) as the paradox of supervision: "supervising Claude requires the very coding skills that may atrophy from AI overuse."

> 对任何具体任务而言，应该在多大程度上信任智能体，本身就是一个需要判断的问题。保持校准的一部分，就是持续审查工作，因为模型容易出错的地方一直在变化。Anthropic 对内部工程师和研究人员的研究[指出了这个陷阱](https://www.anthropic.com/research/how-ai-is-transforming-work-at-anthropic)，并把它称为“监督悖论”：“监督 Claude，恰恰需要那些可能因过度使用 AI 而退化的编程能力。”

These are some of the things that matter most to me and that a better model won't solve: what are you building, why is it worth it, who does it impact and what are you willing to sacrifice? Those are all questions you need to answer. An agent can be helpful in working them through, and I would like it to be, but ultimately they're still yours.

> 下面这些问题对我最重要，而更好的模型也无法替你解决：你在构建什么？它为什么值得做？它会影响谁？你愿意为它牺牲什么？这些都必须由你回答。智能体可以帮助你梳理问题，我也希望它能提供帮助，但归根结底，这些问题仍然属于你。

**You may offload the work and much of the auditing, but not the accountability.**

> **你可以卸载工作，也可以卸载大部分审计，但不能卸载责任。**

## Practices for the everyday

> ## 日常实践

You don't need to do all this rigorously. Just plug in what works for your workflow.

> 你不必严丝合缝地执行所有做法，只需要把适合自己的部分嵌入工作流。

Once a week, write a bit of code without an agent, or do one real thing that would suck if you forgot how to do it. (I've [called this a calibration exercise](https://addyosmani.com/blog/cognitive-surrender/), but I don't mean it as a moral one.) Once a month, write down what you've stopped doing and decide which of those you're okay not doing. [One question from an old blog post of mine](https://addyo.substack.com/p/avoiding-skill-atrophy-in-the-age) remains as valid as ever: How lost would you be if AI didn't exist?

> 每周在没有智能体的情况下写一点代码，或者亲手做一件“一旦忘记怎么做就会很麻烦”的真实任务。（我把它[称为校准练习](https://addyosmani.com/blog/cognitive-surrender/)，但并不想赋予它道德含义。）每个月，写下自己已经停止亲自做的事情，并决定其中哪些能力可以接受不再保持。我在[一篇旧博客文章中提出的问题](https://addyo.substack.com/p/avoiding-skill-atrophy-in-the-age)仍然有效：如果 AI 不存在，你会有多不知所措？

If something is above your comprehension, go learn it. If I'm writing and I run into a phrase I haven't seen before, I could Google a one-line explanation and include it. I prefer to do a little research to properly understand it, so I can see where it fits.

> 如果遇到超出自己理解范围的内容，就去学习它。写作时碰到一个从未见过的短语，我当然可以 Google 一句解释，然后直接放进文章。但我更愿意做一点研究，真正弄懂它，从而知道它在整体知识结构中的位置。

Checking the machine properly is real work, and pretending otherwise is how teams end up not doing it. It isn't free, so schedule it as a line item and you'll actually get it done.

> 正确检查机器产出本身就是实实在在的工作。假装它不算工作，最终只会让团队根本不去做。检查不是免费的，所以应当把它作为明确的工作项排进计划，这样它才会真正完成。

**Skills that you stop exercising are going to go away, and probably faster than you might guess.** Keep doing the ones you're not willing to let go.

> **一项技能只要停止练习，就会逐渐消失，而且速度可能比你想象的更快。** 那些你不愿失去的能力，要继续亲自练习。

## What to bring with you

> ## 请记住这些原则

**Be intentional.** An agent can quiz you, interview you and show you its evidence, but only if you set that up. So set it up.

> **保持主动和有意识。** 智能体可以测验你、采访你、向你展示证据，但前提是你先把这些机制设置好。所以，去设置它们。

**Be honest about your place on the spectrum.** If you can't explain the answer, even with an agent's help, you've surrendered it.

> **诚实面对自己处在光谱的哪个位置。** 如果你无法解释答案，哪怕借助智能体也解释不了，那你已经对它发生了认知投降。

**Have a hypothesis.** Formulate one before asking, even if it's bad.

> **先有一个假设。** 提问前先形成自己的猜想，哪怕这个猜想很差。

**A green check means one thing.** What did it check? What did it not check?

> **一个绿色勾号只代表一件事。** 它检查了什么？又没有检查什么？

**Look for evidence.** Read what it ran and what it returned before reading the summary.

> **寻找证据。** 在阅读摘要前，先查看它实际运行了什么、返回了什么。

**Read to know what decisions it made.** What did it decide for you?

> **阅读是为了弄清它做过哪些决定。** 它替你决定了什么？

**Craft your prompt.** How you write what you prompt shows how much you understood the problem.

> **打磨你的提示词。** 你如何写提示词，反映了你在多大程度上理解问题。

**Set a bar, and stick to it.** If you wouldn't put your name on it, it doesn't go out.

> **设定标准，并坚持它。** 如果你不愿意署上自己的名字，就不要发布。

Keep yourself in the game by manually applying the skills that matter. One thing you could do: Before you ask, write down what you think will happen, and after the agent is done, write down one thing it didn't check. Let me know if that changes the way you read the output.

> 通过亲自运用那些重要的技能，让自己始终留在场上。你可以从一个简单做法开始：提问前，写下你认为会发生什么；智能体完成后，再写下一件它没有检查的事。看看这是否会改变你阅读输出的方式。

**Think independently. Ask better questions. Take responsibility for the outcome.**

> **独立思考。提出更好的问题。对结果负责。**
