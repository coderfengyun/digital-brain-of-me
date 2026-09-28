# RubricEval : A Rubric-Level Meta-Evaluation Benchmark for LLM Judges in Instruction Following

###### Abstract

Rubric-based evaluation has become a prevailing paradigm for evaluating instruction following in large language models (LLMs). Despite its widespread use, the reliability of these rubric-level evaluations remains unclear, calling for meta-evaluation. However, prior meta-evaluation efforts largely focus on the response level, failing to assess the fine-grained judgment accuracy that rubric-based evaluation relies on. To bridge this gap, we introduce RubricEval . Our benchmark features: (1) the first rubric-level meta-evaluation benchmark for instruction following, (2) diverse instructions and responses spanning multiple categories and model sources, and (3) a substantial set of 3,486 quality-controlled instances, along with Easy / Hard subsets that better differentiates judge performance. Our experiments reveal that rubric-level judging remains far from solved : even GPT-4o, a widely adopted judge in instruction-following benchmarks, achieves only 55.97% on Hard subset. Considering evaluation paradigm, rubric-level evaluation outperforms checklist-level, explicit reasoning improves accuracy, and both together reduce inter-judge variance. Through our established rubric taxonomy, we further identify common failure modes and offer actionable insights for reliable instruction-following evaluation.

RubricEval : A Rubric-Level Meta-Evaluation Benchmark for LLM Judges in Instruction Following

Tianjun Pan 1 , Xuan Lin 3 , Wenyan Yang 3 , Qianyu He 1 , Shisong Chen 1 Licai Qi 3 , Wanqing Xu 3 , Hongwei Feng 1 2 2 2 Corresponding author , Bo Xu 2 2 2 2 Corresponding author , Yanghua Xiao 1 2 2 2 Corresponding author 1 College of Computer Science and Artificial Intelligence, Fudan University 2 Donghua University, 3 Ant Group

## 1 Introduction

Instruction following (IF) is a fundamental capability of large language models (LLMs), as it directly affects task completion quality and user experience Ouyang et al. ( 2022 ); Achiam et al. ( 2023 ) . In this context, reliable evaluation of instruction following becomes equally critical.

Accordingly, a central question is how to reliably evaluate instruction-following behavior in LLMs. While rule-based evaluation methods such as IFEval Zhou et al. ( 2023 ) offer scalability and high precision, they are restricted to a narrow set of verifiable constraints. To handle open-ended instructions with semantically complex constraints, recent benchmarks Qin et al. ( 2024b ); Zhang et al. ( 2025a ); Wen et al. ( 2024 ); Zhang et al. ( 2025b ) decompose instructions into fine-grained rubrics and use LLM judges to verify each rubric, as illustrated in Figure 1 (a). While widely used for evaluation, potential errors in per-rubric judgments may propagate through score aggregation and bias subsequent applications, such as model training Gunjal et al. ( 2025 ); Huang et al. ( 2025 ); Peng et al. ( 2025 ); An et al. ( 2025 ) , self-evolving Wang et al. ( 2025 ); An et al. ( 2025 ) , and benchmark scoring, making judge reliability a critical concern.

Consequently, meta-evaluating LLM judges becomes indispensible. However, existing meta-evaluation efforts for instruction following Zeng et al. ( 2023 ); Malik et al. ( 2025 ); Zhou et al. ( 2025 ) exhibit several critical limitations: (1) Coarse granularity : Prior work evaluates judges at the response level, assessing only their ability to distinguish overall response quality, which is misaligned with the modern rubric-based evaluation paradigm and fails to measure fine-grained judgment accuracy. (2) Limited instruction coverage : Existing benchmarks rely on relatively simple instructions with narrow type diversity, limiting their ability to assess judge performance across varied scenarios. (3) Lack of realistic failures : They rely on synthetic or curated failure cases rather than real model-generated responses, unable to capture realistic failure modes and thus may not faithfully reflect judge performance in practice.

To address these limitations, we introduce RubricEval , a fine-grained meta-evaluation benchmark that evaluates LLM judges at the rubric level. Our benchmark offers three key advantages: (1) Fine granularity: it evaluates judges at the rubric level, directly aligned with the prevailing rubric-based instruction following evaluation paradigm; (2) Diverse and realistic data: diverse instruction types combined with real model outputs, reflecting realistic evaluation scenarios; and (3) Reliable reference labels: reference labels are obtained through a multi-stage framework with human verification, ensuring high reliability.

As illustrated in Figure 1 (b), RubricEval focuses on binary rubric-judgment tasks: given an instruction, a response, and a target rubric, a candidate judge predicts whether the response satisfies the rubric. By comparing judge predictions against our curated high-confidence reference labels, we assess their fine-grained evaluation capability.

Overall, RubricEval comprises 3,486 rubric-level judgment instances across four instruction categories, with 2,034 Easy and 1,452 Hard instances, enabling finer differentiation of judge capabilities, especially on challenging cases.

Our contributions can be summarized as follows:

- • The first fine-grained meta-evaluation benchmark for instruction following : We introduce RubricEval , the first rubric-level meta-evaluation benchmark with 3,486 instances spanning diverse instruction types and real model outputs, capturing realistic evaluation scenarios.

The first fine-grained meta-evaluation benchmark for instruction following : We introduce RubricEval , the first rubric-level meta-evaluation benchmark with 3,486 instances spanning diverse instruction types and real model outputs, capturing realistic evaluation scenarios.

- • A scalable rubric annotation framework : We propose the Rubric Arbitration Framework (RAF), which addresses the challenge of obtaining reliable rubric-level labels at scale. RAF achieves high agreement with human annotations while significantly reducing annotation cost.

A scalable rubric annotation framework : We propose the Rubric Arbitration Framework (RAF), which addresses the challenge of obtaining reliable rubric-level labels at scale. RAF achieves high agreement with human annotations while significantly reducing annotation cost.

- • Systematic evaluation and analysis : We benchmark a diverse set of LLM judges on RubricEval and introduce a rubric taxonomy for structured analysis of judge robustness and failure modes. Our study provides actionable insights for improving instruction-following evaluation.

Systematic evaluation and analysis : We benchmark a diverse set of LLM judges on RubricEval and introduce a rubric taxonomy for structured analysis of judge robustness and failure modes. Our study provides actionable insights for improving instruction-following evaluation.

## 2 Related Work

##### Benchmarks and Evaluation for Instruction Following

Evaluating instruction-following in LLMs has received growing attention. Early benchmarks such as IFEval Zhou et al. ( 2023 ) rely on rule-based evaluation over verifiable constraints, later extended to multilingual and more complex real-world settings by Multi-IF He et al. ( 2024b ) and CELLO He et al. ( 2024a ) . IFBench Pyatkin et al. ( 2025 ) further introduces more constraint types. While objective, rule-based evaluation is limited to verifiable constraints. Alternatively, InfoBench Qin et al. ( 2024b ) proposes a decomposed evaluation method and leverages LLM judges for fine-grained verification. ComplexBench Wen et al. ( 2024 ) adopts a hybrid strategy combining rule-based and model-based method to enhance reliability. Beyond benchmarking, several recent works improve instruction-following via RL with rubric-based rewards Peng et al. ( 2025 ); Qin et al. ( 2025 ); Viswanathan et al. ( 2025 ); Liu et al. ( 2025a ) , where open-source LLM judges perform rubric-level verification to derive reward signals. Despite the widespread use of LLM judges in rubric-level instruction following evaluation, the reliablity of these judgments remains largely underexplored.

