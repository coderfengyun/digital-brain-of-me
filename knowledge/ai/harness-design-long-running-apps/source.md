# Harness design for long-running application development

> Source: Anthropic Engineering Blog | Published Mar 24, 2026
> Author: Prithvi Rajasekaran (Labs team)
> URL: https://www.anthropic.com/engineering/harness-design-long-running-apps

Harness design is key to performance at the frontier of agentic coding. Here's how we pushed Claude further in frontend design and long-running autonomous software engineering.

## Background

Over the past several months I've been working on two interconnected problems: getting Claude to produce high-quality frontend designs, and getting it to build complete applications without human intervention. This work originated with earlier efforts on our frontend design skill and long-running coding agent harness, where my colleagues and I were able to improve Claude's performance well above baseline through prompt engineering and harness design—but both eventually hit ceilings.

To break through, I sought out novel AI engineering approaches that held across two quite different domains, one defined by subjective taste, the other by verifiable correctness and usability. Taking inspiration from Generative Adversarial Networks (GANs), I designed a multi-agent structure with a **generator** and **evaluator** agent. Building an evaluator that graded outputs reliably—and with taste—meant first developing a set of criteria that could turn subjective judgments like "is this design good?" into concrete, gradable terms.

I then applied these techniques to long-running autonomous coding, carrying over two lessons from our earlier harness work: decomposing the build into tractable chunks, and using structured artifacts to hand off context between sessions. The final result was a three-agent architecture—planner, generator, and evaluator—that produced rich full-stack applications over multi-hour autonomous coding sessions.

## Prior Work and Persistent Problems

We've previously shown that harness design has a substantial impact on the effectiveness of long running agentic coding. In an earlier experiment, we used an initializer agent to decompose a product spec into a task list, and a coding agent that implemented the tasks one feature at a time before handing off artifacts to carry context across sessions. The broader developer community has converged on similar insights, with approaches like the "Ralph Wiggum" method using hooks or scripts to keep agents in continuous iteration cycles.

But some problems remained persistent. For more complex tasks, the agent still tends to go off the rails over time. While decomposing this issue, we observed two common failure modes with agents executing these sorts of tasks.

### Failure Mode 1: Context Degradation

Models tend to lose coherence on lengthy tasks as the context window fills (see our post on context engineering). Some models also exhibit "context anxiety," in which they begin wrapping up work prematurely as they approach what they believe is their context limit. Context resets—clearing the context window entirely and starting a fresh agent, combined with a structured handoff that carries the previous agent's state and the next steps—addresses both these issues.

This differs from compaction, where earlier parts of the conversation are summarized in place so the same agent can keep going on a shortened history. While compaction preserves continuity, it doesn't give the agent a clean slate, which means context anxiety can still persist. A reset provides a clean slate, at the cost of the handoff artifact having enough state for the next agent to pick up the work cleanly. In our earlier testing, we found Claude Sonnet 4.5 exhibited context anxiety strongly enough that compaction alone wasn't sufficient to enable strong long task performance, so context resets became essential to the harness design. This solves the core issue, but adds orchestration complexity, token overhead, and latency to each harness run.

### Failure Mode 2: Self-Evaluation Bias

A second issue, which we haven't previously addressed, is self-evaluation. When asked to evaluate work they've produced, agents tend to respond by confidently praising the work—even when, to a human observer, the quality is obviously mediocre. This problem is particularly pronounced for subjective tasks like design, where there is no binary check equivalent to a verifiable software test. Whether a layout feels polished or generic is a judgment call, and agents reliably skew positive when grading their own work.

However, even on tasks that do have verifiable outcomes, agents still sometimes exhibit poor judgment that impedes their performance while completing the task. Separating the agent doing the work from the agent judging it proves to be a strong lever to address this issue. The separation doesn't immediately eliminate that leniency on its own; the evaluator is still an LLM that is inclined to be generous towards LLM-generated outputs. But tuning a standalone evaluator to be skeptical turns out to be far more tractable than making a generator critical of its own work, and once that external feedback exists, the generator has something concrete to iterate against.

## Part 1: Frontend Design — GAN-Inspired Generator-Evaluator

I started by experimenting on frontend design, where the self-evaluation issue was most visible. Absent any intervention, Claude normally gravitates toward safe, predictable layouts that are technically functional but visually unremarkable.

Two insights shaped the harness I built for frontend design. First, while aesthetics can't be fully reduced to a score—and individual tastes will always vary—they can be improved with grading criteria that encode design principles and preferences. "Is this design beautiful?" is hard to answer consistently, but "does this follow our principles for good design?" gives Claude something concrete to grade against. Second, by separating frontend generation from frontend grading, we can create a feedback loop that drives the generator toward stronger outputs.

### Four Grading Criteria

With this in mind, I wrote four grading criteria that I gave to both the generator and evaluator agents in their prompts:

1. **Design quality**: Does the design feel like a coherent whole rather than a collection of parts? Strong work here means the colors, typography, layout, imagery, and other details combine to create a distinct mood and identity.

