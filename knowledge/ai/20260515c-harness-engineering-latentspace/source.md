# Extreme Harness Engineering for Token Billionaires

**Author**: swyx (Latent Space), with Ryan Lopopolo (OpenAI Frontier) and Vibhu
**Source**: https://www.latent.space/p/harness-eng
**Date**: 2026-04-08
**Platform**: Latent Space Podcast (72 min) + Substack post (摘要 + 完整 transcript)
**Video**: https://www.youtube.com/watch?v=CeOXx-XTYek
**Original OpenAI blog**: https://openai.com/index/harness-engineering/
**Symphony repo**: https://github.com/openai/symphony
**Full transcript**: snapshot1.txt（同目录，从 Latent Space 页面 snapshot 提取）

---

Subtitle: 1M LOC, 1B toks/day, 0% human code, 0% human review — Ryan Lopopolo, OpenAI Frontier & Symphony

We shed light on OpenAI's first Dark Factory for the first time.

Ryan Lopopolo of OpenAI is leading that charge, recently publishing a lengthy essay on Harness Eng that has become the talk of the town. In it, Ryan peeled back the curtains on how the recently announced OpenAI Frontier team have become OpenAI's top Codex users, running a >1m LOC codebase with 0 human written code and, crucially for the Dark Factory fans, no human REVIEWED code before merge. Ryan is admirably evangelical about this, calling it borderline "negligent" if you aren't using >1B tokens a day (roughly $2-3k/day in token spend).

Over the past five months, they ran an extreme experiment: building and shipping an internal beta product with zero manually written code. Through the experiment, they adopted a different model of engineering work: when the agent failed, instead of prompting it better or to "try harder," the team would look at "what capability, context, or structure is missing?"

The result was Symphony, "a ghost library" and reference Elixir implementation that sets up a massive system of Codex agents all extensively prompted with the specificity of a proper PRD spec, but without full implementation.