##### Meta-Evaluation for LLM Judges

As LLMs are increasingly used as evaluators, recent work has begun to meta-evaluate LLM judge reliability. RewardBench2 Malik et al. ( 2025 ) evaluates reward models on diverse preference pair. JudgeBench Tan et al. ( 2024 ) benchmarks LLM judges on challenging response pairs. JETTS Zhou et al. ( 2025 ) measures how reliably judges can select higher-quality responses during inference-time. VerifyBench Li et al. ( 2025b ) assesses reasoning verifiers across domains. In instruction following, LLMBar Zeng et al. ( 2023 ) is the first meta-evaluation benchmark. It constructs evaluation sets where one response follows the instruction and the other deviates subtly. ReIFE Liu et al. ( 2025b ) scales analysis to different judge configurations. Meta-evaluation also appears in some other works Ferraz et al. ( 2024 ); Qin et al. ( 2025 ) , but the lack of open-sourced data makes them opaque. Overall, existing efforts all evaluate LLM judge only at the response level, yielding a coarse-grained reliability assessment. We fills this gap with the first rubric-level meta-evaluation benchmark for instruction following.

## 3 RubricEval

This section details our data collection process, the annotation framework, and benchmark statistics.

### 3.1 Task Formulation

In rubric-based instruction-following evaluation, a judge is prompted with an instruction x x , a response y y , a rubric r r , and is required to produce a binary judgment j j indicating whether y y satisfies r r .

Formally, we define the rubric-level evaluation task as:

|  | j = IF_Rubric_Judge ​ ( x ⊕ y ⊕ r ) , j=\textit{IF\_Rubric\_Judge}(\,x\oplus y\oplus r\,), |  | (1) |
|---|---|---|---|


where j ∈ { 0 , 1 } j\in\{0,1\} denotes the judge’s binary judgment ( 1 1 if y y satisfies r r , and 0 otherwise), x x is the instruction, y y is the model response, and r r is a rubric—a specific criterion decomposed from the instruction to verify a particular aspect of instruction following. The operator ⊕ \oplus denotes prompt concatenation of x x , y y , and r r into a single input.

### 3.2 Data Collection

##### Instruction and Rubric Collection

To ensure diverse instruction coverage, we consider four widely used instruction categories in prior instruction-following benchmarks: Constrained , Compositional , Multi-turn , and System . Appendix A provides detailed definitions of the categories. We only focus on benchmarks that simultaneously provide instructions and corresponding rubrics.

For each category, we also collect instructions from multiple benchmarks when feasible (see Appendix J for the detailed source information and statistics). We believe this helps reduce source-specific bias. We directly derive rubrics from these benchmarks to ensure high rubric quality. These rubrics are all human-written or human-verified. Appendix B reports summary statistics of the collected instructions and rubrics.

##### Response Generation

To ensure response diversity, we randomly sample a model from an open-source LLM pool for each instruction. Prior work Zeng et al. ( 2023 ); Ren et al. ( 2025 ); Malik et al. ( 2025 ) creates failure instances via synthetic instruction–response mismatches. While efficient, these failures are artificial and may not generalize to real-world settings. Instead, we use the original model responses so that failures arise naturally. This captures realistic failure modes and reflects more realistic evaluation scenarios in practice. Details of the LLM pool are provided in Appendix F .

### 3.3 Label Annotation

The task of judging whether a response satisfies a rubric is quite challenging, as instruction-following judgments are often subjective. In addition, ambiguities in either the response or the rubric may lead to borderline cases. As a result, fully manual rubric-level annotation is hard to scale to the full benchmark. In this subsection, we aim to develop an automated labeling framework that is efficient at scale while producing high-confidence rubric-level labels.

#### 3.3.1 Human-Annotated Set

To design an automated labeling framework and validate its effectiveness, we construct a human-annotated reference set. It contains 506 instruction–response–rubric triplets sampled from LLM judges disagreement cases to ensure non-triviality. Then two human annotators label each triplet independently and resolve conflicts through discussion. The set is balanced across positive and negative labels. See Appendix D for construction details and statistics.

#### 3.3.2 Rubric Arbitration Framework

We first evaluate a range of candidate judge models on reference set. Considering overall performance and practical trade-offs, we select four high-performance models spanning multiple model families as base judges. We then compare different labeling strategies built on these base judges. Different model performance and selection strategy are in Appendix K .

As shown in Figure 3 , when four base judges unanimously agree, their consensus achieves 96.6% accuracy ( κ \kappa =0.93). However, for disputed cases, majority voting yields only 69.5% ( κ \kappa =0.39), and even the best-performing single judge (o3) achieves just 79.9% ( κ \kappa =0.60). Motivated by prior work showing that collaboration and meta-judging can improve evaluation reliability Qian et al. ( 2025 ); Wu et al. ( 2025 ) , we introduce a meta-review stage in which two meta-judges assess the rationales from multiple base judges and make their final judgment. We further enforce a consensus-based judgment rule to ensure high-quality labels. This strategy raises accuracy to 85.4% ( κ \kappa =0.69) on disputed cases.

Based on these findings, we propose the Rubric Arbitration Framework (RAF) , a three stage pipeline prioritizing label reliability over coverage—ambiguous instances are discarded rather than force-labeled. See Appendix M for case study.

##### Coarse-grained Filtering

Given the large number of rubrics, evaluating each one individually is costly. In this stage, four base judges evaluate the full rubric checklist for each instruction–response pair in a single pass. Rubrics with unanimous agreement are discarded; only disputed ones proceed to finer-grained stages. This procedure substantially alleviates the annotation burden in later stages

| Category | Benchmark | Easy | Hard | Total |
|---|---|---|---|---|
| Constrained | InfoBench_hard | 72 | 47 | 119 |
| ComplexBench | 54 | 46 | 100 |  |
| CFBench | 54 | 71 | 125 |  |
| AdvancedIF | 188 | 152 | 340 |  |
|  | Subtotal | 368 | 316 | 684 |
| Compositional | ComplexBench | 130 | 110 | 240 |
| Multi-Turn | StructFlowBench | 186 | 95 | 281 |
| AdvancedIF | 477 | 336 | 813 |  |
| Subtotal | 663 | 431 | 1,094 |  |
| System | SysBench | 160 | 217 | 377 |
| AdvancedIF | 713 | 378 | 1,091 |  |
| Subtotal | 873 | 595 | 1,468 |  |
| Total | 2,034 | 1,452 | 3,486 |  |

##### Fine-grained Re-evaluation

For disputed rubrics, we perform targeted rubric-level re-evaluation. Four base judge evaluates every disputed rubric in a single pass, providing both a judgment and supporting rationale. Rubrics reaching unanimous agreement form RubricEval-Easy ; others proceed to arbitration. This stage forces judges focus evaluation on every rubric, reducing cross-rubric interference.

##### Meta-Judges Arbitration

For persistently disputed rubrics, we invoke two meta-judges with strong reasoning capabilities. * * * We use OpenAI o3 and DeepSeek-R1 as meta-judges. Two meta-judges arbitrate by reviewing the base judges’ rationales and render independent judgments. When both agree, their consensus forms RubricEval-Hard ; others are discarded.

### 3.4 Human Validation

To verify the quality of our RAF-annotated labels, we conduct a human validation on a random sample of 160 rubric instances across subsets and instruction types. Two annotators independently label each instance, resolving disagreements through discussion.

Human-RAF agreement reaches 85.0% accuracy with Cohen’s κ \kappa = 0.702 , indicating substantial agreement. This confirms that RAF reliably approximates human judgment and can serve as trustworthy ground truth for meta-evaluation.