2. **Originality**: Is there evidence of custom decisions, or is this template layouts, library defaults, and AI-generated patterns? A human designer should recognize deliberate creative choices. Unmodified stock components—or telltale signs of AI generation like purple gradients over white cards—fail here.

3. **Craft**: Technical execution: typography hierarchy, spacing consistency, color harmony, contrast ratios. This is a competence check rather than a creativity check. Most reasonable implementations do fine here by default; failing means broken fundamentals.

4. **Functionality**: Usability independent of aesthetics. Can users understand what the interface does, find primary actions, and complete tasks without guessing?

I emphasized design quality and originality over craft and functionality. Claude already scored well on craft and functionality by default, as the required technical competence tended to come naturally to the model. But on design and originality, Claude often produced outputs that were bland at best. The criteria explicitly penalized highly generic "AI slop" patterns, and by weighting design and originality more heavily it pushed the model toward more aesthetic risk-taking.

I calibrated the evaluator using few-shot examples with detailed score breakdowns. This ensured the evaluator's judgment aligned with my preferences, and reduced score drift across iterations.

### Implementation

I built the loop on the Claude Agent SDK, which kept the orchestration straightforward. A generator agent first created an HTML/CSS/JS frontend based on a user prompt. I gave the evaluator the Playwright MCP, which let it interact with the live page directly before scoring each criterion and writing a detailed critique. In practice, the evaluator would navigate the page on its own, screenshotting and carefully studying the implementation before producing its assessment. That feedback flowed back to the generator as input for the next iteration. I ran 5 to 15 iterations per generation, with each iteration typically pushing the generator in a more distinctive direction as it responded to the evaluator's critique. Because the evaluator was actively navigating the page rather than scoring a static screenshot, each cycle took real wall-clock time. Full runs stretched up to four hours. I also instructed the generator to make a strategic decision after each evaluation: refine the current direction if scores were trending well, or pivot to an entirely different aesthetic if the approach wasn't working.

### Observations

Across runs, the evaluator's assessments improved over iterations before plateauing, with headroom still remaining. Some generations refined incrementally. Others took sharp aesthetic turns between iterations.

The wording of the criteria steered the generator in ways I didn't fully anticipate. Including phrases like "the best designs are museum quality" pushed designs toward a particular visual convergence, suggesting that the prompting associated with the criteria directly shaped the character of the output.

While scores generally improved over iterations, the pattern was not always cleanly linear. Later implementations tended to be better as a whole, but I regularly saw cases where I preferred a middle iteration over the last one. Implementation complexity also tended to increase across rounds, with the generator reaching for more ambitious solutions in response to the evaluator's feedback. Even on the first iteration, outputs were noticeably better than a baseline with no prompting at all, suggesting the criteria and associated language themselves steered the model away from generic defaults before any evaluator feedback led to further refinement.

**Notable example**: I prompted the model to create a website for a Dutch art museum. By the ninth iteration, it had produced a clean, dark-themed landing page for a fictional museum. The page was visually polished but largely in line with my expectations. Then, on the tenth cycle, it scrapped the approach entirely and reimagined the site as a spatial experience: a 3D room with a checkered floor rendered in CSS perspective, artwork hung on the walls in free-form positions, and doorway-based navigation between gallery rooms instead of scroll or click. It was the kind of creative leap that I hadn't seen before from a single-pass generation.

## Part 2: Long-Running Autonomous Coding — Three-Agent Architecture

With these findings in hand, I applied this GAN-inspired pattern to full-stack development. The generator-evaluator loop maps naturally onto the software development lifecycle, where code review and QA serve the same structural role as the design evaluator.

### V1 Harness (Opus 4.5): Three-Agent System with Sprints

In our earlier long-running harness, we had solved for coherent multi-session coding with an initializer agent, a coding agent that worked one feature at a time, and context resets between sessions. Context resets were a key unlock: the harness used Sonnet 4.5, which exhibited the "context anxiety" tendency mentioned earlier. Opus 4.5 largely removed that behavior on its own, so I was able to drop context resets from this harness entirely. The agents were run as one continuous session across the whole build, with the Claude Agent SDK's automatic compaction handling context growth along the way.

For this work I built on the foundation from the original harness with a three-agent system, with each agent addressing a specific gap I'd observed in prior runs:

1. **Planner**: Took a simple 1-4 sentence prompt and expanded it into a full product spec. Prompted to be ambitious about scope and to stay focused on product context and high level technical design rather than detailed technical implementation. Also asked to find opportunities to weave AI features into product specs.

2. **Generator**: Worked in sprints, picking up one feature at a time from the spec. Each sprint implemented the app with a React, Vite, FastAPI, and SQLite (later PostgreSQL) stack. Self-evaluated at the end of each sprint before handing off to QA. Had git for version control.

3. **Evaluator**: Used the Playwright MCP to click through the running application the way a user would, testing UI features, API endpoints, and database states. Graded each sprint against both bugs found and a set of criteria covering product depth, functionality, visual design, and code quality. Each criterion had a hard threshold; if any fell below, the sprint failed.

### Sprint Contracts

