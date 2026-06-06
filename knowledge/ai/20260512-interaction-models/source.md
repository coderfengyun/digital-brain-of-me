# Interaction Models: A Scalable Approach to Human-AI Collaboration

**Source**: https://thinkingmachines.ai/blog/interaction-models/
**Author**: Thinking Machines Lab
**Date**: May 11, 2026

---

## Introduction

Today, we're announcing a research preview of interaction models: models that handle interaction natively rather than through external scaffolding. We think interactivity should scale alongside intelligence; the way we work with AI should not be treated as an afterthought. Interaction models let people collaborate with AI the way we naturally collaborate with each other—they continuously take in audio, video, and text, and think, respond, and act in real time.

We train an interaction model from scratch. To ensure real-time responsiveness, we adopt a multi-stream, micro-turn design. Our research preview demonstrates qualitatively new interaction capabilities, as well as state-of-the-art combined performance in intelligence and responsiveness.

## The collaboration bottleneck

AI labs often treat the ability for AI to work autonomously as the model's most important capability.[1] As a result, today's models and interfaces aren't optimized for humans to remain in the loop.[2]

[1] Kwa, T., West, B., Becker, J., et al. Measuring AI Ability to Complete Long Tasks. METR, 2025.

[2] A recent frontier model card states: "Importantly, we find that when used in an interactive, synchronous, "hands-on-keyboard" pattern, the benefits of the model were less clear. When used in this fashion, some users perceived [our model] as too slow and did not realize as much value. Autonomous, long-running agent harnesses better elicited the model's coding capabilities."

Autonomous interfaces are valuable, but in most real work, users can't fully specify their requirements upfront and walk away—good results benefit from a collaborative process where the human stays in the loop, clarifying and giving feedback along the way. However, humans increasingly get pushed out not because the work doesn't need them, but because the interface has no room for them. Instead, people are most effective when they can collaborate with AI the same way we do with other people: messaging, talking, listening, seeing, showing, and interjecting as needed—and for the model to do the same.[3][4]

[3] Communication gets better with: (a) Copresence: people can interact with what others are interacting with; (b) Contemporality: people receive information as it's produced by others with instant feedback; (c) Simultaneity: people receive and produce information at the same time. Clark H. and Brennan S., "Grounding in Communication," in Perspectives on Socially Shared Cognition, 1991.

[4] The evanescence of orality for its participatory (cf. objectively distanced) nature. Today's computers and mediums of knowledge work have similar interactive properties. Ong, W. J.. In Orality and Literacy: The technologizing of the word, 1982.

In order to resolve this, we need to move beyond the current turn-based interface for the models. Today's models experience reality in a single thread.[5] Until the user finishes typing or speaking, the model waits with no perception of what the user is doing or how the user is doing it. Until the model finishes generating, its perception freezes, receiving no new information until it finishes or is interrupted. This creates a narrow channel for human-AI collaboration that limits how much of a person's knowledge,[6][7] intent, and judgement can reach the model, and how much of the model's work can be understood. Picture trying to resolve a crucial disagreement over email rather than in person.

[5] We are referring to commercial general-purpose frontier models—there are smaller-scale or specialized models like Moshi, PersonaPlex, Nemotron VoiceChat, or GPT-Realtime-Translate.

[6] "Metis, with the premium it places on practical knowledge, experience, and stochastic reasoning…is the mode of reasoning most appropriate to complex material and social tasks where the uncertainties are so daunting that we must trust our (experienced) intuition and feel our way." Scott, J. C: Métis. In Seeing like a State: How certain schemes to improve the human condition have failed, 1998.

[7] "A little reflection will show that there is…a body of very important but unorganized knowledge…: the knowledge of the particular circumstances of time and place." Hayek, F. A. "The use of knowledge in society." The American Economic Review, 1945.

At Thinking Machines, we believe we can solve this bandwidth bottleneck by making **AI interactive in real time across any modality**. This enables AI interfaces to meet humans where they are, rather than forcing humans to contort themselves to AI interfaces.

Most existing AI models bolt on interactivity with a harness: stitching components together to emulate interruptions, multimodality, or concurrency.[8] However, "the bitter lesson"[9] suggests that these hand-crafted systems will be outpaced by the advance of general capabilities. **For interactivity to scale with intelligence, it must be part of the model itself.** With this approach, scaling a model makes it smarter **and** a better collaborator.