| Model | Constrained | Compositional | Multi-turn | System | Overall |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|---|
| BAcc | mF1 | BAcc | mF1 | BAcc | mF1 | BAcc | mF1 | BAcc | mF1 |  |
| \rowcolor gray!15 \cellcolor gray!15 RubricEval-Easy |  |  |  |  |  |  |  |  |  |  |
| Llama-3.1-8B-Instruct | 65.71 | 61.18 | 57.52 | 48.21 | 65.80 | 58.25 | 66.12 | 64.59 | 63.79 | 58.06 |
| Llama-3.3-70B-Instruct | 80.48 | 81.83 | 81.65 | 83.42 | 82.82 | 83.83 | 86.83 | 87.24 | 82.94 | 84.08 |
| Qwen2.5-7B-Instruct | 63.70 | 63.05 | 69.85 | 62.46 | 60.06 | 55.04 | 67.11 | 65.89 | 65.18 | 61.61 |
| Qwen2.5-32B-Instruct | 75.78 | 76.26 | 75.64 | 70.01 | 75.72 | 76.96 | 79.38 | 79.17 | 76.63 | 75.60 |
| QwQ-32B | 85.26 | 85.67 | 79.17 | 73.80 | 77.00 | 77.12 | 80.29 | 80.38 | 80.43 | 79.24 |
| Qwen3-8B | 79.22 | 80.51 | 84.06 | 81.68 | 83.40 | 83.65 | 80.27 | 80.74 | 81.74 | 81.65 |
| Qwen3-235B-A22B-2507 | 87.24 | 88.56 | 93.98 | 92.44 | 90.59 | 90.84 | 87.65 | 87.81 | 89.87 | 89.91 |
| gpt-oss-120b | 89.84 | 87.24 | 86.24 | 81.65 | 91.29 | 89.65 | 90.83 | 90.02 | 89.55 | 87.14 |
| GPT-4o-2024-11-20 | 82.15 | 80.88 | 85.34 | 81.42 | 85.80 | 82.77 | 84.33 | 83.37 | 84.41 | 82.11 |
| o3-mini | 85.66 | 84.67 | 85.26 | 84.63 | 88.63 | 89.40 | 89.12 | 89.15 | 87.17 | 86.96 |
| \rowcolor gray!15 \cellcolor gray!15 RubricEval-Hard |  |  |  |  |  |  |  |  |  |  |
| Qwen3-235B-A22B-2507 | 62.68 | 53.31 | 60.95 | 49.37 | 69.28 | 61.80 | 62.48 | 57.28 | 63.85 | 55.44 |
| gpt-oss-120b | 80.00 | 76.81 | 61.83 | 54.78 | 82.32 | 79.74 | 79.39 | 78.57 | 75.89 | 72.48 |
| GPT-4o-2024-11-20 | 48.51 | 41.04 | 67.99 | 53.27 | 57.85 | 56.20 | 49.54 | 48.21 | 55.97 | 49.68 |
| o3-mini | 71.88 | 64.78 | 69.97 | 55.86 | 76.63 | 70.03 | 62.48 | 57.28 | 70.24 | 61.99 |
| GPT-4.1 | 64.91 | 55.67 | 52.92 | 44.60 | 74.39 | 71.24 | 60.09 | 57.31 | 63.08 | 57.21 |
| GPT-5.1 | 71.90 | 69.48 | 74.92 | 63.43 | 72.26 | 71.75 | 70.03 | 68.27 | 72.28 | 68.23 |
| o3 | 87.35 | 82.22 | 80.97 | 67.09 | 88.50 | 87.20 | 82.42 | 79.89 | 84.81 | 79.10 |
| Claude-Sonnet-4.5 | 58.70 | 50.63 | 52.04 | 39.39 | 59.75 | 55.76 | 52.11 | 47.88 | 55.65 | 48.41 |
| Gemini-3-Flash | 77.91 | 75.30 | 84.43 | 75.18 | 82.43 | 81.06 | 74.93 | 76.14 | 79.93 | 76.92 |
| Gemini-3-Pro | 81.56 | 78.08 | 83.93 | 76.22 | 87.77 | 84.53 | 78.89 | 79.22 | 83.04 | 79.51 |
| Deepseek-v3.2 | 53.48 | 50.08 | 59.85 | 52.28 | 64.41 | 60.90 | 58.95 | 55.67 | 59.17 | 54.73 |
| Deepseek-r1-0528 | 68.62 | 62.41 | 80.47 | 66.13 | 71.92 | 66.76 | 73.18 | 69.95 | 73.55 | 66.31 |

### 3.5 Dataset Statistics

Table 1 summarizes the overall statistics of our constructed RubricEval . In total, the benchmark contains 1,989 instructions and 3,486 rubric-level instances, including 2,034 Easy and 1,452 Hard instances. A detailed breakdown by source benchmark is provided in Appendix G .

To support fine-grained analysis of rubric-level judge performance, we construct a rubric taxonomy for RubricEval . This rubric taxonomy has 13 fine-grained categories, organized into 4 high-level dimensions: Content , Form , Quality , and Style . This taxonomy helps us view finer-grained rubric distributions.

As shown in Figure 4 , the distribution of instances exhibits a long-tail pattern reflecting a natural distribution of real-world tasks. And Appendix E show the t-SNE visualization of rubric instances.

The detailed category definitions and categorization procedure are provided in Appendix L . Appendix I further summarizes the distribution by high-level dimensions (and their proportions).

## 4 Experiments

### 4.1 Experimental Setup

##### Metrics.

Rubric-level judging is a binary classification task. We report Balanced Accuracy and Macro F1 to account for class imbalance.

##### Protocol.

When conducting evaluation, we ask judges to first provide a rationale, then give the final judgment. We think this protocol better reflects the judge’s true evaluation capability. We follow the original evaluation prompting guidelines provided by the corresponding source benchmarks. Prompt for evaluating Constrained rubric is in Appendix N .

##### Evaluated Models.

We evaluate a diverse set of judge models covering both open-source and proprietary LLMs, spanning multiple model families and parameter scales. We report results on both the Easy and Hard splits, with an overlapping subset of models evaluated on both for direct comparison.

### 4.2 Main Results

| Granularity | Reasoning | Constrained | Compositional | Multi-turn | System | Overall |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Qwen | GPT | Qwen | GPT | Qwen | GPT | Qwen | GPT | Qwen | GPT |  |  |
| Rubric-level | ✗ | 62.55 | 69.99 | 75.62 | 78.37 | 68.09 | 74.62 | 69.55 | 78.89 | 68.95 | 75.47 |
| ✓ | 74.19 | 82.90 | 83.17 | 80.83 | 76.80 | 83.48 | 75.34 | 81.45 | 77.38 (+8.4) | 82.17 (+6.7) |  |
| Checklist-level | ✗ | 54.06 | 60.80 | 72.38 | 68.21 | 53.39 | 56.11 | 63.98 | 68.48 | 60.95 | 63.40 |
| ✓ | 66.71 | 69.59 | 77.06 | 74.60 | 60.90 | 57.88 | 74.94 | 79.67 | 69.90 (+9.0) | 70.44 (+7.0) |  |

Table 3.4 reports the main results on RubricEval .

##### Overall Performance.

