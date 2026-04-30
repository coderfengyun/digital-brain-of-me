# Why Some Expertise Transfers to AI Personas Easily While Other Expertise Resists Capture

> **Author**: Muratcan Koylan ([@koylanai](https://x.com/koylanai))
> **Date**: December 19, 2025
> **Source**: [Original Tweet](https://x.com/koylanai/status/2002059772867326374)
> **Series**: AI Persona Creation from Human Expert Interviews — Part 3

---

Harry Collins's taxonomy of tacit knowledge clarified something I'd been struggling with: why some expertise transfers to AI personas easily while other expertise resists capture entirely.

Collins, a sociologist of science at Cardiff, spent decades studying how scientific knowledge actually transfers between people — not through papers and manuals, but through extended contact between researchers.

## Three Types of Tacit Knowledge (Ordered by Resistance to Explication)

### 1. Relational Tacit Knowledge (Weak)

Knowledge that's tacit for contingent, not principled, reasons. Collins identifies five subcategories:

- **Concealed knowledge**: Trade secrets, selective apprenticeship, guild protections
- **Mismatched saliences**: The expert assumes you already possess some critical piece of knowledge, so they don't mention it (e.g. A CMO who doesn't mention that "repositioning always fails when the sales team isn't consulted first" because to them it's obvious)
- **Unrecognized knowledge**: The expert doesn't realize which parts of what they know are actually doing the work (e.g. The strategist who doesn't realize their habit of asking "what would make this obviously wrong?" is doing most of the work)
- **Ostensive knowledge**: Can only be transferred through guided interaction with an object — "here, feel how this should move"
- **Logistically demanding knowledge**: Could be explicated, but doing so would be prohibitively expensive or time-consuming

Any piece of relational tacit knowledge CAN be made explicit. With enough time, the right questions, and skilled extraction, you can capture it. This is what NDM (first post of this series) researchers spend months doing. It's also what we're targeting with our AI interviewer system.

### 2. Somatic Tacit Knowledge (Medium)

Knowledge that's tacit because it's embodied. Bike riding, surgical technique, guitar playing. Collins makes a crucial distinction here: somatic tacit knowledge is tacit only because of human limitations, not because of the knowledge itself.

The physics of bicycle balancing is completely understood. Machines can ride bikes. It's tacit for humans only because we can't consciously perform the calculations fast enough so we learn through practice instead. "If we could calculate a billion times faster we could probably ride a bike using the rules of physics."

This means machines can often replicate somatic skills through different mechanisms than humans use. The knowledge isn't fundamentally inexplicable, it's just that humans access it through embodiment rather than calculation.

### 3. Collective Tacit Knowledge (Strong)

Knowledge that's tacit because it's embedded in social context. You pick it up through socialization, not instruction.

The formal rules of traffic are explicit. But negotiating a busy intersection in Hanoi versus London versus Rome versus Delhi involves completely different collective tacit knowledge — when to make eye contact with drivers, which rules actually apply, how to signal your intentions through body language. You absorb this by being there, participating in the social life of the place.

This is the "irreducible heartland" of tacit knowledge. Collins argues it cannot be explicated even in principle because it's polimorphic — requiring different behaviors in different social contexts, constantly adapting to changes in society, located in the collective rather than any individual.

## The Inverse Relationship

Collins notes an inverse relationship that matters for training and extraction:

**Ease of explicating:**
Relational (possible) → Somatic (sometimes) → Collective (impossible)

**Ease of acquiring:**
Collective (easiest — we absorb it from birth) → Somatic → Relational (hardest)

Collective tacit knowledge comes naturally through socialization. We don't notice acquiring it. Relational tacit knowledge is the hardest to acquire because it depends on the contingencies of relationships — you need access to the right people who are willing to share. This is exactly why expertise is scarce even when it's explicable in principle.

## Implications for AI Persona Design

When we build AI personas for marketing and strategy, we're primarily dealing with **relational tacit knowledge**. The expert has decoded their domain. They make sophisticated judgments. But they haven't articulated the full structure of how they think — often because of mismatched saliences (they assume their reasoning is obvious) or unrecognized knowledge (they don't know which parts of their expertise are actually critical).

Interviews work here because you capture the natural joint distribution of their beliefs through concrete examples. They tell you through the incidents they describe.

### Why LLM-Generated Synthetic Personas Fail

Collins's 2024 paper on AI is direct about this: "Learning from the internet is not the same as socialisation."

When you ask an LLM to "imagine a senior brand strategist," it invents from statistical priors — what it learned from text about brand strategists. It can't access the actual joint distribution that exists in a real expert's head. LLMs are "retrospectively socialised" through human feedback rather than acquiring genuine understanding. So they produce plausible-sounding content without the underlying structure that makes expert judgment reliable.

### When Interviews Aren't Enough

Somatic and collective tacit knowledge are harder. If your expert's skill is primarily embodied (a physical craft) or primarily social (navigating organizational politics), interviews capture less. Video observation and apprenticeship help for somatic. Ethnographic immersion helps for collective.

For most forms of strategy expertise, however, the core is relational. The expert has insights that could be explicated with the right questions, from someone who understands what they're looking for. And relational tacit knowledge can be extracted.

That's exactly what AI interviewer systems should be designed to do: systematically probe the subcategories Collins identified — surfacing concealed knowledge, correcting mismatched saliences, uncovering unrecognized knowledge — through a structured conversation that captures the joint distribution of real expert judgment.

> Part 4 will cover cognitive agility — why dynamic reasoning matters more than static knowledge for expert personas.

---

## Context: Part 2 — Applied Cognitive Task Analysis (ACTA)

> [Original Tweet (Part 2)](https://x.com/koylanai/status/2000641196289642755)

In my last post of the 'AI Persona Creation from Human Expert Interviews' series, I covered Gary Klein's RPD model, the map of how expert intuition actually works.

The Critical Decision Method (CDM) that Klein developed is powerful but it's a research tool, not a practitioner tool. Militello and Hutton solved this in 1998 with **Applied Cognitive Task Analysis (ACTA)**, a simplified toolkit that trades some depth for accessibility.

The main goal of ACTA is to extract the "black box" of expert performance. Graduate students with zero Cognitive Task Analysis experience used ACTA to interview fireground commanders. They successfully identified training gaps that seasoned pros had missed.

If a grad student can use this framework to extract tacit expertise, a specialized AI Interviewer can too.

### How to Architect Agents to Use ACTA

**1. The Task Diagram**
Ask the expert to decompose their skill into 3–6 major steps. We don't want granular detail yet; we want the cognitive "heat map."

- Probe: "Which of these steps require difficult cognitive skills, judgments, assessments, or problem-solving?"
- Why: This focuses the AI's context window & attention mechanism. We stop the expert from giving speeches about "best practices" and force them to focus on the hard parts.

**2. The Knowledge Audit**
The core. Use specific probes to target the invisible mental work:

- **The "Noticing" Probe**: "Have you had experiences where part of a situation just 'popped' out at you, but others didn't catch it?"
- **The "Past & Future" Probe**: "When did you walk into a situation and instantly know how it got there and where it was going?"
- **The "Improvising" Probe**: "When did you have to deviate from the standard procedure to get the job done?"

After every probe, ask: "What would a novice have done in that situation?" — This defines the negative space of expertise and prevents our AI persona from hallucinating generic competence.

**3. The Simulation Interview**
Present a challenging scenario, revealing events one at a time. At each stage, the agent probes for specific cues. Run the same simulation with multiple experts to map the full "solution space" of acceptable answers.

**4. The Output: A Cognitive Demands Table**

| Difficult Element | Cues | Strategies | Novice Errors |
|---|---|---|---|
| e.g., determining if a lead is qualified | e.g., tone of voice, specific objections | e.g., asking about budget early | e.g., pitching features too soon |

- Every "Cue" becomes a pattern recognition instruction.
- Every "Strategy" becomes a reasoning step.
- Every "Novice Error" becomes a constraint.

Prompt engineering alone cannot invent these details. You cannot "few-shot" prompt a specific intuition that you don't know exists. You have to interview for it.

ACTA turns the "magic" of expertise into structured data. And structured data is something we can scale.