Before each sprint, the generator and evaluator negotiated a sprint contract: agreeing on what "done" looked like for that chunk of work before any code was written. The generator proposed what it would build and how success would be verified, and the evaluator reviewed that proposal. Communication was handled via files: one agent would write a file, another agent would read it and respond.

### V1 Results: Retro Game Maker

Prompt: "Create a 2D retro game maker with features including a level editor, sprite editor, entity behaviors, and a playable test mode."

| Harness | Duration | Cost |
|---------|----------|------|
| Solo | 20 min | $9 |
| Full harness | 6 hr | $200 |

The harness was over 20x more expensive, but the difference in output quality was immediately apparent.

**Solo run issues**: Layout wasted space, workflow was rigid, and the actual game was broken—entities appeared on screen but nothing responded to input. The wiring between entity definitions and the game runtime was broken.

**Full harness advantages**: The planner expanded the one-line prompt into a 16-feature spec across ten sprints, including sprite animation, behavior templates, sound effects, AI-assisted sprite generator, and game export. The evaluator kept implementation in line with the spec—Sprint 3 alone had 27 criteria covering the level editor. Example evaluator findings:

- Rectangle fill tool: "FAIL — Tool only places tiles at drag start/end points instead of filling the region. fillRectangle function exists but isn't triggered properly on mouseUp."
- Entity deletion: "FAIL — Delete key handler requires both selection and selectedEntityId to be set, but clicking an entity only sets selectedEntityId."
- Frame reorder: "FAIL — PUT /frames/reorder route defined after /{frame_id} routes. FastAPI matches 'reorder' as a frame_id integer and returns 422."

### Tuning the Evaluator

Getting the evaluator to perform at this level took work. Out of the box, Claude is a poor QA agent. In early runs, it identified legitimate issues, then talked itself into deciding they weren't a big deal and approved the work anyway. It also tended to test superficially. The tuning loop was to read the evaluator's logs, find examples where its judgment diverged from mine, and update the QA's prompt to solve for those issues. It took several rounds before the evaluator was grading reasonably.

## Part 3: V2 Harness — Simplification with Opus 4.6

The first set of harness results was encouraging, but it was also bulky, slow, and expensive. The logical next step was to find ways to simplify the harness without degrading its performance.

**Key principle**: Every component in a harness encodes an assumption about what the model can't do on its own, and those assumptions are worth stress testing, both because they may be incorrect, and because they can quickly go stale as models improve. From "Building Effective Agents": "find the simplest solution possible, and only increase complexity when needed."

### Simplification with Opus 4.6

Opus 4.6 provided motivation to reduce harness complexity. From the launch blog: "[Opus 4.6] plans more carefully, sustains agentic tasks for longer, can operate more reliably in larger codebases, and has better code review and debugging skills to catch its own mistakes."

Changes made:
- **Removed sprint construct entirely**: Opus 4.6 could natively handle work without decomposition
- **Kept planner**: Without it, the generator under-scoped
- **Moved evaluator to single pass at end**: Rather than per-sprint grading
- **Evaluator became conditional**: Worth the cost when task sits beyond what model does reliably solo

### V2 Results: Digital Audio Workstation

Prompt: "Build a fully featured DAW in the browser using the Web Audio API."

| Agent & Phase | Duration | Cost |
|---------------|----------|------|
| Planner | 4.7 min | $0.46 |
| Build (Round 1) | 2 hr 7 min | $71.08 |
| QA (Round 1) | 8.8 min | $3.24 |
| Build (Round 2) | 1 hr 2 min | $36.89 |
| QA (Round 2) | 6.8 min | $3.09 |
| Build (Round 3) | 10.9 min | $5.88 |
| QA (Round 3) | 9.6 min | $4.06 |
| **Total** | **3 hr 50 min** | **$124.70** |

The generator ran coherently for over two hours without sprint decomposition. QA still caught real gaps:

Round 1: "Several core DAW features are display-only without interactive depth: clips can't be dragged/moved on the timeline, there are no instrument UI panels, and no visual effect editors."

Round 2: "Audio recording is still stub-only. Clip resize by edge drag and clip split not implemented. Effect visualizations are numeric sliders, not graphical."

The final app had all core pieces of a functional music production program: arrangement view, mixer, and transport. The agent set tempo and key, laid down a melody, built a drum track, adjusted mixer levels, and added reverb.

## Takeaways

As models continue to improve, we can roughly expect them to be capable of working for longer, and on more complex tasks. In some cases, that will mean the scaffold surrounding the model matters less over time. On the other hand, the better the models get, the more space there is to develop harnesses that can achieve complex tasks beyond what the model can do at baseline.

Lessons worth carrying forward:
1. **Experiment with the model**: Read its traces on realistic problems, and tune its performance to achieve your desired outcomes
2. **Decompose when needed**: There is sometimes headroom from decomposing the task and applying specialized agents to each aspect
3. **Re-examine harness on new models**: Strip away pieces no longer load-bearing, add new pieces to achieve greater capability

**Core conviction**: The space of interesting harness combinations doesn't shrink as models improve. Instead, it moves, and the interesting work for AI engineers is to keep finding the next novel combination.