The results reveal a wide performance spectrum across evaluated models. On the Easy subset, small open-source models such as Qwen2.5-7B-Instruct achieves only around 65% balanced accuracy, while stronger models like Qwen3-235B and gpt-oss-120b reach around 90%. On the Hard split, even commercial models struggle considerably. For instance, GPT-4o achieves merely 55.97% balanced accuracy, and Claude-Sonnet-4.5 reaches 55.65%, indicating that hard rubric cases remain challenging even for strong LLMs. These findings underscore the necessity of rubric-level meta-evaluation: rubric-level judging remains far from solved . Practically, deploying small open-source models as judges Qin et al. ( 2025 ) may produce noisy or misleading signals in applications like rubric-based RL. Meanwhile, GPT-4o, the widely-adopted evaluator in instruction-following benchmarks Wen et al. ( 2024 ); Li et al. ( 2025a ) , may introduce systematic biases, potentially affecting the reliability of the reported scores.

##### From Easy to Hard : A Significant Performance Gap.

We evaluate the same four models on both Easy and Hard subsets † † † We evaluate these four models: Qwen3-235B-A22B-2507, gpt-oss-120b, GPT-4o, and o3-mini , enabling a direct comparison of subset difficulty. Consistently, all four exhibit substantial performance drop from Easy to Hard : GPT-4o declines by 28.4 BAcc (84.41% → \rightarrow 55.97%), Qwen3-235B by 26.0 points (89.87% → \rightarrow 63.85%), and even the relatively robust gpt-oss-120b drops by 13.7 points. This performance degradation confirms that our data construction pipeline produces two practical subsets that vary in difficulty. Hard subset genuinely captures challenging cases. The two-tier design also facilitates more fine-grained evaluation across a broader set of judges.

##### Performance Varies Across Instruction Types.

Judge performance also varies across instruction categories. This indicates that rubric verification difficulty depends strongly on the type of the underlying instruction. Compositional instructions prove most challenging, with most models showing their lowest mF1 on this type. This is likely because judges are required to accurately parse the underlying structure and ground each rubric to specific parts of the response, which is more error-prone than checking surface-level constraints. Conversely, Multi-turn instructions tend to be easier, possibly because conversational history provides additional cues for rubric verification. Constrained and System instructions show moderate difficulty, though some models underperform notably.

## 5 Analysis

In this section, we study different evaluation paradigms that vary in granularity and reasoning, as well as common error patterns.

### 5.1 Does Evaluation Paradigm Matter?

Table 3 compares four evaluation paradigms along two dimensions: granularity and reasoning . For granularity, checklist-level evaluates all rubrics in a single pass, while rubric-level verifies each rubric independently with a separate call. For reasoning, we compare direct judgment versus generating a rationale before the final verdict.

##### Rubric-Level Evaluation is More Accurate.

As shown in Table 3 , rubric-level evaluation consistently outperforms checklist-level evaluation across both models and all instruction types. With reasoning enabled, rubric-level achieves 77.38% (Qwen) and 82.17% (GPT) BAcc, while checklist-level achieves only 69.90% and 70.44%—a gap of 7–12 points. This pattern holds across all instruction types and on both Easy and Hard subsets (see Appendix H ).

##### Reasoning Consistently Helps.

Explicit reasoning also significantly enhances judging accuracy. Across both granularity settings and all model types, enabling reasoning consistently leads to performance gains. Specifically, in the rubric-level setting, Qwen and GPT achieve absolute improvements of 8.4% and 6.7% in BAcc, respectively. Similar trends are observed in the checklist-level setting, with gains of 9.0% and 7.0%.

### 5.2 Trade-offs

For the first finding, a likely explanation is that checklist-level evaluation forces judges to verify multiple rubrics in a single pass, increasing cognitive load and the risk of missing individual rubrics. Rubric-level evaluation isolates each decision, reducing interference and improving precision.

For the second finding, reasoning likely helps by forcing judges to ground their decisions in evidence rather than relying on intuition, thereby reducing unreliable judgments.

However, both rubric-level evaluation and reasoning come at a cost. Rubric-level evaluation requires a separate API call for each rubric, significantly increasing latency and expense. Reasoning further adds to output token costs. This creates a reliability–efficiency trade-off : checklist-level without reasoning is fast and cheap but less accurate, while rubric-level with reasoning is more reliable but costlier. Some existing benchmarks and reward methods adopt the former for efficiency—our results suggest this may compromise evaluation reliability.

### 5.3 Inter-Judge Analysis

We further investigate whether evaluation paradigm affects inter-judge consistency. Using CFBench Zhang et al. ( 2025a ) as a testbed, we evaluate responses from Qwen2.5-7B-Instruct with three judges of varying performance levels on our benchmark (GPT-4o, Qwen3-235B, and GPT-5.1) under four evaluation paradigms.

As shown in Figure 5 , the vanilla evaluation paradigm (checklist-level without reasoning) exhibits substantial inter-judge variance: CSR scores range from 55% (GPT-5.1) to 80% (GPT-4o)—a gap of 25 points for the same model responses. This suggests that judge selection alone can dramatically affect benchmark scores and potentially lead to conflicting conclusions about model performance.

As we move toward more fine-grained and reasoning-augmented paradigms, inter-judge variance decreases. With rubric-level evaluation and reasoning, the three judges converge noticeably: scores range from 62% to 74%, reducing the gap to 12 points. However, non-trivial differences still remain, reflecting inherent capability gaps among judges. This suggests that rubric-level evaluation with reasoning improves both accuracy and inter-judge consistency, but cannot fully eliminate variance introduced by judge capability differences, highlighting the importance of our rubric-level meta-evaluation efforts.

| Rubric Type | Qwen3 | gpt-oss | GPT-4o | o3-mini |
|---|---|---|---|---|
| Content | 76.9 | 86.1 | 72.2 | 81.0 |
| Content Inclusion | 77.1 | 86.8 | 72.3 | 80.6 |
| Content Exclusion | 80.4 | 87.8 | 71.4 | 83.9 |
| Topic Scope | 72.9 | 83.5 | 72.9 | 78.4 |
| Form | 77.6 | 87.5 | 67.0 | 87.3 |
| Quantity Limit | 78.6 | 86.6 | 68.7 | 88.6 |
| Format Structure | 75.9 | 86.1 | 66.8 | 84.9 |
| Ordering Sequence | 80.0 | 94.7 | 61.3 | 89.3 |
| Quality | 75.6 | 84.5 | 70.8 | 76.6 |
| Quality Requirements | 74.8 | 83.2 | 72.5 | 75.2 |
| Conditional Logic | 78.0 | 84.8 | 71.8 | 80.9 |
| Task Completion | 73.5 | 86.6 | 66.3 | 72.4 |
| Style | 79.2 | 86.6 | 74.7 | 78.5 |
| Style Tone | 79.4 | 87.0 | 79.0 | 79.0 |
| Language Linguistics | 75.8 | 89.4 | 70.2 | 83.9 |
| Multi-turn Coherence | 91.0 | 89.0 | 75.6 | 74.2 |
| Role Persona | 71.1 | 81.6 | 72.0 | 77.6 |
| Overall | 77.5 | 86.2 | 71.2 | 81.4 |

### 5.4 Error Analysis

Table 4 presents the accuracy of four judges † † footnotetext: Qwen3 refers to Qwen3-235B-A22B-Instruct-2507, gpt-oss refers to gpt-oss-120b, and GPT-4o refers to GPT-4o-2024-11-20. across fine-grained rubric types in RubricEval , grouped into four high-level dimensions.

##### Common Failure Modes.