[8] Most real-time commercial speech systems use voice-activity-detection components to detect turn boundaries.

[9] Sutton R. The Bitter Lesson, 2019.

## Capabilities

Having interactivity be part of the model unlocks a variety of capabilities that would otherwise need to be implemented in the harness.

- **Seamless dialog management.** The model tracks implicitly whether the speaker is thinking, yielding, self-correcting, or inviting a response. There is no separate dialog management component.
- **Verbal and visual interjections.** The model jumps in as needed depending on the context, not only when the user finishes speaking.
- **Simultaneous speech.** The user and the model can speak concurrently (e.g. live translation)
- **Time-awareness.** The model has a direct sense of elapsed time.
- **Simultaneous tools calls, search, and generative UI.** While speaking and listening to the user, the model can concurrently search, browse the web, or generate UI—weaving back results into the conversation as needed.

In a longer real session, all of this happens continuously, creating an experience that feels more like collaborating and less like prompting.

## Our approach

An interaction model is in constant two-way exchange with the user—perceiving and responding at the same time. Some domains take such interactivity as a given—the physical world demands that robotics and autonomous vehicles operate in real time. Audio full-duplex models[10] are another example where interaction is bidirectional and continuous.

[10] Moshi, PersonaPlex, nemotron-voicechat, Seeduplex.

Applying the same principle, we set out to build an interaction model native to this regime—one that perceives and responds in the same continuous loop, across audio, video, and text. The result is a system architected around two ideas: a time-aware interaction model that maintains real-time presence, and an asynchronous background model that handles sustained reasoning, tool use, and longer-horizon work.

### System overview

The interaction model is in constant exchange with the user. When a task requires deeper reasoning than can be produced instantaneously, the interaction model delegates to a background model that runs asynchronously.[11] The interaction model remains present throughout — answering follow-ups, taking new input, holding the thread — and integrates background results into the conversation as they arrive.

[11] This approach builds upon prior work like Qwen-omni, KAME, MoshiRAG.

This split lets the user benefit from both responsiveness as well as the full extent of intelligence: the planning, tool-use, and agentic workflows of reasoning models at the response latency of non-thinking ones. Note that both the background and interaction models are intelligent — on its own, the interaction model is also competitive on both interactive and intelligence benchmarks.

### The interaction model

Our starting point is continuous audio and video — modalities that are inherently real-time. Text can wait, but a live conversation cannot. By designing around the hardest case first, we arrive at an architecture that is natively multimodal, time-aware, and capable of handling concurrent input and output streams across all modalities. Several design choices make this possible.

**Time-aligned micro-turns.** The interaction model works with micro-turns continuously interleaving the processing of 200ms worth of input and generation of 200ms worth of output. Rather than consuming a complete user-turn and generating a complete response, both input and output tokens are treated as streams. Working with 200ms chunks of these streams enables near real-time concurrency of multiple input and output modalities.

With this design, there are no artificial turn boundaries that the model must adhere to. In contrast, most existing real-time systems require a harness that predicts turn boundaries in order for the turn-based models to feel real-time and responsive.[12] This harness is made out of components like voice-activity-detection (VAD) that are meaningfully less intelligent than the model itself. This precludes a variety of interaction modes like proactive interjections ("interrupt when I say something wrong") or reactions to visual cues ("tell me when I've written a bug in my code"). Moreover, the model can do things like speak while listening ("translate from spanish to english live") or watching ("live-commentate this sports game").

[12] Moshi, PersonaPlex, and Nemotron Voicechat are examples of full duplex systems that do not use harnesses to detect turns. They are smaller scale models focused on latency rather than intelligence benchmarks.

Thus, all of these different interaction modes that require special harnesses today become special-cases of what the model can do and improve in quality as we scale up model size and training data.

**Encoder-free early fusion.** Rather than processing audio and video through large, standalone encoders, we opt for a system with minimal pre-processing. Many omnimodal models require training a separate encoder (e.g. Whisper-like) or decoder (e.g. TTS model-like). We instead take in audio signals as dMel (Bai, et al. 2024) and transform it via a light-weighted embedding layer. Images are split into 40x40 patches which are encoded by an hMLP (Touvron et al. 2022). For the audio decoder we use a flow head (Lipman at al. 2022). All components are co-trained from scratch together with the transformer.