We identify five rubric types where most judges underperform: Topic Scope , Format Structure , Quality Requirements , Task Completion , and Role Persona . These rubrics typically require strict evidence checking or involve subjective interpretation.

Format Structure and Role Persona are consistently difficult across all judges—the former reveals that format structure verification is relatively hard for llm judges and may benefit from rule-based verification methods. While the latter indicates that persona maintenance remains ambiguous for judges to assess, where correctness is not always clearly defined and borderline cases may exist. The other three types ( Topic Scope , Quality Requirements , Task Completion ) all lack clear-cut criteria, making consistent judgment difficult.

##### Model-Specific Observations.

We also observe clear model-specific strengths and weaknesses. GPT-4o performs poorly on Form rubrics (67.0%), especially on Ordering/Sequence (61.3%), suggesting difficulty in verifying strict ordering requirements. In contrast, Qwen3 performs strongly on Multi-turn Coherence (91.0%), indicating better handling of dialogue consistency across turns. The gpt-oss judge shows the most balanced performance across dimensions overall, although it still underperforms on Role Persona , which remains challenging across models.

## 6 Conclusion

We present RubricEval , the first rubric-level meta-evaluation benchmark for instruction following, covering four instruction categories with Easy and Hard splits. We design and use the Rubric Arbitration Framework (RAF) to produce high-confidence labels at scale. Our experiments reveal that rubric-level judging remains challenging. Even widely adopted judges like GPT-4o and Claude-4.5 struggle on hard instances, raising concerns about current rubric-based evaluation practices. We also find that rubric-level evaluation outperforms checklist-level evaluation, explicit reasoning improves judging accuracy, and both together enhance inter-judge consistency. Through error analysis with our rubric taxonomy, we identify common failure modes, providing guidance for future judge development and benchmark design. We hope RubricEval serves as a foundation for developing more reliable LLM judges for instruction following, ultimately advancing trustworthy evaluation in both research and practice.

## Limitations

Our work has several limitations: (1) RubricEval focuses on four main instruction categories, which may not fully cover all instruction-following scenarios in practice. Other instruction types, such as agent-related or domain-specific instructions, are not included. (2) The Rubric Arbitration Framework (RAF) relies on LLM judges and reasoning models to produce high-confidence reference labels. Although human validation shows high agreement with RAF labels, the remaining cases may still contain annotation noise. Additionally, rubrics that fail to reach consensus between meta-judges are discarded to prioritize label quality. While the resulting benchmark remains sufficiently large and discriminative, some genuinely hard cases may still be excluded. (3) We focus on rubric-level binary judgments, which is the most common setting in current benchmarks. Other evaluation formats, such as Likert-scale ratings or comparative judgments, are beyond the scope of our work.

## References

- J. Achiam, S. Adler, S. Agarwal, L. Ahmad, I. Akkaya, F. L. Aleman, D. Almeida, J. Altenschmidt, S. Altman, S. Anadkat, et al. (2023) Gpt-4 technical report . arXiv preprint arXiv:2303.08774 . Cited by: §1 .

- K. An, L. Sheng, G. Cui, S. Si, N. Ding, Y. Cheng, and B. Chang (2025) UltraIF: advancing instruction following from the wild . arXiv preprint arXiv:2502.04153 . Cited by: Appendix C , §1 .

- R. K. Arora, J. Wei, R. S. Hicks, P. Bowman, J. Quiñonero-Candela, F. Tsimpourlas, M. Sharman, M. Shah, A. Vallone, A. Beutel, et al. (2025) Healthbench: evaluating large language models towards improved human health . arXiv preprint arXiv:2505.08775 . Cited by: Appendix C .

- G. Bai, J. Liu, X. Bu, Y. He, J. Liu, Z. Zhou, Z. Lin, W. Su, T. Ge, B. Zheng, et al. (2024) Mt-bench-101: a fine-grained benchmark for evaluating large language models in multi-turn dialogues . arXiv preprint arXiv:2402.14762 . Cited by: Appendix A .

- T. P. Ferraz, K. Mehta, Y. Lin, H. Chang, S. Oraby, S. Liu, V. Subramanian, T. Chung, M. Bansal, and N. Peng (2024) Llm self-correction with decrim: decompose, critique, and refine for enhanced following of instructions with multiple constraints . arXiv preprint arXiv:2410.06458 . Cited by: §2 .

- A. Gunjal, A. Wang, E. Lau, V. Nath, Y. He, B. Liu, and S. Hendryx (2025) Rubrics as rewards: reinforcement learning beyond verifiable domains . arXiv preprint arXiv:2507.17746 . Cited by: Appendix C , §1 .

- Q. He, J. Zeng, W. Huang, L. Chen, J. Xiao, Q. He, X. Zhou, J. Liang, and Y. Xiao (2024a) Can large language models understand real-world complex instructions? . In Proceedings of the AAAI Conference on Artificial Intelligence , Vol. 38 , pp. 18188–18196 . Cited by: §2 .

- Y. He, D. Jin, C. Wang, C. Bi, K. Mandyam, H. Zhang, C. Zhu, N. Li, T. Xu, H. Lv, et al. (2024b) Multi-if: benchmarking llms on multi-turn and multilingual instructions following . arXiv preprint arXiv:2410.15553 . Cited by: §2 .

- Y. He, W. Li, H. Zhang, S. Li, K. Mandyam, S. Khosla, Y. Xiong, N. Wang, X. Peng, B. Li, et al. (2025) AdvancedIF: rubric-based benchmarking and reinforcement learning for advancing llm instruction following . arXiv preprint arXiv:2511.10507 . Cited by: Table 10 , Table 10 , Table 10 .

- Z. Huang, Y. Zhuang, G. Lu, Z. Qin, H. Xu, T. Zhao, R. Peng, J. Hu, Z. Shen, X. Hu, et al. (2025) Reinforcement learning with rubric anchors . arXiv preprint arXiv:2508.12790 . Cited by: Appendix C , §1 .

- J. Li, J. Li, Y. Wang, Y. Chang, and Y. Wu (2025a) Structflowbench: a structured flow benchmark for multi-turn instruction following . arXiv preprint arXiv:2502.14494 . Cited by: Appendix A , Table 10 , §4.2 .

- X. Li, X. Li, S. Hu, Y. Guo, and W. Zhang (2025b) Verifybench: a systematic benchmark for evaluating reasoning verifiers across domains . arXiv preprint arXiv:2507.09884 . Cited by: §2 .

- G. Lior, A. Yehudai, A. Gera, and L. Ein-Dor (2025) Wildifeval: instruction following in the wild . arXiv preprint arXiv:2503.06573 . Cited by: Appendix A .

- W. Liu, Z. Guo, M. Xie, J. Xu, Z. Huang, M. Tian, J. Xu, M. Wu, X. Wang, C. Lv, et al. (2025a) RECAST: strengthening llms’ complex instruction following with constraint-verifiable data . arXiv preprint arXiv:2505.19030 . Cited by: §2 .

- Y. Liu, K. Shi, A. R. Fabbri, Y. Zhao, P. Wang, C. Wu, S. Joty, and A. Cohan (2025b) ReIFE: re-evaluating instruction-following evaluation . In Proceedings of the 2025 Conference of the Nations of the Americas Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers) , pp. 12247–12287 . Cited by: §2 .

- S. Malik, V. Pyatkin, S. Land, J. Morrison, N. A. Smith, H. Hajishirzi, and N. Lambert (2025) RewardBench 2: advancing reward model evaluation . arXiv preprint arXiv:2506.01937 . Cited by: §1 , §2 , §3.2 .