**Inference optimization.** At inference time, 200ms chunks require frequent prefills and decodes of small sizes, each having to meet strict latency constraints. Unfortunately, existing LLM inference libraries are not optimized for frequent small prefills—they often have a significant amount of overhead per turn. To address this, we implemented streaming sessions. The client sends each 200ms chunk as a separate request, while the inference server appends these chunks into a persistent sequence in GPU memory. This avoids frequent memory reallocations and metadata computations, and we've upstreamed a version of this feature to SGLang. In addition, we also optimized our kernels for latency as well as the shapes we see for bidirectional serving. For example, we use a gather+gemv strategy for MoE kernels instead of the standard grouped gemm, as in prior work from PyTorch and Cursor.

**Trainer-sampler alignment.** We've found bitwise trainer-sampler alignment to be useful for training stability as well as debugging the various components of our system. We implement batch-invariant kernels with minimal (<5%) e2e performance overhead.[13] To highlight two particular kernels:

[13] Funnily enough, for some period of time using the batch-invariant kernels was actually faster e2e, due to the custom communication kernels which were not only batch-invariant but also much lower latency.

- **All-reduce and reduce-scatter**: We use NVLS to implement low-latency comm kernels which are deterministic on Blackwell, and achieve bitwise alignment between somewhat different parallelism strategies (i.e. Sequence Parallelism and Tensor Parallelism).
- **Attention**: The primary challenge with attention is Split-KV, which can typically lead to inconsistent accumulation orders between decode and prefill.[14] However, we can maintain consistent accumulation order by choosing to split consistently between decode and prefill. For example, we could split SMs to process 4096 tokens at a time (left-aligned), achieving good efficiency in both prefill and decode.

[14] Work done in collaboration with Colfax

**Coordination between interaction and background models.** When the interaction model delegates, it sends a rich context package — not a standalone query, but the full conversation. Results stream back as the background model produces them, and the interaction model interleaves these updates into the conversation at a moment appropriate to what the user is currently doing, rather than as an abrupt context switch.

**Safety.** Because real-time interaction stresses safety differently than turn-based exchanges, our safety work focused on two axes: modality-appropriate refusals and long-horizon robustness. To make refusals colloquial in speech, we use a text-to-speech model to generate refusal and over-refusal training data covering a range of disallowed topics, with the refusal boundary calibrated to favor naturally-phrased, but no less firm, refusals. To improve robustness across extended speech-to-speech conversations, we used an automated red-teaming harness to generate multi-turn refusal data, while maintaining close behavioral parity with the model's text-based refusals.

## Benchmarks

### Intelligence and interactivity frontier

We show that our interaction model, named **TML-Interaction-Small**, is the first model that has both strong intelligence/instruction following **and** interactivity. To measure interaction quality we use FD-bench which is one of the few existing benchmarks intended to measure interactivity. In FD-bench v1.5, the model is given prerecorded audio, and must respond at certain times. This benchmark measures model behavior across several scenarios: user interruption, user backchannel, talking to others, and background speech. Our model scores well in all of these areas. To quantify intelligence we use Audio MultiChallenge, a common benchmark that tracks intelligence and instruction following.

#### Benchmark Results

| Benchmark | Metric | TML-Interaction-Small | GPT-realtime-2.0 (minimal) | GPT-realtime-1.5 | Gemini-3.1-flash-live (minimal) | Qwen 3.5 OMNI-plus-realtime | GPT-realtime-2.0 (xhigh) | Gemini-3.1-flash-live (high) |
|-----------|--------|----------------------|---------------------------|-------------------|-------------------------------|---------------------------|--------------------------|---------------------------|
| FD-bench V1 | Turn-taking latency (s) | **0.40** | 1.18 | 0.59 | 0.57 | 2.14 | 1.63 | 0.94 |
| FD-bench V1.5 | Average | **77.8** | 46.8 | 48.3 | 54.3 | 39.0 | 47.8 | 45.5 |
| FD-bench V3 | Response Quality / Pass@1 | **82.8 / 68.0** | 80.0 / 52.0 | 77.9 / 55.0 | 68.5 / 48.0 | 60.0 / 50.0 | 81.0 / 58.0 | 71.4 / 48.0 |
| Audio MultiChallenge | APR (%) | 43.4 | 37.6 | 34.7 | 26.8 | - | **48.5** | 36.1 |
| BigBench Audio | Accuracy (%) | 75.7 / 96.5* | 71.8 | 81.4 | 71.3 | 73.0 | **96.6** | 96.6 |
| IFEval (VoiceBench) | Accuracy (%) | 82.1 | 81.7 | 68.1 | 67.6 | 80.3 | **83.2** | 82.8 |
| IFEval | Accuracy (%) Text | 89.7 | **89.6** | 87.5 | 85.8 | 83.4 | **95.2** | 90.0 |
| Harmbench | Refusal rate (%) | 99.0 | 99.5 | **100.0** | 99.0 | 99.5 | **100.0** | 98.0 |