- L. Ouyang, J. Wu, X. Jiang, D. Almeida, C. Wainwright, P. Mishkin, C. Zhang, S. Agarwal, K. Slama, A. Ray, et al. (2022) Training language models to follow instructions with human feedback . Advances in neural information processing systems 35 , pp. 27730–27744 . Cited by: §1 .

- H. Peng, Y. Qi, X. Wang, B. Xu, L. Hou, and J. Li (2025) VerIF: verification engineering for reinforcement learning in instruction following . arXiv preprint arXiv:2506.09942 . Cited by: Appendix C , §1 , §2 .

- V. Pyatkin, S. Malik, V. Graf, H. Ivison, S. Huang, P. Dasigi, N. Lambert, and H. Hajishirzi (2025) Generalizing verifiable instruction following . arXiv preprint arXiv:2507.02833 . Cited by: §2 .

- Y. Qian, S. Zhang, Y. Zhou, H. Ding, D. Socolinsky, and Y. Zhang (2025) Enhancing llm-as-a-judge via multi-agent collaboration . Cited by: §3.3.2 .

- Y. Qin, T. Zhang, Y. Shen, W. Luo, H. Sun, Y. Zhang, Y. Qiao, W. Chen, Z. Zhou, W. Zhang, et al. (2024a) SysBench: can large language models follow system messages? . arXiv preprint arXiv:2408.10943 . Cited by: Appendix A , Table 10 .

- Y. Qin, K. Song, Y. Hu, W. Yao, S. Cho, X. Wang, X. Wu, F. Liu, P. Liu, and D. Yu (2024b) Infobench: evaluating instruction following ability in large language models . arXiv preprint arXiv:2401.03601 . Cited by: Appendix A , Table 10 , §1 , §2 .

- Y. Qin, G. Li, Z. Li, Z. Xu, Y. Shi, Z. Lin, X. Cui, K. Li, and X. Sun (2025) Incentivizing reasoning for advanced instruction-following of large language models . arXiv preprint arXiv:2506.01413 . Cited by: §2 , §2 , §4.2 .

- Q. Ren, J. Zeng, Q. He, J. Liang, Y. Xiao, W. Zhou, Z. Sun, and F. Yu (2025) Step-by-step mastery: enhancing soft constraint following ability of large language models . arXiv preprint arXiv:2501.04945 . Cited by: §3.2 .

- S. Tan, S. Zhuang, K. Montgomery, W. Y. Tang, A. Cuadron, C. Wang, R. A. Popa, and I. Stoica (2024) Judgebench: a benchmark for evaluating llm-based judges . arXiv preprint arXiv:2410.12784 . Cited by: §2 .

- V. Viswanathan, Y. Sun, S. Ma, X. Kong, M. Cao, G. Neubig, and T. Wu (2025) Checklists are better than reward models for aligning language models . arXiv preprint arXiv:2507.18624 . Cited by: §2 .

- C. Wang, L. Wen, S. Jia, X. Zhang, and L. Xu (2025) Light-if: endowing llms with generalizable reasoning via preview and self-checking for complex instruction following . arXiv preprint arXiv:2508.03178 . Cited by: §1 .

- B. Wen, P. Ke, X. Gu, L. Wu, H. Huang, J. Zhou, W. Li, B. Hu, W. Gao, J. Xu, et al. (2024) Benchmarking complex instruction-following with multiple constraints composition . Advances in Neural Information Processing Systems 37 , pp. 137610–137645 . Cited by: Appendix A , Table 10 , Table 10 , §1 , §2 , §4.2 .

- T. Wu, W. Yuan, O. Golovneva, J. Xu, Y. Tian, J. Jiao, J. E. Weston, and S. Sukhbaatar (2025) Meta-rewarding language models: self-improving alignment with llm-as-a-meta-judge . In Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing , pp. 11548–11565 . Cited by: §3.3.2 .

- Z. Zeng, J. Yu, T. Gao, Y. Meng, T. Goyal, and D. Chen (2023) Evaluating large language models at evaluating instruction following . arXiv preprint arXiv:2310.07641 . Cited by: §1 , §2 , §3.2 .

- T. Zhang, C. Zhu, Y. Shen, W. Luo, Y. Zhang, H. Liang, F. Yang, M. Lin, Y. Qiao, W. Chen, et al. (2025a) Cfbench: a comprehensive constraints-following benchmark for llms . In Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers) , pp. 32926–32944 . Cited by: Appendix A , Table 10 , §1 , §5.3 .

- X. Zhang, H. Yu, C. Fu, F. Huang, and Y. Li (2025b) Iopo: empowering llms with complex instruction following via input-output preference optimization . In Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers) , pp. 22185–22200 . Cited by: Appendix A , §1 .

- Z. Zhang, S. Li, Z. Zhang, X. Liu, H. Jiang, X. Tang, Y. Gao, Z. Li, H. Wang, Z. Tan, et al. (2025c) IHEval: evaluating language models on following the instruction hierarchy . arXiv preprint arXiv:2502.08745 . Cited by: Appendix A .

- J. Zhou, T. Lu, S. Mishra, S. Brahma, S. Basu, Y. Luan, D. Zhou, and L. Hou (2023) Instruction-following evaluation for large language models . arXiv preprint arXiv:2311.07911 . Cited by: §1 , §2 .

- Y. Zhou, A. Xu, P. Wang, C. Xiong, and S. Joty (2025) Evaluating judges as evaluators: the jetts benchmark of llm-as-judges as test-time scaling evaluators . arXiv preprint arXiv:2504.15253 . Cited by: §1 , §2 .

## Appendix A Instruction Category Definitions

We collect instructions in RubricEval from four widely used categories. Below we provide detailed definitions for each category.

##### Constrained Instructions.

Constrained instructions are single-turn instructions that contain multiple constraints that model must satisfy simultaneously during generation. For example, an instruction may require the response to simultaneously include specific content, follow a specified format, and output in a style.

This type of instruction is widely used in instruction-following evaluation, as it directly tests a model’s ability to handle multiple requirements in parallel. Representative benchmarks include InfoBench Qin et al. ( 2024b ) , CFBench Zhang et al. ( 2025a ) , TRACE Zhang et al. ( 2025b ) and Wildifeval Lior et al. ( 2025 ) .

Evaluation difficulty for constrained instructions is moderate to high, as judges must verify each constraint independently while ensuring no constraint is overlooked.

##### Compositional Instructions.

Compositional instructions contain complex topological structures with logical dependencies among constraints, such as conditional branches(Selection), sequential chains(Chain), and conjunctive relations(And).

This type of instruction tests a model’s ability to parse and execute logically structured requirements, which is essential for complex real-world tasks. ComplexBench Wen et al. ( 2024 ) is the primary benchmark focusing on this instruction type.

Evaluation difficulty is high, as judges must correctly parse the underlying logical structure and ground each rubric to the corresponding part of the response.

##### Multi-turn Instructions.

Multi-turn instructions involve conversational interactions spanning multiple dialogue turns. The model must maintain consistency, track context, and follow constraints that may evolve or accumulate across turns.

This type of instruction reflects realistic conversational AI scenarios, where users interact with models through extended dialogues. Related benchmarks include MT-Bench-101 Bai et al. ( 2024 ) and StructFlowBench Li et al. ( 2025a ) .

Evaluation difficulty is moderate, as conversational history provides additional context for rubric verification. However, judges must correctly handle cross-turn references and ensure coherence throughout the conversation.

##### System Instructions.

System instructions include a system prompt that defines the model’s behavior, role, or constraints at the conversation level. The model is expected to strictly adhere to the system prompt throughout its responses.

This type of instruction is prevalent in deployed AI systems, where system prompts are used to customize model behavior for specific applications. Benchmarks such as SysBench Qin et al. ( 2024a ) and IHEval Zhang et al. ( 2025c ) focus on system-prompt following evaluation.

Evaluation difficulty varies depending on the specificity of the system prompt. Verifying adherence to abstract role definitions (e.g., “act as a helpful assistant”) is harder than checking concrete constraints (e.g., “always respond in JSON”).

## Appendix B Statistics of the original instructions and rubrics

| Type | Benchmark | #Inst. | #Rub. | R/I | H. |
|---|---|---|---|---|---|
| Constrained | InfoBench_hard | 228 | 1,453 | 6.37 | ✓ |
| ComplexBench | 238 | 1,027 | 4.32 | ✓ |  |
| CFBench | 243 | 1,035 | 4.26 | ✓ |  |
| AdvancedIF | 243 | 1,816 | 7.47 | ✓ |  |
| Compositional | ComplexBench | 435 | 1,651 | 4.49 | ✓ |
| Multi-Turn | StructFlowBench | 643 | 1,775 | 2.76 | ✓ |
| AdvancedIF | 736 | 4,478 | 6.08 | ✓ |  |
| System | SysBench | 1,000 | 2,478 | 2.48 | ✓ |
| AdvancedIF | 507 | 4,972 | 9.81 | ✓ |  |
| Total | 4,273 | 20,685 | 4.84 | ✓ |  |

Table 5 summarizes the instruction and rubric sources used in RubricEval . We collect from multiple benchmarks across four instruction categories, totaling 4,273 instructions and 20,685 rubrics. All rubrics are human-crafted or human-verified.

## Appendix C Rubric-based Evaluation

Rubric-based evaluation has been widely adopted across various domains beyond instruction following. For example, HealthBench Arora et al. ( 2025 ) employs rubric-level verification to evaluate medical question answering, and similar approaches have been applied to code generation, summarization, and other complex tasks. In this paradigm, complex evaluation criteria are decomposed into a set of fine-grained rubrics, each specifying a particular requirement. An LLM judge then verifies whether the response satisfies each rubric independently, and the results are aggregated into an overall score.

Beyond benchmarking, rubric-level judgments are increasingly used as supervision or reward signals in model training Gunjal et al. ( 2025 ); Huang et al. ( 2025 ); Peng et al. ( 2025 ); An et al. ( 2025 ) . Compared to binary or scalar response-level rewards, rubric-based rewards enable models to receive fine-grained feedback and partial credit for partially correct responses, which can lead to more effective learning.

Compared to holistic response-level evaluation, rubric-based evaluation offers several advantages. First, it is particularly well-suited for tasks that are inherently subjective or multi-faceted. By breaking down holistic evaluation into smaller, more focused decisions, rubric-based evaluation reduces ambiguity and provides more interpretable feedback, as it explicitly identifies which requirements are satisfied and which are not.

However, this paradigm also introduces new challenges. The reliability of the final score depends on the accuracy of each individual rubric judgment. Errors in rubric-level verification can propagate through aggregation and bias downstream applications, making judge reliability a critical concern. This motivates the need for rigorous meta-evaluation of LLM judges at the rubric level, which is the focus of our work.

## Appendix D Human Set Construction and Statistics

We construct a human-labeled reference set by collecting instances on which four LLM judges disagree during evaluation, as such cases are typically non-trivial. Two annotators independently label each triplet by examining the instruction, the response, and the target rubric. For triplets with conflicting annotations, the annotators discuss the case and reach a consensus label, which we treat as the final ground truth.

To further increase the dataset size while maintaining a balanced distribution of positive and negative labels, we apply a rewriting-based data augmentation strategy. Specifically, for a triplet labeled as True (1) under a given rubric, we prompt GPT-4.1 to minimally edit the response to violate that rubric; for a triplet labeled as False (0), we prompt GPT-4.1 to minimally edit the response to satisfy the rubric. The rewriting prompt is conditioned on the rubric type to ensure the edit targets the relevant requirement.

All rewritten responses are manually verified by annotators to ensure that the edit is effective and valid with respect to the target rubric. We retain only the verified rewritten examples in the final augmented reference set.

| Subset | Samples | Judge Inst. | Pos. | Neg. |
|---|---|---|---|---|
| Right-to-Wrong | 120 | 240 | 120 | 120 |
| Wrong-to-Right | 133 | 266 | 133 | 133 |
| Total | 253 | 506 | 253 | 253 |

## Appendix E T-SNE visualization of rubrics

Figure 6 shows that several categories form relatively compact clusters—e.g., [Multi-turn Coherence] ( light green ), [Quantity Limit] ( purple ), and [Format Structure] ( light orange )—indicating consistent patterns within these rubric types.

| Model | Family | Total | Active | Arch. | Mode |
|---|---|---|---|---|---|
| Qwen3-4B-Instruct-2507 | Qwen | 4B | 4B | Dense | Instruct |
| Qwen3-4B-Thinking-2507 | Qwen | 4B | 4B | Dense | Thinking |
| Qwen2.5-7B-Instruct | Qwen | 7B | 7B | Dense | Instruct |
| Llama-3.1-8B-Instruct | Llama | 8B | 8B | Dense | Instruct |
| DeepSeek-R1-0528-Qwen3-8B | Qwen+DeepSeek | 8B | 8B | Dense | Thinking |
| Qwen3-30B-A3B-Instruct-2507 | Qwen | 30B | 3B | MoE | Instruct |
| Qwen3-30B-A3B-Thinking-2507 | Qwen | 30B | 3B | MoE | Thinking |
| Qwen2.5-32B-Instruct | Qwen | 32B | 32B | Dense | Instruct |
| Llama-3.3-70B-Instruct | Llama | 70B | 70B | Dense | Instruct |

## Appendix F Model Pool for Response Generation

We list the models used to generate responses in RubricEval . The pool spans diverse model families, scales, and architectures to ensure response diversity.

| Category | Source Benchmark | # Instr. | # Rubric-Level Labels | Category Summary |  |  |  |  |
|---|---|---|---|---|---|---|---|---|
| Easy | Hard | Total | Easy | Hard | Total |  |  |  |
| Constrained | InfoBench_hard | 95 | 72 | 47 | 119 | 368 | 316 | 684 |
| ComplexBench | 80 | 54 | 46 | 100 |  |  |  |  |
| CFBench | 112 | 54 | 71 | 125 |  |  |  |  |
| AdvancedIF | 219 | 188 | 152 | 340 |  |  |  |  |
| Compositional | ComplexBench | 188 | 130 | 110 | 240 | 130 | 110 | 240 |
| Multi-Turn | StructFlowBench | 229 | 186 | 95 | 281 | 663 | 431 | 1,094 |
| AdvancedIF | 424 | 477 | 336 | 813 |  |  |  |  |
| System | SysBench | 282 | 160 | 217 | 377 | 873 | 595 | 1,468 |
| AdvancedIF | 360 | 713 | 378 | 1,091 |  |  |  |  |
| Total | RubricEval (Ours) | 1,989 | 2,034 | 1,452 | 3,486 | 2,034 | 1,452 | 3,486 |

## Appendix G Dataset Statistics

Table 8 provides a detailed breakdown of RubricEval statistics by source benchmark, including the number of instructions and rubric instances in each split.