*For benchmarks that require reasoning or tool calls we report results with background agent enabled.

### New dimensions of interactivity

The existing interactivity-oriented benchmarks do not adequately capture the qualitative jumps in interaction capabilities we notice. To that end, we have some early work aimed at quantifying these capabilities.

**Time awareness and simultaneous speech.** Turn-based models with a dialog management system do not support accurate time estimation or simultaneous speech. Examples include: "How long did it take me to run one mile?", "Correct my mispronunciations as you hear them" or "How long did it take me to write this function?"

We created two internal benchmarks:

- **TimeSpeak:** Tests whether the model can initiate speech at user-specified times while producing the correct content. For example: "I want to practice my breathing, remind me to breathe in and out every 4 seconds until I ask you to stop."
- **CueSpeak:** Tests whether the model speaks at the appropriate moment with the expected semantically correct response. Dataset entries are created to ensure that the model needs to speak at the same time as the user to get a full score. For example: "Everytime I codeswitch and use another language, give me the correct word in the original language."

**Visual proactivity.** Today's commercial real-time APIs perform turn-detection via audio-only dialogue management harnesses. They respond to spoken turns, but they cannot proactively choose to speak when the visual world changes.[16]

[16] Though we are not aware of any commercial APIs that support speech-out visual proactivity, several academic papers have built related research prototypes. StreamBridge, Streamo, and MMDuet2 study when to output text in a streaming video input setting. Being text out, they do not study additional constraints of speech-output interaction. Closest to ours is AURA, which adds an ASR/TTS demo around a VideoLLM that decides when to emit text or be silent; in contrast ours is speech-native and full-duplex.

We adapted three benchmarks to evaluate visual proactivity:

- **RepCount-A**: Videos of repeated actions adapted into an online counting task. Stream the video following audio instruction "Please count out reps for {action}." Grade by whether the last number said by the model after the ground truth penultimate rep was within one rep of the ground truth.
- **ProactiveVideoQA**: Videos with questions whose answers become available at specific moments. Report the paper's turn-weighted PAUC@ω=0.5 metric (scaled 0-100). Staying silent scores 25.0.
- **Charades**: Standard temporal action-localization benchmark. Model is graded by temporal IoU between predicted and reference intervals.

No existing model can meaningfully perform any of these tasks. GPT Realtime-2 (minimal) and all other models evaluated stay silent or give incorrect answers.

## Limitations and future work

- **Long sessions.** Continuous audio and video accumulate context quickly. Very long sessions still require careful context management.
- **Compute and deployment.** Streaming audio and video at low latency requires reliable connectivity. Without a good connection, the experience degrades significantly.
- **Alignment and safety.** A realtime interface opens up an exciting area of research for both alignment and safety.
- **Scaling model size.** The current TML-Interaction-Small is a 276B parameter MoE with 12B active. Larger pretrained models are currently too slow to serve in this setting. Plan to release larger models later this year.
- **Improved background agents.** Agentic intelligence is also an essential capability. Just scratched the surface in how background agents can work together with the interaction model.

## Citation

Thinking Machines Lab, "Interaction Models: A Scalable Approach to Human-AI Collaboration", Thinking Machines Lab: Connectionism, May 2026.

```bibtex
@article{thinkingmachines2026interactionmodels,
  author = {Thinking Machines Lab},
  title = {Interaction Models: A Scalable Approach to Human-AI Collaboration},
  journal = {Thinking Machines Lab: Connectionism},
  year = {2026},
  month = {May},
  note = {https://thinkingmachines.ai/blog/interaction-models/},
  doi = {10.64434/tml.20260511},
}
```