| Granularity | Reasoning | Constrained | Compositional | Multi-turn | System | Overall |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Qwen | GPT | Qwen | GPT | Qwen | GPT | Qwen | GPT | Qwen | GPT |  |  |
| \rowcolor gray!10 Easy Subset |  |  |  |  |  |  |  |  |  |  |  |
| Rubric-level | w/o CoT | 70.01 | 84.05 | 81.50 | 85.49 | 82.28 | 85.74 | 84.81 | 90.71 | 79.65 | 86.50 |
| w/ CoT | 86.44 | 97.89 | 91.65 | 96.99 | 88.75 | 94.88 | 85.13 | 93.13 | 87.99 | 95.72 |  |
| Checklist-level | w/o CoT | 53.07 | 67.45 | 79.17 | 72.86 | 56.83 | 56.82 | 74.83 | 79.07 | 65.98 | 69.05 |
| w/ CoT | 76.18 | 81.08 | 80.60 | 86.99 | 67.86 | 61.88 | 84.08 | 89.04 | 77.18 | 79.75 |  |
| \rowcolor gray!10 Hard Subset |  |  |  |  |  |  |  |  |  |  |  |
| Rubric-level | w/o CoT | 58.45 | 58.42 | 47.85 | 52.31 | 52.18 | 54.24 | 45.56 | 58.97 | 51.01 | 55.99 |
| w/ CoT | 64.19 | 70.87 | 62.93 | 51.93 | 65.75 | 66.92 | 58.31 | 63.18 | 62.80 | 63.23 |  |
| Checklist-level | w/o CoT | 56.57 | 53.99 | 43.75 | 42.01 | 46.54 | 52.79 | 48.97 | 53.20 | 48.96 | 50.50 |
| w/ CoT | 60.58 | 59.80 | 54.51 | 56.77 | 50.92 | 52.21 | 64.42 | 67.35 | 57.61 | 59.03 |  |

## Appendix H Evaluation Paradigm Performance on Easy and Hard Split

Table G reports evaluation paradigm comparison results separately on Easy and Hard splits, complementing the combined results in the main text.

## Appendix I Rubric Statistics

Figure 7 shows the distribution of rubric types in RubricEval according to our 13-category taxonomy across four high-level dimensions.

| Type | Benchmark | Description | Used Subset | Total | Used |  |  |
|---|---|---|---|---|---|---|---|
|  | Inst. | Rub. | Inst. | Rub. |  |  |  |
| Constrained | InfoBench Qin et al. ( 2024b ) | Breaks instructions into decomposed questions; evaluates instruction-following with DRFR metrics. | Hard | 500 | 2,250 | 228 | 1,453 |
| ComplexBench Wen et al. ( 2024 ) | Tests multi-constraint, complex instruction following using hierarchical constraint types and combinations. | Multi-Constraint | 1,150 | 5,297 | 238 | 1,027 |  |
| CFBench Zhang et al. ( 2025a ) | Large-scale Chinese constraint-following benchmark spanning 200+ real scenarios and 50+ NLP tasks. | Filtered | 1,000 | 4,273 | 243 | 1,035 |  |
| AdvancedIF He et al. ( 2025 ) | Expert-rubric benchmark for advanced instruction following (complex, multi-turn, system-level); supports rubric-based RL. | Single-turn | 1,645 | 12,442 | 243 | 1,816 |  |
| Compositional | ComplexBench Wen et al. ( 2024 ) | Tests multi-constraint, complex instruction following using hierarchical constraint types and combinations. | Compositonal | 1,150 | 5,297 | 435 | 1,651 |
| Multi-Turn | StructFlowBench Li et al. ( 2025a ) | Multi-turn benchmark measuring dialogue “structure-flow” understanding across turn-to-turn relation types. | Full | 643 | 1,775 | 643 | 1,775 |
| AdvancedIF He et al. ( 2025 ) | Expert-rubric benchmark for advanced instruction following (complex, multi-turn, system-level); supports rubric-based RL. | Multi-turn | 1,645 | 12,442 | 736 | 4,478 |  |
| System | SysBench Qin et al. ( 2024a ) | Evaluates system-message adherence via violations, misclassification, and multi-turn consistency. | Random | 2,500 | 5,962 | 1,000 | 2,478 |
| AdvancedIF He et al. ( 2025 ) | Expert-rubric benchmark for advanced instruction following (complex, multi-turn, system-level); supports rubric-based RL. | System | 1,645 | 12,442 | 507 | 4,972 |  |
| Total |  |  | 4,273 | 20,685 |  |  |  |

## Appendix J Benchmark Sources and Statistics

Table 10 lists the source benchmarks for each instruction category along with detailed statistics. All rubrics are human-crafted or human-verified.

## Appendix K Judge Model Performance and Selection

Figure 8 . reports the accuracy of different judge models on our human-annotated reference set. We observe non-trivial performance gaps across models, indicating that judge model choice can substantially affect labeling quality. Considering the accuracy and practical trade-offs on the reference set, we select the following four models as base judges: GPT-4.1, Claude-Sonnet-4.5, Gemini-2.5-Flash, and Deepseek-v3.2-exp.

| Dimension | Rubric type | Definition | Example |
|---|---|---|---|
| Content | Content Inclusion | The response must include specific content elements (keywords, entities, components). | For each destination in the itinerary, does the generated text include the recommended duration of stay? |
|  | Content Exclusion | The response must NOT include specific content elements. | Does the generated text free of using the letter ’e’? |
|  | Topic Scope | The response must stay within a specified topic, domain, or area. | Were four questions related to Greek mythology? |
| Form | Quantity Limit | The response or its elements must meet explicit numeric limits (counts, lengths, frequencies). | Did the model cite at least 3 of the clues in each explanation? |
|  | Format Structure | The output must follow a required format, structure, template, or match an exact output. | Is the generated text formatted as a travelogue video script? |
|  | Ordering Sequence | Elements in the response must follow a specified order or arrangement. | Was the list appropriately organized by publishing date, from oldest to newest? |
| Quality | Quality Requirements | Requirements about response quality rather than explicit content/form. | Does each sentence convey a clear, understandable meaning? |
|  | Conditional Logic | The response must make correct judgments or branch based on conditions or context. | Did the response include Ërror: Cannot Complete Requestïf it cannot answer the query about R v Bertrand Marchand? |
|  | Task Completion | The response must complete a specified task or produce a required artifact. | Did the model change each instance of ’God only knows’ to ’Nobody knows?’ |
| Style | Style Tone | The response must follow a specified writing style, tone, or emotional stance. | Does the generated travelogue video script maintain a friendly and engaging tone throughout? |
|  | Language Linguistics | Constraints on language choice, grammar, or linguistic properties. | Does every sentence in the generated text exclusively use the future tense? |
|  | Multi-turn Coherence | The response must correctly handle dependencies on previous conversation turns. | Does the model combine the two messages into a single one? |
|  | Role Persona | The response must be produced from a specified identity, role, or viewpoint. | Did the model respond in a manner consistent with the persona of a painfully shy 11 year old girl? |

## Appendix L Rubric Taxonomy

To categorize each rubric, we write prompt and use GPT-5.1 for rubric categorization. When the source benchmark provides category for the rubric, we use them as guidance in the prompt rather than directly adopting them. This leads to more accurate categorization. If no predefined categories are provided, we perform the categorization directly.

## Appendix M Case Study

Figure 9 illustrates a case study of our automated labeling framework, demonstrating strong labeling quality and scalability.

## Appendix N Evaluation Prompt
