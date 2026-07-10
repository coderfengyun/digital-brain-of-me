Why Supervised Fine-Tuning Fails to Learn: A Systematic Study of Incomplete Learning in Large Language Models Report GitHub Issue × Title: 
Content selection saved. Describe the issue below: 
Description: Submit without GitHub Submit in GitHub arXiv is now an independent nonprofit! Learn more × Back to arXiv Why HTML? Report Issue Back to Abstract Download PDF 
Abstract 

1 Introduction 

2 Related Works 
Supervised Fine-Tuning of Large Language Models 

Data Quality and Multi-Stage Fine-Tuning 

Scaling Laws in Large Language Models 


3 Methods 
3.1 Unlearned Sample Detection 
3.1.1 Sample-Level Evaluation 

3.1.2 Post-SFT Consistency Evaluation 

3.1.3 Robust Detection 

3.1.4 Empirical Prevalence of Unlearned Samples 

3.1.5 Knowledge-State Probing for Diagnostic Preparation 


3.2 Unlearned Sample Processing 
3.2.1 Base Model Knowledge Limitations 

3.2.2 Conflicts Between SFT and Base Model 

3.2.3 Knowledge Conflicts Within SFT Data 

3.2.4 Left-side Forgetting 

3.2.5 Insufficient Training 



4 Results Analysis 
4.1 Base Model Knowledge Enhancement 

4.2 Knowledge Conflict Calibration 

4.3 SFT Knowledge Conflict Resolution 

4.4 Alleviating Left-Side Forgetting 

4.5 Alleviating Insufficient Learning 


5 Conclusion 

6 Limitations 

References 

A Base Model Knowledge Limitations Supplement 
A.1 Experimental Datasets 

A.2 Experimental Baselines 

A.3 Algorithm of Knowledge-Enhanced Continue Pre-training 

A.4 Verification of the Unlearnability of Knowledge Blind Spots by Increasing SFT Epochs 
A.4.1 Experimental Design 



B Conflicts Between SFT and Base Model Supplement 
B.1 Experimental Datasets 

B.2 Algorithm for Resolving Calibration Conflicts Between SFT and Base Model 


C Knowledge Conflicts Between SFT Data Supplement 
C.1 Experimental Datasets 

C.2 Algorithm of Knowledge Conflicts Between SFT Data 

C.3 Deleting and Grouping Conflicting Data 


D Left-side Forgetting Supplement 
D.1 Experimental Datasets 
Parameter Settings for Dynamic Resampling. 


D.2 Algorithm of Left-side Forgetting 

D.3 Analysis of Alleviating Left-sided Forgetting 


E Insufficient Training Supplement 
E.1 Experimental Datasets 

E.2 Algorithm of Insufficient Training 


F Experiment and Analysis with Olmo2-7B 
F.1 Experimental Setup 
Expanded Evaluation Framework. 


F.2 Analysis of SFT Data in Relation to OLMo2 Pre-training Corpus 
Methodology for Knowledge Relationship Assessment. 

Statistical Results. 

Discussion of Findings. 


F.3 CPT Performance and Knowledge Relationship Analysis on OLMo2-7B 
Quantitative Results. 

Discussion of CPT Impact on OLMo2-7B Generalization. 


F.4 Case Studies of Knowledge Conflict Resolution in OLMo2-7B 
Timeliness Conflicts. 

Disciplinary Controversies or Evolving Terminology. 

Multilingual Ambiguities and Geo-Specificity. 

Cross-Cultural Differences and Regional Legal Nuances. 

Summary of Case Study Observations. 


F.5 Summary and Implications of OLMo2 Experiments 

License: arXiv.org perpetual non-exclusive license arXiv:2604.10079v4 [cs.CL] 24 Apr 2026 
Why Supervised Fine-Tuning Fails to Learn: A Systematic Study of Incomplete Learning in Large Language Models 
Chao Xue 1, ⋆ \star , Yao Wang 1, ⋆ \star , Mengqiao Liu 2 , Di Liang 2,3, † \dagger , Xingsheng Han 2 , Peiyang Liu 5 , Xianjie Wu 2 , Chenyao Lu 2 , Lei Jiang 2 , Yu Lu 2 , Haibo Shi 2,3 , Shuang Liang 4 , Minlong Peng 2 , Flora D. Salim 1, † \dagger 1 University of New South Wales, Australia, 2 Tencent Hunyuan, China, 3 Tencent Yuanbao, China, 4 UESTC, China , 5 Peking University, China xuechao8071@gmail.com; flora.salim@unsw.edu.au Abstract 
Supervised Fine-Tuning (SFT) is the standard approach for adapting large language models (LLMs) to downstream tasks. However, we observe a persistent failure mode: even after convergence, models often fail to correctly reproduce a subset of their own supervised training data. We refer to this behavior as the Incomplete Learning Phenomenon (ILP) . This paper presents the first systematic study of ILP in LLM fine-tuning. We formalize ILP as post-training failure to internalize supervised instances and demonstrate its prevalence across multiple model families, domains, and datasets. Through controlled analyses, we identify five recurrent sources of incomplete learning: (1) missing prerequisite knowledge in the pre-trained model, (2) conflicts between SFT supervision and pre-training knowledge, (3) internal inconsistencies within SFT data, (4) left-side forgetting during sequential fine-tuning, and (5) insufficient optimization for rare or complex patterns. We introduce a diagnostic-first framework that maps unlearned samples to these causes using observable training and inference signals, and study several targeted mitigation strategies as causal interventions. Experiments on Qwen, LLaMA, and OLMo2 show that incomplete learning is widespread and heterogeneous, and that improvements in aggregate metrics can mask persistent unlearned subsets. The findings highlight the need for fine-grained diagnosis of what supervised fine-tuning fails to learn, and why. 

Why Supervised Fine-Tuning Fails to Learn: A Systematic Study of Incomplete Learning in Large Language Models 

Chao Xue 1, ⋆ \star , Yao Wang 1, ⋆ \star , Mengqiao Liu 2 , Di Liang 2,3, † \dagger , Xingsheng Han 2 , Peiyang Liu 5 , Xianjie Wu 2 , Chenyao Lu 2 , Lei Jiang 2 , Yu Lu 2 , Haibo Shi 2,3 , Shuang Liang 4 , Minlong Peng 2 , Flora D. Salim 1, † \dagger 1 University of New South Wales, Australia, 2 Tencent Hunyuan, China, 3 Tencent Yuanbao, China, 4 UESTC, China , 5 Peking University, China xuechao8071@gmail.com; flora.salim@unsw.edu.au 
1 1 footnotetext: ⋆ \star Equal Contribution. † \dagger Corresponding Author. 2 2 footnotetext: This work was completed by Xue Chao and Yao Wang under Di Liang’s supervision. 
1 Introduction 

Supervised Fine-Tuning has become the dominant paradigm for adapting large language models (LLMs) to downstream applications such as question answering, dialogue generation, and domain-specific reasoning Hou et al. ( 2024a ); Zhao et al. ( 2024 ) . By leveraging relatively small but carefully curated labeled datasets, SFT enables pre-trained models to align their behavior with task-specific objectives while retaining general linguistic competence. As a result, SFT is widely regarded as a reliable and efficient mechanism for specialization. 

Despite its widespread adoption, SFT exhibits a subtle but consequential failure mode that is insufficiently understood. In practice, we observe that even after training loss convergence and extensive hyperparameter tuning, LLMs frequently fail to correctly answer a subset of their supervised training examples. These failures occur on the SFT dataset itself, rather than on held-out or out-of-distribution data, and persist across random seeds and evaluation settings. We refer to this behavior as the Incomplete Learning Phenomenon (ILP). Figure 1 illustrates ILP: after fine-tuning, re-evaluating the model on its supervised training set reveals that certain instances or patterns remain consistently mispredicted. Importantly, ILP is distinct from catastrophic forgetting McCloskey and Cohen ( 1989 ) , which concerns the loss of previously acquired capabilities, and from machine unlearning Cao and Yang ( 2015 ) , which is intentional. Instead, ILP reflects a failure to acquire or internalize parts of the supervision signal during SFT. 

Understanding ILP is practically important for several reasons. First, SFT datasets, especially in expert domains such as law and medicine, are costly to construct, and incomplete learning directly reduces their utility. Second, unlearned samples are often not random; they tend to correspond to rare cases, compositional patterns, or knowledge-intensive instances, which disproportionately affect robustness and reliability. Third, aggregate evaluation metrics can obscure ILP: improvements on standard benchmarks may coexist with persistent failures on specific supervised instances. Prior work has investigated challenges related to fine-tuning stability, data quality, and optimization dynamics Gururangan et al. ( 2020 ); Zhang and Wu ( 2024 ); Bengio et al. ( 2009 ); Wang et al. ( 2026a ) . However, these studies typically focus on improving overall task performance rather than explaining which supervised knowledge fails to be learned a- nd why . As a result, existing approaches provide limited tools for diagnosing fine-tuning failures at the level of individual samples or patterns. 

In this paper, we take a phenomenon-driven perspective. Our goal is not to propose a new fine-tuning algorithm, but to systematically characterize, diagnose, and validate the sources of incomplete learning in SFT. Through extensive empirical analysis, we identify five recurring contributors to ILP: (i) Pre-training Knowledge Limitations, where the base model lacks prerequisite concepts needed to absorb the supervised signal; (ii) Knowledge Conflicts, where SFT supervision contradicts entrenched pre-training knowledge; (iii) Internal SFT Data Conflicts, arising from noisy or inconsistent annotations; (iv) Left-Side Forgetting, where earlier supervised instances are overwritten during sequential fine-tuning; (v) Insufficient Optimization for Complex Patterns, where rare or compositional structures receive inadequate training signal. 

To operationalize this analysis, we introduce a diagnostic framework that associates unlearned samples with these causes using observable training and inference indicators, such as prediction consistency, entropy dynamics, and replay sensitivity. We further examine several targeted mitigation strategies, including continued pre-training, conflict-aware scheduling, and replay-based resampling, not as universally optimal solutions, but as controlled interventions to test the plausibility of each hypothesized cause. We evaluate our framework on multiple LLMs (Qwen, LLaMA, and OLMo2) across diverse domains and tasks. The results demonstrate that incomplete learning is both prevalent and heterogeneous: no single intervention resolves all failures, and improvements in aggregate metrics can mask persistent unlearned subsets. 

Overall, this work makes three contributions. First, it identifies and formalizes the Incomplete Learning Phenomenon as a measurable and reproducible failure mode in supervised fine-tuning. Second, it provides a systematic taxonomy and diagnostic framework that links unlearned supervised instances to distinct underlying causes. Third, it empirically shows that different sources of incomplete learning require different remedies, highlighting the limitations of one-size-fits-all fine-tuning strategies. Together, these findings argue for a shift from performance-centric evaluation of SFT toward fine-grained, learning-centric diagnosis, offering a foundation for more reliable and interpretable adaptation of large language models. 

Figure 1: Schematic illustration of the incomplete learning phenomenon, where testing the model on the initial training set after fine-tuning reveals that certain samples or patterns were not effectively learned during SFT. 

Figure 2: The Incomplete Learning framework consists of three stages: (1) fine-tune on SFT data; (2) detect unlearned samples via re-evaluation; (3) calibrate model and data to fix them. 

2 Related Works 

Recent research on large language models spans multiple directions: stepwise distillation Chen et al. ( 2025 ); Jiang et al. ( 2025 ); Zhang et al. ( 2025 ) , multi-hop temporal knowledge reasoning Wen et al. ( 2026 ); Xue et al. ( 2024 ) , and security and robustness through jailbreak detection Hua et al. ( 2025 ) and backdoor analysis in reward learning Guo et al. ( 2026b ) ; structured representation learning for contextual semantic matching Xue and Gao ( 2025 ) and empathetic dialogue modeling Ji et al. ( 2026 ) ; multimodal referential understanding Wang et al. ( 2026b ) ; memorization-constrained story reasoning Jiang and Ferraro ( 2026 ) ; and broader applications in AI governance Chen ( 2026b , a ) and predictive analytics Hu and Shen ( 2026 ) . A common thread across many of these approaches is the reliance on high-quality, human- or model-generated reasoning demonstrations—typically injected into the model via supervised fine-tuning (SFT)—to align behavior with desired reasoning patterns. 
Supervised Fine-Tuning of Large Language Models 
LLMs show remarkable zero-shot capabilities Brown et al. ( 2020 ); Wu et al. ( 2021 ); Hou et al. ( 2024b ); Song et al. ( 2023 ) , leading to extensive efforts in enhancing their applicability via Supervised Fine-Tuning. To unlock their full potential, LLMs are often subjected to the SFT phase, which refines their ability to perform specific tasks and better align with human instructions Ponti et al. ( 2023 ); Li et al. ( 2026 ); Gao et al. ( 2026 ); Huang et al. ( 2026 ) . This study broadens the traditional scope of SFT to incorporate diverse forms of sequence-to-sequence fine-tuning, including fine-tuning for human alignment, instruction adherence, and domain-specific task optimization (Zhou et al. , 2023b ; Yuan et al. , 2023b ; Cheng et al. , 2023a ; Zhang et al. , 2024 ; Liu et al. , 2026 ) . Recent research has explored multi-task instruction fine-tuning for pre-trained LLMs, aimed at enhancing their zero-shot performance across a broad range of downstream NLP tasks (Sanh et al. , 2022 ; Khashabi et al. , 2020 ) . Prominent efforts such as FLAN, which curated large-scale instruction datasets, have shown that models fine-tuned with such data Chung et al. ( 2022 ); Singhal et al. ( 2022 ) achieve improved zero-shot generalization. Although the generalization capabilities of LLMs in out-of-distribution domains have been extensively studied Liu et al. ( 2024a ); Yuan et al. ( 2024 ); Wang et al. ( 2024 ) , the effect of multi-task fine-tuning on in-domain performance, and potential SFT-induced degradation of foundational abilities Mukhoti et al. ( 2023 ); Liu et al. ( 2025b ) or catastrophic forgetting Kotha et al. ( 2023 ) , remain critical areas of investigation. These challenges highlight the complexities our work on ILP addresses by focusing on why SFT data itself is not fully learned. With the rise of proprietary models like ChatGPT, the focus on SFT for better aligning LLMs with human intent has grown (Ouyang et al. , 2022 ) . Beyond crowd-sourcing, user logs (Chiang et al. , 2023 ; Wang et al. , 2023a ) and LLM-assisted self-generated data (Wang et al. , 2023c ; Taori et al. , 2023 ; Cheng et al. , 2023b ; Lei et al. , 2023 ; Xu et al. , 2023 ; Xue et al. , 2023b ; Wu et al. , 2025a ; Mukherjee et al. , 2023 ; Wang et al. , 2025 ; Wu et al. , 2025c ) are increasingly used for SFT. Moreover, methods to improve the quality of SFT datasets have been proposed to enhance alignment with human preferences (Zhou et al. , 2023a ; Wang et al. , 2023b ; Lu et al. , 2023 ; Wu et al. , 2025d ; Liu et al. , 2024b ; Cui et al. , 2023 ) . SFT has also proven valuable for domain-specific applications, excelling in areas such as mathematical reasoning (Cobbe et al. , 2021 ; Yuan et al. , 2023a ; Yue et al. , 2023 ; Gou et al. , 2024 ; Yue et al. , 2024 ; Dai et al. , 2025 ) and code generation tasks (Chaudhary, 2023 ; Luo et al. , 2023 ; Wei et al. , 2023 ; Wu et al. , 2025b ) . Additionally, supervised fine-tuned LLMs have been leveraged to enhance interactivity by composing external commands, enabling the execution of a variety of highly complex downstream applications, such as tool integration Yao et al. ( 2023b , a ); Song et al. ( 2024 ); Fu et al. ( 2024 ); Liu et al. ( 2025a ); Guo et al. ( 2026a ) . 
Data Quality and Multi-Stage Fine-Tuning 
Improving data quality is a recurring focal point in the SFT pipeline Mazumder et al. ( 2023 ); Li et al. ( 2024a ); Liu et al. ( 2024c ); Li et al. ( 2024c ) . Techniques such as data augmentation Shorten and Khoshgoftaar ( 2019 ); Li et al. ( 2024b ); Fu et al. ( 2021 ) and active learning Settles ( 2009 ) aim to enhance the diversity or informativeness of training examples. Prompt engineering Lester et al. ( 2021 ); Liu et al. ( 2023b , a ) has been introduced to reshape the input space, thereby encouraging more consistent model outputs. Additionally, knowledge distillation Hinton ( 2015 ) is employed to transfer knowledge from larger teacher models to smaller or specialized student models, ensuring knowledge preservation while reducing model size or computational overhead Sanh et al. ( 2019 ); Liang et al. ( 2019b ); Wang et al. ( 2022 ); Song et al. ( 2022 ); Xue et al. ( 2023a ); Chen et al. ( 2026 ); Gui et al. ( 2018 ); Zheng et al. ( 2022 ); Liang et al. ( 2019a ); Hu et al. ( 2025 ); Xue et al. ( 2026 ) . Curriculum learning Bengio et al. ( 2009 ); Qian et al. arranges training samples in an order of increasing complexity, enabling models to develop foundational competencies before tackling more difficult examples. Such methods have demonstrated improved convergence rates and robustness Platanios et al. ( 2019 ) . Multi-Task and multi-pass fine-tuning extend ideas by exposing the model to multiple related tasks or multi-step schedules, where earlier tasks are revisited Dong et al. ( 2023 ); Ruder ( 2017 ); Ma et al. ( 2022 ); Fei et al. ( 2022 ) . These strategies highlight how training order, data scheduling, and repeated re-exposure to previously learned samples can reduce overfitting, mitigate forgetting, and improve generalization Parisi et al. ( 2019 ) . 
Scaling Laws in Large Language Models 
The remarkable performance of LLMs is driven by scaling model sizes, dataset volumes, and computational resources to unprecedented levels Kaplan et al. ( 2020 ) . Analyzing how performance across an exponential range of scales has become crucial. Research has explored scaling laws in pre-training (Anil et al. , 2023 ; Hoffmann et al. , 2022 ) , transfer learning (Chronopoulou et al. , 2019 ) , preference modeling (Gao et al. , 2022 ) , and mathematical reasoning (Yuan et al. , 2023a ) , underscoring the pivotal role of scaling in enhancing LLMs’ capability. 

3 Methods 

Our method is designed to systematically diagnose and mitigate incomplete learning phenomena in supervised fine-tuning of large language models. As illustrated in Figure 2 , the framework consists of two tightly coupled components: Unlearned Sample Detection and Unlearned Sample Processing . The Unlearned Sample Detection module aims to identify training instances that are not effectively internalized by the model during SFT. Unlike conventional data filtering approaches that rely on static heuristics or annotation quality, we focus on samples that remain persistently mispredicted or unstable across training, indicating a failure of learning rather than noise. These unlearned samples form hidden bottlenecks that limit performance gains from additional data or training iterations. Building on the detected unlearned samples, the Unlearned Sample Processing module analyzes their underlying characteristics and failure modes. Through empirical analysis, we categorize typical unlearned samples into five representative error types, each associated with distinct learning deficiencies. For each type, we design targeted processing strategies that directly address its root cause, rather than uniformly reweighting or discarding data. 

3.1 Unlearned Sample Detection 

A prerequisite for studying incomplete learning is a reliable mechanism to identify which supervised instances are not effectively learned after fine-tuning. In this work, we treat unlearned sample detection as a post-training measurement problem rather than an optimization objective. Specifically, we ask whether a model, after supervised fine-tuning (SFT) convergence, can consistently reproduce the supervision signal it has already seen. 

3.1.1 Sample-Level Evaluation 

SFT datasets typically consist of free-form text responses, which makes instance-level correctness difficult to assess in a standardized manner. To enable consistent measurement across heterogeneous datasets and tasks, we operationalize supervised responses into a multiple-choice (MC) format. This conversion is not intended to change the supervision content, but to provide a discrete and comparable evaluation interface. Concretely, for each SFT instance, the original response is preserved as the correct option, while several semantically plausible but incorrect alternatives are constructed as distractors. The model is then required to select the correct option among a fixed set of candidates. Figure 2 illustrates the overall framework, and an example of this conversion is shown below. 

The index of the correct option is recorded and used for subsequent evaluation. Importantly, this conversion is applied only for detection and analysis and does not alter the original SFT training objective. 

3.1.2 Post-SFT Consistency Evaluation 

As shown in Figure 2 , unlearned sample detection is performed after the SFT process has converged. During fine-tuning, we monitor the training loss to ensure stable optimization and exclude under-training artifacts. After convergence, the entire SFT dataset is re-evaluated by the fine-tuned model using the MC-based interface. For a dataset of N N supervised instances, we define sample-level correctness by whether the model selects the ground-truth option. The training-set accuracy is: 

Acc = 1 N ​ ∑ i = 1 N 𝕀 ​ ( arg ⁡ max k ⁡ y ^ i , k = y i ) , \mathrm{Acc}=\frac{1}{N}\sum_{i=1}^{N}\mathbb{I}\left(\arg\max_{k}\hat{y}_{i,k}=y_{i}\right), (1) 


where y ^ i , k \hat{y}_{i,k} is predicted probability for option k k of instance i i , and y i y_{i} is the correct index. Accuracy is coarse and misses partial or unstable learning; thus, we use repeated sampling to reduce stochasticity. 

3.1.3 Robust Detection 

For each instance, we perform N N independent inference runs and compute its pass@N rate, defined as the fraction of runs in which the model predicts the correct option. This metric reflects the consistency with which the supervision signal is recovered. In addition, we adopt a Best-of- N N (BoN) criterion, which selects the prediction with the highest confidence score among N N samples, providing a complementary upper-bound estimate of model capability. An instance is considered unlearned if its pass@N rate falls below a predefined threshold T T . In our experiments, we set T = 0.2 T=0.2 under BoN-5 sampling unless otherwise stated. We empirically verify that the identified unlearned instances are stable across random seeds and sampling runs, indicating that they are not artifacts of stochastic decoding. 

3.1.4 Empirical Prevalence of Unlearned Samples 

Applying this detection protocol across ten benchmark SFT datasets, we find that incomplete learning is widespread. On average, 15.3 % ± 2.1 % 15.3\%\pm 2.1\% of supervised instances remain unlearned after SFT convergence. This observation holds across model families and domains, suggesting that ILP is not an isolated or dataset-specific phenomenon. For subsequent analysis, we construct a candidate set by selecting instances with pass@5 rates below the threshold under repeated BoN-5 sampling. From this set, we select the top- K K most severe cases based on error consistency, with K = 1000 K=1000 in our main experiments. These instances form the basis for fine-grained diagnosis in the following section. 

3.1.5 Knowledge-State Probing for Diagnostic Preparation 

To enable attribution of unlearned samples to potential causes, we probe the knowledge state of the base model prior to fine-tuning. For each candidate instance x x , we first test whether the base model can correctly answer it in a zero-shot setting. We define a binary indicator of knowledge existence as 

𝒫 exist ​ ( x ) = 𝕀 ​ ( Acc ​ ( ℳ base ​ ( x ) ) > 0.8 ) . \mathcal{P}_{\mathrm{exist}}(x)=\mathbb{I}\left(\mathrm{Acc}(\mathcal{M}_{\mathrm{base}}(x))>0.8\right). (2) 


In addition, we measure how the model’s predictive distribution changes after SFT by computing the Jensen–Shannon divergence between the base and fine-tuned models,as: 

D JS ​ ( P base ∥ P SFT ) = 1 2 ​ D KL ​ ( P base ∥ M ) \displaystyle D_{\text{JS}}(P_{\text{base}}\|P_{\text{SFT}})=\frac{1}{2}D_{\text{KL}}\left(P_{\text{base}}\|M\right) (3) 

+ 1 2 ​ D KL ​ ( P SFT ∥ M ) \displaystyle+\frac{1}{2}D_{\text{KL}}\left(P_{\text{SFT}}\|M\right) 


where M = ( P base + P SFT ) / 2 M=(P_{\mathrm{base}}+P_{\mathrm{SFT}})/2 . Together, these signals characterize whether the base model lacks relevant knowledge, holds conflicting priors, or undergoes insufficient or unstable updates during fine-tuning. In the next subsection, we use these diagnostics to analyze unlearned samples and map them to distinct sources of incomplete learning. 

3.2 Unlearned Sample Processing 

To systematically analyze the Incomplete Learning Phenomenon (ILP), we introduce a unified pipeline that operates at the level of individual supervised instances. The core objective is not merely to improve aggregate performance, but to determine why specific SFT samples remain unlearned after convergence. Figure 3 illustrates the overall attribution process. The pipeline begins by identifying unlearned samples via post-SFT evaluation. Each such sample is then sequentially examined under a set of diagnostic tests, each corresponding to a hypothesized source of incomplete learning. Importantly, the mitigation strategies described below are not positioned as general-purpose solutions; instead, they serve as controlled interventions to validate the causal relevance of each attributed factor. 

3.2.1 Base Model Knowledge Limitations 

The first step of our framework focuses on identifying knowledge blind spots in the base model. We begin by detecting unlearned samples from the SFT dataset and extracting their underlying factual content using OpenIE tools. 1 1 1 https://nlp.stanford.edu/software/openie.html Each sample is converted into a set of subject–predicate–object triplets, forming a candidate knowledge set 𝒦 cand = { ( h , r , t ) } \mathcal{K}_{\text{cand}}=\{(h,r,t)\} . 

To quantify whether a knowledge triplet is sufficiently covered by the base model, we adopt BoN sampling and the pass@N metric as probing mechanisms. Intuitively, if the model repeatedly fails to produce correct answers even under multiple sampling attempts, the corresponding knowledge is likely missing rather than poorly optimized. Formally, we define the set of blind knowledge as: 

𝒦 blind = { k ∣ pass@10 ( k ) < 0.2 \displaystyle\mathcal{K}_{\text{blind}}=\{k\mid\text{pass@10}(k)<2 (4) 

∧ BoN-5 Acc ( k ) < 0.1 } . \displaystyle\land\text{BoN-5 Acc}(k)<1\}. 


This criterion filters out cases where errors are attributable to stochasticity or reasoning noise, retaining only those samples that reflect systematic knowledge gaps. Once blind knowledge is identified, we expand the corresponding background information by querying multiple external sources, including WikiData APIs, Google Search, and the OpenAI-o1 API. For each unknown entity, we retrieve an average of 20 ± 1.1 20\pm 1.1 related documents, covering definitions, relations, and contextual usage. This multi-source aggregation mitigates bias from any single knowledge provider and improves factual completeness. The resulting knowledge-augmented corpus 𝒞 aug \mathcal{C}_{\text{aug}} is then mixed with a general-domain corpus to perform continued pre-training. The mixed corpus as: 

𝒞 mix = 0.8 ​ 𝒞 general + 0.2 ​ 𝒞 aug , \mathcal{C}_{\text{mix}}=0.8\mathcal{C}_{\text{general}}+0.2\mathcal{C}_{\text{aug}}, (5) 


where 𝒞 general \mathcal{C}_{\text{general}} consists of standard pre-training data such as OpenWebText and BookCorpus. This design explicitly balances knowledge injection and distributional stability, enabling the model to acquire missing facts without degrading its general language understanding capabilities. After CPT, we reapply SFT using the original SFT dataset and evaluate the updated model. Improvements are measured using accuracy and pass@N metrics, allowing us to isolate gains attributable to knowledge completion rather than optimization artifacts. As shown in Figure 4 , this procedure consistently improves downstream performance across medical, legal, and financial benchmarks, validating that incomplete learning in SFT can often be traced back to knowledge deficiencies in the base model. 

3.2.2 Conflicts Between SFT and Base Model 

Beyond missing knowledge, we observe another failure mode in which the base model exhibits strong but incorrect beliefs that conflict with SFT supervision. Such conflicts are particularly problematic because high-confidence errors tend to resist correction during fine-tuning, leading to unstable or slow convergence. To systematically identify these cases, we prompt the base model to answer multiple-choice questions from the SFT dataset and extract the probability of the predicted answer token. Let P model ​ ( y ∣ x ) P_{\text{model}}(y\mid x) denote the model’s confidence for input x x and predicted answer y y . A sample is flagged as a high-confidence error if the model strongly prefers an incorrect answer: 

Error ​ ( x , y ) = ​ { 1 , P ​ ( y | x ) > T ​ and ​ y ≠ y SFT , 0 , otherwise . \begin{aligned} \text{Error}(x,y)=\end{aligned}\begin{cases}\begin{aligned} 1,&P(y|x)>T\text{ and }y\neq y_{\text{SFT}},\\ 0,&\text{otherwise}.\end{aligned}\end{cases} (6) 


Here, T T denotes a predefined confidence threshold, and y SFT y_{\text{SFT}} is the ground-truth label provided by the SFT data. Samples satisfying this condition form a high-confidence error set ℰ \mathcal{E} , representing explicit knowledge conflicts between the base model and supervision. To resolve these conflicts, we follow the same knowledge augmentation and CPT procedure described above. Specifically, authoritative external sources such as Wikipedia and domain-specific corpora are used to retrieve verified information corresponding to conflicting samples. Continued pre-training on this curated corpus realigns the model’s internal knowledge representations, reducing resistance to subsequent SFT updates. 

Figure 3: Unlearned sample attribution framework. 

3.2.3 Knowledge Conflicts Within SFT Data 

Incomplete learning may also originate from inconsistencies internal to the SFT dataset itself. When semantically similar inputs are associated with contradictory labels, the model receives an incoherent learning signal, limiting convergence on affected samples. We detect such conflicts by computing semantic similarity between sample pairs. If Sim ​ ( s i , s j ) > X \text{Sim}(s_{i},s_{j})>X , the pair is treated as potentially conflicting. To determine correctness, we employ GPT OpenAI et al. ( 2024 ) ,deepseek DeepSeek-AI et al. ( 2025 ) as an external evaluator. If one sample is judged incorrect, it is removed; if both are judged correct, the pair is retained but treated as incompatible during training. Rather than discarding valid supervision, we assign conflicting samples to separate training buckets, ensuring they do not co-occur within the same mini-batch. This bucket assignment is periodically re-evaluated every K K training steps to reflect the model’s evolving competence. Observed reductions in error rates on these samples after bucketing indicate that internal data conflict, rather than representational insufficiency, was the primary cause of incomplete learning. 

Figure 4: Performance improvements achieved by introducing Continued Pre-Training (CPT). Results demonstrate consistent accuracy gains across the medical (MedQA), legal (LegalBench), and financial (FinanceBench) domains. 

3.2.4 Left-side Forgetting 

Another manifestation of incomplete learning appears as left-side forgetting. When SFT datasets are concatenated or processed sequentially, we observe a systematic bias toward recently seen data. By reversing dataset order and tracking per-dataset accuracy, we find that earlier samples are progressively overshadowed, consistent with left-side forgetting Li and Lee ( 2024 ) . To mitigate this effect, we apply random shuffling across the entire SFT dataset and introduce a dynamic re-sampling mechanism. At regular intervals of K K steps, validation accuracy is monitored for each data subset. If a significant drop is detected, samples from the affected subset are temporarily upweighted. This strategy, detailed in Algorithm 4 , serves to test whether incomplete learning arises from training order effects rather than intrinsic difficulty. 

3.2.5 Insufficient Training 

Finally, incomplete learning can arise from insufficient optimization, where a fixed number of training epochs fails to accommodate datasets of varying complexity. To address this, we adopt a progressive epoch increment strategy inspired by early stopping Prechelt ( 2002 ) . Training begins with a minimal epoch count E min E_{\min} and incrementally increases until validation performance ceases to improve. The stopping condition is defined as 

𝒞 ​ stop = 𝕀 ​ ( ℒ ​ val ( e ) > ℒ val ( e − 1 ) + δ ) , \mathcal{C}\text{stop}=\mathbb{I}\left(\mathcal{L}\text{val}^{(e)}>\mathcal{L}_{\text{val}}^{(e-1)}+\delta\right), (7) 


where δ = 0.01 \delta=0.01 prevents premature termination due to noise. This adaptive strategy ensures sufficient learning while avoiding overfitting, and its implementation is detailed in Algorithm 5 . 

Model ARC CommonQA SocialIQA MedMCQA 

Qwen 7B 68.1 → \rightarrow 70.9 (+2.8) 74.5 → \rightarrow 76.9 (+2.4) 70.3 → \rightarrow 72.2 (+1.9) 61.2 → \rightarrow 63.7 (+2.5) 

Qwen 14B 71.2 → \rightarrow 73.7 (+2.5) 76.8 → \rightarrow 79.1 (+2.3) 72.1 → \rightarrow 74.0 (+1.9) 63.1 → \rightarrow 65.3 (+2.2) 

LLaMA2 7B 66.3 → \rightarrow 68.8 (+2.5) 72.8 → \rightarrow 75.3 (+2.5) 68.9 → \rightarrow 71.1 (+2.2) 58.9 → \rightarrow 61.4 (+2.5) 

LLaMA2 13B 69.1 → \rightarrow 71.3 (+2.2) 75.2 → \rightarrow 77.3 (+2.1) 70.5 → \rightarrow 72.1 (+1.6) 61.1 → \rightarrow 63.0 (+1.9) 


Table 1: Accuracy (%) before and after Continued Pre-Training (CPT) on four knowledge-intensive benchmarks. Improvements brought by CPT are highlighted in color and remain consistent across model sizes and domains. 

Experiment Qwen-7B Qwen-14B LLaMA-7B LLaMA-13B 

Knowledge conflict 82.3 → \rightarrow 85.1 (+2.8) 84.5 → \rightarrow 87.2 (+2.7) 81.8 → \rightarrow 84.3 (+2.5) 83.6 → \rightarrow 86.5 (+2.9) 

Left-side forgetting 78.5 → \rightarrow 79.8 (+1.3) 79.3 → \rightarrow 80.5 (+1.2) 77.9 → \rightarrow 79.1 (+1.2) 78.7 → \rightarrow 80.2 (+1.5) 

Insufficient learning 88.2 → \rightarrow 90.1 (+1.9) 89.5 → \rightarrow 91.3 (+1.8) 87.8 → \rightarrow 89.7 (+1.9) 88.9 → \rightarrow 90.8 (+1.9) 


Table 2: Performance improvements across baseline models after applying optimization strategies for resolving knowledge conflicts, mitigating left-side forgetting, and addressing insufficient learning. 

4 Results Analysis 

4.1 Base Model Knowledge Enhancement 

To address pre-training knowledge gaps, we employ Continued Pre-Training (CPT), described in Appendix A . As illustrated in Figure 4 , CPT consistently improves accuracy on domain-specific benchmarks, including MedQA Jin et al. ( 2020 ) , LegalBench Guha et al. ( 2023 ); Koreeda and Manning ( 2021 ) , and FinanceBench Islam et al. ( 2023 ) for models such as Qwen Bai et al. ( 2023 ) and LLaMA2 Touvron et al. ( 2023 ) . Accuracy gains range from 9.4% to 14.1% (e.g., +12.5% on MedQA), demonstrating CPT’s effectiveness in filling critical knowledge gaps that standard SFT fails to capture. Notably, simply extending SFT epochs leads to only marginal improvements, underscoring that missing foundational knowledge cannot be addressed through prolonged fine-tuning alone. Further validation with OLMo2-7B OLMo et al. ( 2025 ) (Appendix F ) shows similar trends: CPT significantly enhances performance in domains where the base model initially exhibited high ’Knowledge Non-Existence Rates’. While targeted knowledge injection sometimes interacts with generalization, careful corpus balancing mitigates negative effects, indicating that CPT can selectively improve domain-specific knowledge without undermining overall language understanding. Collectively, these results highlight CPT as a necessary step for bridging knowledge deficits in LLMs prior to SFT. 

4.2 Knowledge Conflict Calibration 

High-confidence conflicts between pre-trained knowledge and SFT supervision pose another obstacle to complete learning. To resolve this, we apply a CPT-based calibration strategy (Appendix B ). Table 1 demonstrates consistent accuracy improvements across models(Qwen-7B/14B, LLaMA2-7B, and LLaMA2-13B) on diverse benchmarks. Gains range from +1.6% (LLaMA2-13B on SocialIQA) to +2.8% (Qwen-7B on ARC), with additional improvements for other datasets (e.g., +2.5% for Qwen-14B on ARC, +2.1% for LLaMA2-13B on CommonQA). These improvements correspond to a marked reduction in high-confidence SFT conflicts, confirming that targeted CPT effectively aligns the model’s predictions with supervised knowledge. Case studies on OLMo2-7B reveal that CPT recalibrates conflict points where pre-trained knowledge previously overrode SFT supervision. This demonstrates CPT’s dual role: both filling missing knowledge and mitigating entrenched misbeliefs. Overall, CPT provides a systematic mechanism to harmonize pre-training and supervised signals, which is essential for reducing incomplete learning arising from knowledge conflicts. 

4.3 SFT Knowledge Conflict Resolution 

Internal conflicts within the SFT dataset can also induce incomplete learning, particularly when semantically similar or nearly identical inputs are paired with contradictory labels—introducing noise that confuses the optimization process. To mitigate this, we propose a two-stage approach based on conflict detection followed by dynamic bucketing, which groups potentially conflicting examples into separate training batches while preserving all valid supervision signals (see Appendix C for implementation details). As demonstrated in Table 2 , this strategy yields consistent and substantial performance gains on mixed-domain SFT datasets: for instance, Qwen-7B improves from 82.3% to 85.1% (+2.8%) and Qwen-14B from 84.5% to 87.2% (+2.7%). Comparable improvements are observed across LLaMA model variants, confirming the generality of the method. By isolating conflicting samples into distinct batches rather than discarding them, the model retains access to valuable supervisory information and learns more robust representations from complex, real-world SFT data. Ablation studies reported in Table 8 further validate that dynamic bucketing significantly outperforms naive conflict resolution strategies—such as removing all samples flagged as conflicting—which often eliminate informative examples and inadvertently reduce the overall learning capacity of the model. 

4.4 Alleviating Left-Side Forgetting 

Left-side forgetting, where early-learned SFT knowledge is progressively overshadowed or even overwritten during sequential training on multi-task or mixed-domain data, represents another critical source of incomplete learning. To counteract this temporal bias, we employ a joint strategy of global shuffling—randomizing the entire training sequence across epochs—together with dynamic resampling that adaptively upweights earlier examples throughout training (Appendix D ). This dual approach ensures that initial knowledge remains actively reinforced rather than diluted by later batches. As shown in Table 2 , this leads to consistent accuracy improvements on mixed datasets: Qwen-7B rises from 78.5% → \rightarrow 79.8%, and Qwen-14B from 79.3% → \rightarrow 80.5%. More importantly, ROUGE-L scores on the first 10% of summarization data—the segment most vulnerable to left-side forgetting—increased significantly by +29% (from 0.41 → \rightarrow 0.53, Table 11 ), demonstrating robust preservation of early-acquired capabilities. These results confirm that the combination of dynamic resampling and global shuffling effectively mitigates progressive knowledge decay while minimally interfering with the acquisition of later-stage tasks. 

4.5 Alleviating Insufficient Learning 

Insufficient optimization, particularly for rare, long-tail, or structurally complex patterns in SFT datasets, is a key contributor to incomplete learning. Standard fixed-epoch training often terminates before such difficult examples receive adequate signal, leaving residual errors that degrade model reliability. To address this limitation, we employ a Progressive Epoch Increment strategy combined with validation-driven early stopping (Appendix E ), which dynamically adapts training duration per dataset based on real-time validation performance. This adaptive schedule allocates additional epochs only when marginal gains are observed, ensuring that underrepresented or challenging examples receive sufficient gradient updates while simultaneously preventing overfitting through timely termination. As shown in Table 2 , Qwen-7B accuracy on underlearned tasks increases from 88.2% to 90.1% (+1.9%), with comparable gains observed across Qwen-14B, LLaMA-7B, and LLaMA-13B, whose improvements range from +1.0% to +1.9%. These results demonstrate that adaptive training duration effectively closes persistent learning gaps for difficult data patterns, thereby enhancing both model completeness and robustness—without compromising generalization on broader benchmarks or incurring unnecessary computational cost. 

5 Conclusion 

In this paper, we systematically investigate the “Incomplete Learning Phenomenon” (ILP) in supervised fine-tuning (SFT) of large language models (LLMs) and identify five major contributing factors: (1) limitations in pre-training knowledge that hinder downstream adaptation, (2) conflicts between SFT data and the base model’s priors, (3) internal inconsistencies within the SFT dataset itself, (4) left-side forgetting during sequential training, and (5) insufficient optimization due to inadequate training duration or data exposure. To address these interrelated challenges, we introduce a unified mitigation framework integrating pre-training enhancement, conflict-aware data processing, dynamic bucketing, data resampling, and adaptive epoch augmentation. Extensive experiments with multiple LLMs across diverse datasets demonstrate that these strategies collectively and effectively mitigate ILP, resulting in significant improvements not only in the model’s mastery of SFT-specific knowledge but also in generalization performance on standard evaluation benchmarks. 

6 Limitations 

Despite the effectiveness and breadth of our proposed framework for addressing the Incomplete Learning Phenomenon in Supervised Fine-Tuning (SFT), several limitations warrant further investigation: 

Complexity of Conflict Detection: While we have proposed strategies for detecting and resolving knowledge conflicts (both between pre-training and SFT data, and within the SFT data itself), the current approach depends on high-quality annotations and reliable external tools (e.g., for domain verification). Inconsistent or noisy data sources may reduce conflict detection accuracy, leading to potentially suboptimal or partial conflict resolution. 

Dependency on Quality Pre-training Data: Our method presupposes that injecting additional knowledge or updates into the pre-training phase will robustly bridge knowledge gaps. However, if the supplementary corpus is itself noisy or a biased representative, those newly introduced biases or errors could propagate through subsequent fine-tuning stages, diminishing overall performance gains. 

Computational Overheads: The inclusion of pre-training enhancement and knowledge resampling increases training time and resource consumption. Particularly at the multi-billion parameter level LLMs, amplify computational demands, raising concerns about feasibility for organizations with limited hardware or training budgets. 

Overall, while our proposed framework alleviates many inherent challenges of SFT in large language models, the actual fine-grained calibration remains underexplored. 

References 

R. Anil, A. M. Dai, O. Firat, M. Johnson, D. Lepikhin, A. Passos, S. Shakeri, E. Taropa, P. Bailey, Z. Chen, et al. (2023) Palm 2 technical report . arXiv preprint arXiv:2305.10403 . Cited by: §2 . 

J. Bai, S. Bai, Y. Chu, Z. Cui, K. Dang, X. Deng, Y. Fan, W. Ge, Y. Han, F. Huang, et al. (2023) Qwen technical report . arXiv preprint arXiv:2309.16609 . Cited by: §4.1 . 

Y. Bengio, J. Louradour, R. Collobert, and J. Weston (2009) Curriculum learning . In Proceedings of the 26th annual international conference on machine learning , pp. 41–48 . Cited by: §1 , §2 . 

T. Brown, B. Mann, N. Ryder, M. Subbiah, J. D. Kaplan, P. Dhariwal, A. Neelakantan, P. Shyam, G. Sastry, A. Askell, et al. (2020) Language models are few-shot learners . Advances in neural information processing systems 33 , pp. 1877–1901 . Cited by: §2 . 

Y. Cao and J. Yang (2015) Towards making systems forget with machine unlearning . In 2015 IEEE symposium on security and privacy , pp. 463–480 . Cited by: §1 . 

S. Chaudhary (2023) Code alpaca: an instruction-following llama model for code generation . GitHub . Note: https://github.com/sahil280114/codealpaca Cited by: §2 . 

L. Chen (2026a) Beyond external constraints: the missing dimension of ai governance . Available at SSRN 6449738 . Cited by: §2 . 

L. Chen (2026b) Testing moral development in ai: an experimental architecture for internal value development in ai governance . Available at SSRN 6472178 . Cited by: §2 . 

Y. Chen, Y. Chen, Y. Yang, J. Shang, Z. Zhang, Z. Zhang, S. Nie, S. Wang, Y. Sun, H. Wu, et al. (2026) Sparse growing transformer: training-time sparse depth allocation via progressive attention looping . arXiv preprint arXiv:2603.23998 . Cited by: §2 . 

Y. Chen, J. Sheng, W. Zhang, and T. Liu (2025) Improving reasoning capabilities in small models through mixture-of-layers distillation with stepwise attention on key information . In Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing , pp. 4952–4971 . Cited by: §2 . 

X. Cheng, Q. Dong, F. Yue, T. Ko, M. Wang, and Y. Zou (2023a) M 3 st: mix at three levels for speech translation . In ICASSP 2023-2023 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP) , pp. 1–5 . Cited by: §2 . 

X. Cheng, Z. Zhu, W. Xu, Y. Li, H. Li, and Y. Zou (2023b) Accelerating multiple intent detection and slot filling via targeted knowledge distillation . In The 2023 Conference on Empirical Methods in Natural Language Processing , Cited by: §2 . 

W. Chiang, Z. Li, Z. Lin, Y. Sheng, Z. Wu, H. Zhang, L. Zheng, S. Zhuang, Y. Zhuang, J. E. Gonzalez, I. Stoica, and E. P. Xing (2023) Vicuna: an open-source chatbot impressing gpt-4 with 90%* chatgpt quality . External Links: Link Cited by: §2 . 

A. Chronopoulou, C. Baziotis, and A. Potamianos (2019) An embarrassingly simple approach for transfer learning from pretrained language models . arXiv preprint arXiv:1902.10547 . Cited by: §2 . 

H. W. Chung, L. Hou, S. Longpre, B. Zoph, Y. Tay, W. Fedus, Y. Li, X. Wang, M. Dehghani, S. Brahma, A. Webson, S. S. Gu, Z. Dai, M. Suzgun, X. Chen, A. Chowdhery, A. Castro-Ros, M. Pellat, K. Robinson, D. Valter, S. Narang, G. Mishra, A. Yu, V. Zhao, Y. Huang, A. Dai, H. Yu, S. Petrov, E. H. Chi, J. Dean, J. Devlin, A. Roberts, D. Zhou, Q. V. Le, and J. Wei (2022) Scaling instruction-finetuned language models . External Links: 2210.11416 Cited by: §2 . 

P. Clark, I. Cowhey, O. Etzioni, T. Khot, A. Sabharwal, C. Schoenick, and O. Tafjord (2018) Think you have solved question answering? try arc, the ai2 reasoning challenge . arXiv:1803.05457v1 . Cited by: §B.1 . 

K. Cobbe, V. Kosaraju, M. Bavarian, M. Chen, H. Jun, L. Kaiser, M. Plappert, J. Tworek, J. Hilton, R. Nakano, et al. (2021) Training verifiers to solve math word problems . arXiv preprint arXiv:2110.14168 . Cited by: §2 . 

G. Cui, L. Lee, Z. Liu, C. Yuan, S. Li, Y. Sun, C. Zhang, Y. Tian, Z. Zhang, L. Li, et al. (2023) UltraFeedback: boosting language models with high-quality feedback . arXiv preprint arXiv:2310.01377 . Cited by: §2 . 

C. Dai, H. Shan, M. Song, and D. Liang (2025) HoPE: hyperbolic rotary positional encoding for stable long-range dependency modeling in large language models . arXiv preprint arXiv:2509.05218 . Cited by: §2 . 

DeepSeek-AI, A. Liu, B. Feng, B. Xue, B. Wang, B. Wu, C. Lu, C. Zhao, C. Deng, C. Zhang, C. Ruan, D. Dai, D. Guo, D. Yang, D. Chen, D. Ji, E. Li, F. Lin, F. Dai, F. Luo, G. Hao, G. Chen, G. Li, H. Zhang, H. Bao, H. Xu, H. Wang, H. Zhang, H. Ding, H. Xin, H. Gao, H. Li, H. Qu, J. L. Cai, J. Liang, J. Guo, J. Ni, J. Li, J. Wang, J. Chen, J. Chen, J. Yuan, J. Qiu, J. Li, J. Song, K. Dong, K. Hu, K. Gao, K. Guan, K. Huang, K. Yu, L. Wang, L. Zhang, L. Xu, L. Xia, L. Zhao, L. Wang, L. Zhang, M. Li, M. Wang, M. Zhang, M. Zhang, M. Tang, M. Li, N. Tian, P. Huang, P. Wang, P. Zhang, Q. Wang, Q. Zhu, Q. Chen, Q. Du, R. J. Chen, R. L. Jin, R. Ge, R. Zhang, R. Pan, R. Wang, R. Xu, R. Zhang, R. Chen, S. S. Li, S. Lu, S. Zhou, S. Chen, S. Wu, S. Ye, S. Ye, S. Ma, S. Wang, S. Zhou, S. Yu, S. Zhou, S. Pan, T. Wang, T. Yun, T. Pei, T. Sun, W. L. Xiao, W. Zeng, W. Zhao, W. An, W. Liu, W. Liang, W. Gao, W. Yu, W. Zhang, X. Q. Li, X. Jin, X. Wang, X. Bi, X. Liu, X. Wang, X. Shen, X. Chen, X. Zhang, X. Chen, X. Nie, X. Sun, X. Wang, X. Cheng, X. Liu, X. Xie, X. Liu, X. Yu, X. Song, X. Shan, X. Zhou, X. Yang, X. Li, X. Su, X. Lin, Y. K. Li, Y. Q. Wang, Y. X. Wei, Y. X. Zhu, Y. Zhang, Y. Xu, Y. Xu, Y. Huang, Y. Li, Y. Zhao, Y. Sun, Y. Li, Y. Wang, Y. Yu, Y. Zheng, Y. Zhang, Y. Shi, Y. Xiong, Y. He, Y. Tang, Y. Piao, Y. Wang, Y. Tan, Y. Ma, Y. Liu, Y. Guo, Y. Wu, Y. Ou, Y. Zhu, Y. Wang, Y. Gong, Y. Zou, Y. He, Y. Zha, Y. Xiong, Y. Ma, Y. Yan, Y. Luo, Y. You, Y. Liu, Y. Zhou, Z. F. Wu, Z. Z. Ren, Z. Ren, Z. Sha, Z. Fu, Z. Xu, Z. Huang, Z. Zhang, Z. Xie, Z. Zhang, Z. Hao, Z. Gou, Z. Ma, Z. Yan, Z. Shao, Z. Xu, Z. Wu, Z. Zhang, Z. Li, Z. Gu, Z. Zhu, Z. Liu, Z. Li, Z. Xie, Z. Song, Z. Gao, and Z. Pan (2025) DeepSeek-v3 technical report . External Links: 2412.19437 , Link Cited by: §3.2.3 . 

G. Dong, H. Yuan, K. Lu, C. Li, M. Xue, D. Liu, W. Wang, Z. Yuan, C. Zhou, and J. Zhou (2023) How abilities in large language models are affected by supervised fine-tuning data composition . arXiv preprint arXiv:2310.05492 . Cited by: §2 . 

Edoardo Federici (2022) Sentence-bert-base, sentence-transformer for italian . Hugging Face . External Links: Link , Document Cited by: §C.2 , item 2 . 

Z. Fei, Q. Zhang, T. Gui, D. Liang, S. Wang, W. Wu, and X. Huang (2022) CQG: a simple and effective controlled generation framework for multi-hop question generation . In Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers) , pp. 6896–6906 . Cited by: §2 . 

D. Fu, J. Huang, S. Lu, G. Dong, Y. Wang, K. He, and W. Xu (2024) PreAct: predicting future in react enhances agent’s planning ability . External Links: 2402.11534 Cited by: §2 . 

X. Fu, Z. Shao, Y. Qu, Y. Guan, Y. Zou, Z. Shi, and J. Tan (2021) Fast and unsupervised non-local feature learning for direct volume rendering of 3d medical images . In 2021 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS) , pp. 5886–5891 . Cited by: §2 . 

L. Gao, J. Schulman, and J. Hilton (2022) Scaling laws for reward model overoptimization . External Links: 2210.10760 Cited by: §2 . 

Z. Gao, D. Liang, X. Wu, P. Morel, and M. Peng (2026) Decorl: decoupling reasoning chains via parallel sub-step generation and cascaded reinforcement for interpretable and scalable rlhf . In Proceedings of the AAAI Conference on Artificial Intelligence , Vol. 40 , pp. 30789–30797 . Cited by: §2 . 

A. Gokaslan, V. Cohen, E. Pavlick, and S. Tellex (2019) OpenWebText corpus . Note: http://Skylion007.github.io/OpenWebTextCorpus Cited by: §D.1 . 

Z. Gou, Z. Shao, Y. Gong, Y. Shen, Y. Yang, M. Huang, N. Duan, and W. Chen (2024) ToRA: a tool-integrated reasoning agent for mathematical problem solving . External Links: 2309.17452 Cited by: §2 . 

N. Guha, J. Nyarko, D. E. Ho, C. Ré, A. Chilton, A. Narayana, A. Chohlas-Wood, A. Peters, B. Waldon, D. N. Rockmore, D. Zambrano, D. Talisman, E. Hoque, F. Surani, F. Fagan, G. Sarfaty, G. M. Dickinson, H. Porat, J. Hegland, J. Wu, J. Nudell, J. Niklaus, J. Nay, J. H. Choi, K. Tobia, M. Hagan, M. Ma, M. Livermore, N. Rasumov-Rahe, N. Holzenberger, N. Kolt, P. Henderson, S. Rehaag, S. Goel, S. Gao, S. Williams, S. Gandhi, T. Zur, V. Iyer, and Z. Li (2023) LegalBench: a collaboratively built benchmark for measuring legal reasoning in large language models . External Links: 2308.11462 Cited by: §A.1 , §4.1 . 

T. Gui, Q. Zhang, J. Gong, M. Peng, D. Liang, K. Ding, and X. Huang (2018) Transferring from formal newswire domain with hypernet for twitter pos tagging . In Proceedings of the 2018 conference on empirical methods in natural language processing , pp. 2540–2549 . Cited by: §2 . 

W. Guo, Z. Shi, L. Zhao, J. Ma, Z. Zhu, J. He, M. Zhang, and J. Li (2026a) E3-tir: enhanced experience exploitation for tool-integrated reasoning . External Links: 2604.09455 , Link Cited by: §2 . 

W. Guo, Z. Shi, Z. Zhu, Y. Zhou, M. Zhang, and J. Li (2026b) Backdoors in rlvr: jailbreak backdoors in llms from verifiable reward . External Links: 2604.09748 , Link Cited by: §2 . 

S. Gururangan, A. Marasović, S. Swayamdipta, K. Lo, I. Beltagy, D. Downey, and N. A. Smith (2020) Don’t stop pretraining: adapt language models to domains and tasks . External Links: 2004.10964 , Link Cited by: §1 . 

D. Hendrycks, C. Burns, S. Basart, A. Critch, J. Li, D. Song, and J. Steinhardt (2021a) Aligning ai with shared human values . Proceedings of the International Conference on Learning Representations (ICLR) . Cited by: 1st item . 

D. Hendrycks, C. Burns, S. Basart, A. Zou, M. Mazeika, D. Song, and J. Steinhardt (2021b) Measuring massive multitask language understanding . Proceedings of the International Conference on Learning Representations (ICLR) . Cited by: 1st item . 

G. Hinton (2015) Distilling the knowledge in a neural network . arXiv preprint arXiv:1503.02531 . Cited by: §2 . 

J. Hoffmann, S. Borgeaud, A. Mensch, E. Buchatskaya, T. Cai, and L. Sifre (2022) Training compute-optimal large language models . External Links: 2203.15556 Cited by: §2 . 

X. Hou, Q. Li, J. Yang, T. Li, L. Chai, X. Wu, H. Ji, Z. Li, J. Nie, J. Dun, et al. (2024a) Raw text is all you need: knowledge-intensive multi-turn instruction tuning for large language model . arXiv preprint arXiv:2407.03040 . Cited by: §1 . 

Y. Hou, J. Zhang, Z. Lin, H. Lu, R. Xie, J. McAuley, and W. X. Zhao (2024b) Large language models are zero-shot rankers for recommender systems . In European Conference on Information Retrieval , pp. 364–381 . Cited by: §2 . 

J. Hu, C. Xue, C. Yu, J. Xu, and C. Tan (2025) Joint learning event-specific probe and argument library with differential optimization for document-level multi-event extraction . In Findings of the Association for Computational Linguistics: NAACL 2025 , pp. 714–726 . Cited by: §2 . 

L. Hu and Y. Shen (2026) A predictive analytics approach for forecasting global stock index returns using deep learning techniques . Decision Analytics Journal , pp. 100685 . Cited by: §2 . 

P. Hua, H. Li, S. Shi, Z. Yu, and N. Zhang (2025) Rethinking jailbreak detection of large vision language models with representational contrastive scoring . External Links: 2512.12069 , Link Cited by: §2 . 

F. Huang, G. Huang, X. Fan, Y. He, X. Liang, X. Chen, Q. Jiang, F. N. Khan, J. Jiang, and Z. Wang (2026) Semantic-space exploration and exploitation in rlvr for llm reasoning . External Links: 2509.23808 , Link Cited by: §2 . 

P. Islam, A. Kannappan, D. Kiela, R. Qian, N. Scherrer, and B. Vidgen (2023) FinanceBench: a new benchmark for financial question answering . External Links: 2311.11944 Cited by: §A.1 , §4.1 . 

H. Ji, Y. Fan, M. Zhao, X. Li, L. Wu, and C. Gao (2026) STRIDE-ed: a strategy-grounded stepwise reasoning framework for empathetic dialogue systems . External Links: 2604.07100 , Link Cited by: §2 . 

Y. Jiang and F. Ferraro (2026) Beyond math: stories as a testbed for memorization-constrained reasoning in llms . In Proceedings of the 19th Conference of the European Chapter of the Association for Computational Linguistics (Volume 1: Long Papers) , pp. 5590–5607 . Cited by: §2 . 

Y. Jiang, D. Li, and F. Ferraro (2025) DRP: distilled reasoning pruning with skill-aware step decomposition for efficient large reasoning models . arXiv preprint arXiv:2505.13975 . Cited by: §2 . 

D. Jin, E. Pan, N. Oufattole, W. Weng, H. Fang, and P. Szolovits (2020) What disease does this patient have? a large-scale open domain question answering dataset from medical exams . arXiv preprint arXiv:2009.13081 . Cited by: §A.1 , §4.1 . 

M. Joshi, E. Choi, D. Weld, and L. Zettlemoyer (2017) triviaqa: A Large Scale Distantly Supervised Challenge Dataset for Reading Comprehension . arXiv e-prints , pp. arXiv:1705.03551 . External Links: 1705.03551 Cited by: §C.1 . 

J. Kaplan, S. McCandlish, T. Henighan, T. B. Brown, B. Chess, R. Child, S. Gray, A. Radford, J. Wu, and D. Amodei (2020) Scaling laws for neural language models . arXiv preprint arXiv:2001.08361 . Cited by: §2 . 

D. Khashabi, S. Min, A. Saparov, H. Hajishirzi, W. Yih, and P. Clark (2020) UnifiedQA: crossing format boundaries with a single qa system . In Findings of the Association for Computational Linguistics: EMNLP 2020 , pp. 1896–1907 . Cited by: §2 . 

Y. Koreeda and C. D. Manning (2021) ContractNLI: a dataset for document-level natural language inference for contracts . arXiv preprint arXiv:2110.01799 . Cited by: §4.1 . 

S. Kotha, J. M. Springer, and A. Raghunathan (2023) Understanding catastrophic forgetting in language models via implicit inference . arXiv preprint arXiv:2309.10105 . Cited by: §2 . 

T. Kwiatkowski, J. Palomaki, O. Redfield, M. Collins, A. Parikh, C. Alberti, D. Epstein, I. Polosukhin, J. Devlin, K. Lee, K. Toutanova, L. Jones, M. Kelcey, M. Chang, A. M. Dai, J. Uszkoreit, Q. Le, and S. Petrov (2019a) Natural questions: a benchmark for question answering research . Transactions of the Association for Computational Linguistics 7 , pp. 452–466 . External Links: Link , Document Cited by: 3rd item . 

T. Kwiatkowski, J. Palomaki, O. Redfield, M. Collins, A. Parikh, C. Alberti, D. Epstein, I. Polosukhin, M. Kelcey, J. Devlin, K. Lee, K. N. Toutanova, L. Jones, M. Chang, A. Dai, J. Uszkoreit, Q. Le, and S. Petrov (2019b) Natural questions: a benchmark for question answering research . Transactions of the Association of Computational Linguistics . Cited by: §C.1 . 

S. Lei, G. Dong, X. Wang, K. Wang, and S. Wang (2023) InstructERC: reforming emotion recognition in conversation with a retrieval multi-task llms framework . External Links: 2309.11911 Cited by: §2 . 

B. Lester, R. Al-Rfou, and N. Constant (2021) The power of scale for parameter-efficient prompt tuning . arXiv preprint arXiv:2104.08691 . Cited by: §2 . 

B. Li, D. Liang, and Z. Zhang (2024a) Comateformer: combined attention transformer for semantic sentence matching . arXiv preprint arXiv:2412.07220 . Cited by: §2 . 

C. Li and H. Lee (2024) Examining forgetting in continual pre-training of aligned large language models . arXiv preprint arXiv:2401.03129 . Cited by: §3.2.4 . 

J. Li, C. Qi, R. Wang, Q. Chen, L. Xu, D. Liang, B. Simons, and S. Liang (2026) When safety becomes a vulnerability: exploiting llm alignment homogeneity for transferable blocking in rag . arXiv preprint arXiv:2603.03919 . Cited by: §2 . 

L. Li, Q. Liao, M. Lai, D. Liang, and S. Liang (2024b) Local and global: text matching via syntax graph calibration . In ICASSP 2024-2024 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP) , pp. 11571–11575 . Cited by: §2 . 

M. Li, Y. Zhang, S. He, Z. Li, H. Zhao, J. Wang, N. Cheng, and T. Zhou (2024c) Superfiltering: weak-to-strong data filtering for fast instruction-tuning . In Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers) , pp. 14255–14273 . Cited by: §2 . 

D. Liang, F. Zhang, Q. Zhang, and X. Huang (2019a) Asynchronous deep interaction network for natural language inference . In Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP) , pp. 2692–2700 . Cited by: §2 . 

D. Liang, F. Zhang, W. Zhang, Q. Zhang, J. Fu, M. Peng, T. Gui, and X. Huang (2019b) Adaptive multi-attention network incorporating answer information for duplicate question detection . In Proceedings of the 42nd international ACM SIGIR conference on research and development in information retrieval , pp. 95–104 . Cited by: §2 . 

X. Liang, L. Wu, J. Li, Y. Wang, Q. Meng, T. Qin, W. Chen, M. Zhang, and T. Liu (2021) R-drop: regularized dropout for neural networks . External Links: 2106.14448 Cited by: §A.1 . 

B. Liu, L. Zhan, Z. Lu, Y. Feng, L. Xue, and X. Wu (2024a) How good are llms at out-of-distribution detection? . External Links: 2308.10261 Cited by: §2 . 

P. Liu, Z. Cui, D. Liang, and W. Ye (2025a) Who stole your data? a method for detecting unauthorized rag theft . arXiv preprint arXiv:2510.07728 . Cited by: §2 . 

W. Liu, W. Zeng, K. He, Y. Jiang, and J. He (2024b) What makes good data for alignment? a comprehensive study of automatic data selection in instruction tuning . External Links: 2312.15685 Cited by: §2 . 

X. Liu, X. Guan, D. Liang, and X. Wu (2026) DPI: exploiting parameter heterogeneity for interference-free fine-tuning . arXiv preprint arXiv:2601.17777 . Cited by: §2 . 

X. Liu, D. Liang, H. Shan, P. Liu, Y. Liu, M. Wu, Y. Li, X. Wu, L. Miao, J. Shen, et al. (2025b) Structural reward model: enhancing interpretability, efficiency, and scalability in reward modeling . In Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing: Industry Track , pp. 672–685 . Cited by: §2 . 

Y. Liu, M. Li, D. Liang, X. Li, F. Giunchiglia, L. Huang, X. Feng, and R. Guan (2024c) Resolving word vagueness with scenario-guided adapter for natural language inference . arXiv preprint arXiv:2405.12434 . Cited by: §2 . 

Y. Liu, D. Liang, F. Fang, S. Wang, W. Wu, and R. Jiang (2023a) Time-aware multiway adaptive fusion network for temporal knowledge graph question answering . In ICASSP 2023-2023 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP) , pp. 1–5 . Cited by: §2 . 

Y. Liu, D. Liang, M. Li, F. Giunchiglia, X. Li, S. Wang, W. Wu, L. Huang, X. Feng, and R. Guan (2023b) Local and global: temporal question answering via information fusion. . In IJCAI , pp. 5141–5149 . Cited by: §2 . 

K. Lu, H. Yuan, Z. Yuan, R. Lin, J. Lin, C. Tan, and C. Zhou (2023) # instag: instruction tagging for diversity and complexity analysis . arXiv preprint arXiv:2308.07074 . Cited by: §2 . 

Z. Luo, C. Xu, P. Zhao, Q. Sun, X. Geng, W. Hu, C. Tao, J. Ma, Q. Lin, and D. Jiang (2023) WizardCoder: empowering code large language models with evol-instruct . arXiv preprint arXiv:2306.08568 . Cited by: §2 . 

R. Ma, Y. Tan, X. Zhou, X. Chen, D. Liang, S. Wang, W. Wu, T. Gui, and Q. Zhang (2022) Searching for optimal subword tokenization in cross-domain ner . arXiv preprint arXiv:2206.03352 . Cited by: §2 . 

A. L. Maas, R. E. Daly, P. T. Pham, D. Huang, A. Y. Ng, and C. Potts (2011) Learning word vectors for sentiment analysis . In Proceedings of the 49th Annual Meeting of the Association for Computational Linguistics: Human Language Technologies , Portland, Oregon, USA , pp. 142–150 . External Links: Link Cited by: §E.1 . 

M. Mazumder, C. Banbury, X. Yao, B. Karlaš, W. Gaviria Rojas, S. Diamos, G. Diamos, L. He, A. Parrish, H. R. Kirk, et al. (2023) Dataperf: benchmarks for data-centric ai development . Advances in Neural Information Processing Systems 36 , pp. 5320–5347 . Cited by: §2 . 

M. McCloskey and N. J. Cohen (1989) Catastrophic interference in connectionist networks: the sequential learning problem . In Psychology of learning and motivation , Vol. 24 , pp. 109–165 . Cited by: §1 . 

S. Mukherjee, A. Mitra, G. Jawahar, S. Agarwal, H. Palangi, and A. Awadallah (2023) Orca: progressive learning from complex explanation traces of gpt-4 . External Links: 2306.02707 Cited by: §2 . 

J. Mukhoti, S. Rajeswar, H. Singh, K. Rajan, S. Ruder, P. Kumar, A. Raghunathan, A. Kunchukuttan, D. Kumar, and S. Sarawagi (2023) Fine-tuning can cripple your foundation model; preserving features may be the solution . arXiv preprint arXiv:2308.13320 . Cited by: §2 . 

S. Narayan, S. B. Cohen, and M. Lapata (2018) Don’t give me the details, just the summary! topic-aware convolutional neural networks for extreme summarization . ArXiv abs/1808.08745 . Cited by: §D.1 . 

T. OLMo, P. Walsh, L. Soldaini, D. Groeneveld, K. Lo, S. Arora, A. Bhagia, Y. Gu, S. Huang, M. Jordan, N. Lambert, D. Schwenk, O. Tafjord, T. Anderson, D. Atkinson, F. Brahman, C. Clark, P. Dasigi, N. Dziri, A. Ettinger, M. Guerquin, D. Heineman, H. Ivison, P. W. Koh, J. Liu, S. Malik, W. Merrill, L. J. V. Miranda, J. Morrison, T. Murray, C. Nam, J. Poznanski, V. Pyatkin, A. Rangapur, M. Schmitz, S. Skjonsberg, D. Wadden, C. Wilhelm, M. Wilson, L. Zettlemoyer, A. Farhadi, N. A. Smith, and H. Hajishirzi (2025) 2 olmo 2 furious . External Links: 2501.00656 , Link Cited by: Appendix F , §4.1 . 

OpenAI, J. Achiam, S. Adler, S. Agarwal, L. Ahmad, I. Akkaya, F. L. Aleman, D. Almeida, J. Altenschmidt, S. Altman, S. Anadkat, R. Avila, I. Babuschkin, S. Balaji, V. Balcom, P. Baltescu, H. Bao, M. Bavarian, J. Belgum, I. Bello, J. Berdine, G. Bernadett-Shapiro, C. Berner, L. Bogdonoff, O. Boiko, M. Boyd, A. Brakman, G. Brockman, T. Brooks, M. Brundage, K. Button, T. Cai, R. Campbell, A. Cann, B. Carey, C. Carlson, R. Carmichael, B. Chan, C. Chang, F. Chantzis, D. Chen, S. Chen, R. Chen, J. Chen, M. Chen, B. Chess, C. Cho, C. Chu, H. W. Chung, D. Cummings, J. Currier, Y. Dai, C. Decareaux, T. Degry, N. Deutsch, D. Deville, A. Dhar, D. Dohan, S. Dowling, S. Dunning, A. Ecoffet, A. Eleti, T. Eloundou, D. Farhi, L. Fedus, N. Felix, S. P. Fishman, J. Forte, I. Fulford, L. Gao, E. Georges, C. Gibson, V. Goel, T. Gogineni, G. Goh, R. Gontijo-Lopes, J. Gordon, M. Grafstein, S. Gray, R. Greene, J. Gross, S. S. Gu, Y. Guo, C. Hallacy, J. Han, J. Harris, Y. He, M. Heaton, J. Heidecke, C. Hesse, A. Hickey, W. Hickey, P. Hoeschele, B. Houghton, K. Hsu, S. Hu, X. Hu, J. Huizinga, S. Jain, S. Jain, J. Jang, A. Jiang, R. Jiang, H. Jin, D. Jin, S. Jomoto, B. Jonn, H. Jun, T. Kaftan, Ł. Kaiser, A. Kamali, I. Kanitscheider, N. S. Keskar, T. Khan, L. Kilpatrick, J. W. Kim, C. Kim, Y. Kim, J. H. Kirchner, J. Kiros, M. Knight, D. Kokotajlo, Ł. Kondraciuk, A. Kondrich, A. Konstantinidis, K. Kosic, G. Krueger, V. Kuo, M. Lampe, I. Lan, T. Lee, J. Leike, J. Leung, D. Levy, C. M. Li, R. Lim, M. Lin, S. Lin, M. Litwin, T. Lopez, R. Lowe, P. Lue, A. Makanju, K. Malfacini, S. Manning, T. Markov, Y. Markovski, B. Martin, K. Mayer, A. Mayne, B. McGrew, S. M. McKinney, C. McLeavey, P. McMillan, J. McNeil, D. Medina, A. Mehta, J. Menick, L. Metz, A. Mishchenko, P. Mishkin, V. Monaco, E. Morikawa, D. Mossing, T. Mu, M. Murati, O. Murk, D. Mély, A. Nair, R. Nakano, R. Nayak, A. Neelakantan, R. Ngo, H. Noh, L. Ouyang, C. O’Keefe, J. Pachocki, A. Paino, J. Palermo, A. Pantuliano, G. Parascandolo, J. Parish, E. Parparita, A. Passos, M. Pavlov, A. Peng, A. Perelman, F. de Avila Belbute Peres, M. Petrov, H. P. de Oliveira Pinto, Michael, Pokorny, M. Pokrass, V. H. Pong, T. Powell, A. Power, B. Power, E. Proehl, R. Puri, A. Radford, J. Rae, A. Ramesh, C. Raymond, F. Real, K. Rimbach, C. Ross, B. Rotsted, H. Roussez, N. Ryder, M. Saltarelli, T. Sanders, S. Santurkar, G. Sastry, H. Schmidt, D. Schnurr, J. Schulman, D. Selsam, K. Sheppard, T. Sherbakov, J. Shieh, S. Shoker, P. Shyam, S. Sidor, E. Sigler, M. Simens, J. Sitkin, K. Slama, I. Sohl, B. Sokolowsky, Y. Song, N. Staudacher, F. P. Such, N. Summers, I. Sutskever, J. Tang, N. Tezak, M. B. Thompson, P. Tillet, A. Tootoonchian, E. Tseng, P. Tuggle, N. Turley, J. Tworek, J. F. C. Uribe, A. Vallone, A. Vijayvergiya, C. Voss, C. Wainwright, J. J. Wang, A. Wang, B. Wang, J. Ward, J. Wei, C. Weinmann, A. Welihinda, P. Welinder, J. Weng, L. Weng, M. Wiethoff, D. Willner, C. Winter, S. Wolrich, H. Wong, L. Workman, S. Wu, J. Wu, M. Wu, K. Xiao, T. Xu, S. Yoo, K. Yu, Q. Yuan, W. Zaremba, R. Zellers, C. Zhang, M. Zhang, S. Zhao, T. Zheng, J. Zhuang, W. Zhuk, and B. Zoph (2024) GPT-4 technical report . External Links: 2303.08774 , Link Cited by: §3.2.3 . 

L. Ouyang, J. Wu, X. Jiang, D. Almeida, C. L. Wainwright, P. Mishkin, C. Zhang, S. Agarwal, K. Slama, A. Ray, J. Schulman, J. Hilton, F. Kelton, L. Miller, M. Simens, A. Askell, P. Welinder, P. Christiano, J. Leike, and R. Lowe (2022) Training language models to follow instructions with human feedback . External Links: 2203.02155 Cited by: §2 . 

A. Pal, L. K. Umapathi, and M. Sankarasubbu (2022) MedMCQA: a large-scale multi-subject multi-choice dataset for medical domain question answering . In Proceedings of the Conference on Health, Inference, and Learning , G. Flores, G. H. Chen, T. Pollard, J. C. Ho, and T. Naumann (Eds.) , Proceedings of Machine Learning Research , Vol. 174 , pp. 248–260 . External Links: Link Cited by: §B.1 . 

G. I. Parisi, R. Kemker, J. L. Part, C. Kanan, and S. Wermter (2019) Continual lifelong learning with neural networks: a review . Neural networks 113 , pp. 54–71 . Cited by: §2 . 

E. A. Platanios, O. Stretcu, G. Neubig, B. Poczos, and T. M. Mitchell (2019) Competence-based curriculum learning for neural machine translation . arXiv preprint arXiv:1903.09848 . Cited by: §2 . 

E. M. Ponti, C. Vania, G. Glavaš, O. Majewska, Z. Wu, J. Lin, I. Vulic, and A. Korhonen (2023) Fine-tuning language models for specific tasks can be harmful . arXiv preprint arXiv:2310.09419 . Cited by: §2 . 

L. Prechelt (2002) Early stopping-but when? . In Neural Networks: Tricks of the trade , pp. 55–69 . Cited by: §3.2.5 . 

[92] Q. Qian, M. Wu, Z. Huang, W. Liu, C. Lv, X. Wang, Z. Wang, Z. Guo, Z. Xu, L. Chen, et al. Adaptive curriculum strategies: stabilizing reinforcement learning for large language models . Cited by: §2 . 

P. Rajpurkar, J. Zhang, K. Lopyrev, and P. Liang (2016) SQuAD: 100,000+ questions for machine comprehension of text . In Proceedings of the 2016 Conference on Empirical Methods in Natural Language Processing , J. Su, K. Duh, and X. Carreras (Eds.) , Austin, Texas , pp. 2383–2392 . External Links: Link , Document , 1606.05250 Cited by: §C.1 . 

S. Reddy, D. Chen, and C. D. Manning (2019) CoQA: a conversational question answering challenge . Transactions of the Association for Computational Linguistics 7 , pp. 249–266 . External Links: Link , Document Cited by: §C.1 . 

D. Rein, B. L. Hou, A. C. Stickland, J. Petty, R. Y. Pang, J. Dirani, J. Michael, and S. R. Bowman (2024) GPQA: a graduate-level google-proof q&a benchmark . In First Conference on Language Modeling , External Links: Link Cited by: 3rd item . 

S. Ruder (2017) An overview of multi-task learning in deep neural networks . arXiv preprint arXiv:1706.05098 . Cited by: §2 . 

V. Sanh, L. Debut, J. Chaumond, and T. Wolf (2019) DistilBERT, a distilled version of bert: smaller, faster, cheaper and lighter . arXiv preprint arXiv:1910.01108 . Cited by: §2 . 

V. Sanh, A. Webson, T. Wolf, and A. M. Rush (2022) Multitask prompted training enables zero-shot task generalization . External Links: 2110.08207 Cited by: §2 . 

A. See, P. J. Liu, and C. D. Manning (2017) Get to the point: summarization with pointer-generator networks . In Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers) , Vancouver, Canada , pp. 1073–1083 . External Links: Link , Document Cited by: §D.1 . 

B. Settles (2009) Active learning literature survey . Cited by: §2 . 

C. Shorten and T. M. Khoshgoftaar (2019) A survey on image data augmentation for deep learning . Journal of big data 6 ( 1 ), pp. 1–48 . Cited by: §2 . 

K. Singhal, S. Azizi, T. Tu, S. S. Mahdavi, J. Wei, H. W. Chung, N. Scales, Y. Liu, A. Rajkomar, J. Barral, C. Semturs, A. Karthikesalingam, and V. Natarajan (2022) Large language models encode clinical knowledge . External Links: 2212.13138 Cited by: §2 . 

J. Song, D. Liang, R. Li, Y. Li, S. Wang, M. Peng, W. Wu, and Y. Yu (2022) Improving semantic matching through dependency-enhanced pre-trained model with adaptive fusion . arXiv preprint arXiv:2210.08471 . Cited by: §2 . 

X. Song, K. He, P. Wang, G. Dong, Y. Mou, J. Wang, Y. Xian, X. Cai, and W. Xu (2023) Large language models meet open-world intent discovery and recognition: an evaluation of chatgpt . External Links: 2310.10176 Cited by: §2 . 

X. Song, Z. Wang, K. He, G. Dong, Y. Mou, J. Zhao, and W. Xu (2024) Knowledge editing on black-box large language models . External Links: 2402.08631 Cited by: §2 . 

M. Suzgun, N. Scales, N. Schärli, S. Gehrmann, Y. Tay, H. W. Chung, A. Chowdhery, Q. V. Le, E. H. Chi, D. Zhou, and J. Wei (2022) Challenging big-bench tasks and whether chain-of-thought can solve them . arXiv preprint arXiv:2210.09261 . Cited by: 2nd item . 

A. Talmor, J. Herzig, N. Lourie, and J. Berant (2019) CommonsenseQA: a question answering challenge targeting commonsense knowledge . In Proceedings of the 2019 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long and Short Papers) , Minneapolis, Minnesota , pp. 4149–4158 . External Links: Link , Document , 1811.00937 Cited by: §B.1 . 

R. Taori, I. Gulrajani, T. Zhang, Y. Dubois, X. Li, C. Guestrin, P. Liang, and T. B. Hashimoto (2023) Stanford alpaca: an instruction-following llama model . GitHub . Note: https://github.com/tatsu-lab/stanford_alpaca Cited by: §2 . 

H. Touvron, L. Martin, K. Stone, P. Albert, A. Almahairi, Y. Babaei, N. Bashlykov, S. Batra, P. Bhargava, S. Bhosale, D. Bikel, L. Blecher, C. C. Ferrer, M. Chen, G. Cucurull, D. Esiobu, J. Fernandes, J. Fu, W. Fu, B. Fuller, C. Gao, V. Goswami, N. Goyal, A. Hartshorn, S. Hosseini, R. Hou, H. Inan, M. Kardas, V. Kerkez, M. Khabsa, I. Kloumann, A. Korenev, P. S. Koura, M. Lachaux, T. Lavril, J. Lee, D. Liskovich, Y. Lu, Y. Mao, X. Martinet, T. Mihaylov, P. Mishra, I. Molybog, Y. Nie, A. Poulton, J. Reizenstein, R. Rungta, K. Saladi, A. Schelten, R. Silva, E. M. Smith, R. Subramanian, X. E. Tan, B. Tang, R. Taylor, A. Williams, J. X. Kuan, P. Xu, Z. Yan, I. Zarov, Y. Zhang, A. Fan, M. Kambadur, S. Narang, A. Rodriguez, R. Stojnic, S. Edunov, and T. Scialom (2023) Llama 2: open foundation and fine-tuned chat models . External Links: 2307.09288 Cited by: §4.1 . 

G. Wang, S. Cheng, X. Zhan, X. Li, S. Song, and Y. Liu (2023a) OpenChat: advancing open-source language models with mixed-quality data . External Links: 2309.11235 Cited by: §2 . 

P. Wang, Y. Wang, M. Diao, K. He, G. Dong, and W. Xu (2024) Multi-perspective consistency enhances confidence estimation in large language models . External Links: 2402.11279 Cited by: §2 . 

R. Wang, Y. Huang, M. Li, J. Li, D. Liang, B. Simons, P. Ke, S. Liang, and K. Qin (2026a) Rethinking llm-driven heuristic design: generating efficient and specialized solvers via dynamics-aware optimization . arXiv preprint arXiv:2601.20868 . Cited by: §1 . 

S. Wang, D. Liang, J. Song, Y. Li, and W. Wu (2022) Dabert: dual attention enhanced bert for semantic matching . arXiv preprint arXiv:2210.03454 . Cited by: §2 . 

Y. Wang, D. Liang, and M. Peng (2025) Not all parameters are created equal: smart isolation boosts fine-tuning performance . arXiv preprint arXiv:2508.21741 . Cited by: §2 . 

Y. Wang, H. Ivison, P. Dasigi, J. Hessel, T. Khot, K. R. Chandu, D. Wadden, K. MacMillan, N. A. Smith, I. Beltagy, et al. (2023b) How far can camels go? exploring the state of instruction tuning on open resources . arXiv preprint arXiv:2306.04751 . Cited by: §2 . 

Y. Wang, Y. Kordi, S. Mishra, A. Liu, N. A. Smith, D. Khashabi, and H. Hajishirzi (2023c) Self-instruct: aligning language models with self-generated instructions . External Links: 2212.10560 Cited by: §2 . 

Y. Wang, E. Chersoni, and C. Huang (2026b) This one or that one? a study on accessibility via demonstratives with multimodal large language models . In Language Resources and Evaluation Conference 2026 , Cited by: §2 . 

Y. Wei, Z. Wang, J. Liu, Y. Ding, and L. Zhang (2023) Magicoder: source code is all you need . External Links: 2312.02120 Cited by: §2 . 

W. Wen, C. Xue, S. Pan, Y. Sun, and M. Peng (2026) Reinforcement learning enhanced multi-hop reasoning for temporal knowledge question answering . arXiv preprint arXiv:2601.01195 . Cited by: §2 . 

A. Williams, N. Nangia, and S. Bowman (2018) A broad-coverage challenge corpus for sentence understanding through inference . In Proceedings of the 2018 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long Papers) , pp. 1112–1122 . External Links: Link Cited by: §E.1 . 

M. Wu, Q. Qian, W. Liu, X. Wang, Z. Huang, D. Liang, L. Miao, S. Dou, C. Lv, Z. Wang, et al. (2025a) Progressive mastery: customized curriculum learning with guided prompting for mathematical reasoning . arXiv preprint arXiv:2506.04065 . Cited by: §2 . 

S. Wu, X. Zhao, T. Yu, R. Zhang, C. Shen, H. Liu, F. Li, H. Zhu, J. Luo, L. Xu, et al. (2021) Yuan 1.0: large-scale pre-trained language model in zero-shot and few-shot learning . arXiv preprint arXiv:2110.04725 . Cited by: §2 . 

X. Wu, D. Liang, J. Yang, X. Cheng, L. Chai, T. Li, L. Yang, and Z. Li (2025b) Breaking size barrier: enhancing reasoning for large-size table question answering . In International Conference on Database Systems for Advanced Applications , pp. 241–256 . Cited by: §2 . 

X. Wu, J. Yang, L. Chai, G. Zhang, J. Liu, X. Du, D. Liang, D. Shu, X. Cheng, T. Sun, et al. (2025c) Tablebench: a comprehensive and complex benchmark for table question answering . In Proceedings of the AAAI Conference on Artificial Intelligence , Vol. 39 , pp. 25497–25506 . Cited by: §2 . 

X. Wu, J. Yang, T. Li, S. Zhang, Y. Du, L. Chai, D. Liang, and Z. Li (2025d) Unleashing potential of evidence in knowledge-intensive dialogue generation . In ICASSP 2025-2025 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP) , pp. 1–5 . Cited by: §2 . 

C. Xu, Q. Sun, K. Zheng, X. Geng, P. Zhao, J. Feng, C. Tao, and D. Jiang (2023) WizardLM: empowering large language models to follow complex instructions . External Links: 2304.12244 Cited by: §2 . 

C. Xue and Z. Gao (2025) Structcoh: structured contrastive learning for context-aware text semantic matching . In Pacific Rim International Conference on Artificial Intelligence , pp. 300–315 . Cited by: §2 . 

C. Xue, D. Liang, P. Wang, and J. Zhang (2024) Question calibration and multi-hop modeling for temporal question answering . In Proceedings of the AAAI Conference on Artificial Intelligence , Vol. 38 , pp. 19332–19340 . Cited by: §2 . 

C. Xue, D. Liang, S. Wang, J. Zhang, and W. Wu (2023a) Dual path modeling for semantic matching by perceiving subtle conflicts . In ICASSP 2023-2023 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP) , pp. 1–5 . Cited by: §2 . 

C. Xue, Y. Wang, M. Liu, D. Liang, X. Han, P. Liu, X. Wu, C. Lu, L. Jiang, Y. Lu, H. Shi, S. Liang, M. Peng, and F. D. Salim (2026) Reason only when needed: efficient generative reward modeling via model-internal uncertainty . External Links: 2604.10072 , Link Cited by: §2 . 

M. Xue, D. Liu, K. Yang, G. Dong, W. Lei, Z. Yuan, C. Zhou, and J. Zhou (2023b) OccuQuest: mitigating occupational bias for inclusive large language models . External Links: 2310.16517 Cited by: §2 . 

S. Yao, D. Yu, J. Zhao, I. Shafran, T. L. Griffiths, Y. Cao, and K. Narasimhan (2023a) Tree of thoughts: deliberate problem solving with large language models . External Links: 2305.10601 Cited by: §2 . 

S. Yao, J. Zhao, D. Yu, N. Du, I. Shafran, K. Narasimhan, and Y. Cao (2023b) ReAct: synergizing reasoning and acting in language models . External Links: 2210.03629 Cited by: §2 . 

L. Yuan, Y. Chen, G. Cui, H. Gao, F. Zou, X. Cheng, H. Ji, Z. Liu, and M. Sun (2024) Revisiting out-of-distribution robustness in nlp: benchmarks, analysis, and llms evaluations . Advances in Neural Information Processing Systems 36 . Cited by: §2 . 

Z. Yuan, H. Yuan, C. Li, G. Dong, C. Tan, and C. Zhou (2023a) Scaling relationship on learning mathematical reasoning with large language models . External Links: 2308.01825 Cited by: §2 , §2 . 

Z. Yuan, H. Yuan, C. Tan, W. Wang, S. Huang, and F. Huang (2023b) RRHF: rank responses to align language models with human feedback without tears . External Links: 2304.05302 Cited by: §2 . 

X. Yue, X. Qu, G. Zhang, Y. Fu, W. Huang, H. Sun, Y. Su, and W. Chen (2023) MAmmoTH: building math generalist models through hybrid instruction tuning . arXiv preprint arXiv:2309.05653 . Cited by: §2 . 

X. Yue, T. Zheng, G. Zhang, and W. Chen (2024) MAmmoTH2: scaling instructions from the web . External Links: 2405.03548 Cited by: §2 . 

H. Zhang, S. Yang, X. Liang, C. Shang, Y. Jiang, C. Tao, J. Xiong, H. K. So, R. Xie, A. X. Chang, et al. (2025) Find your optimal teacher: personalized data synthesis via router-guided multi-teacher distillation . arXiv preprint arXiv:2510.10925 . Cited by: §2 . 

S. Zhang, L. Dong, X. Li, S. Zhang, X. Sun, S. Wang, J. Li, R. Hu, T. Zhang, F. Wu, and G. Wang (2024) Instruction tuning for large language models: a survey . External Links: 2308.10792 Cited by: §2 . 

X. Zhang, J. J. Zhao, and Y. LeCun (2015) Character-level convolutional networks for text classification . In NIPS , Cited by: §E.1 . 

X. Zhang and J. Wu (2024) Dissecting learning and forgetting in language model finetuning . In The Twelfth International Conference on Learning Representations , External Links: Link Cited by: §1 . 

Y. Zhao, L. Du, X. Ding, K. Xiong, T. Liu, and B. Qin (2024) Supervised fine-tuning achieve rapid task adaption via alternating attention head activation patterns . arXiv preprint arXiv:2409.15820 . Cited by: §1 . 

R. Zheng, R. Bao, Y. Zhou, D. Liang, S. Wang, W. Wu, T. Gui, Q. Zhang, and X. Huang (2022) Robust lottery tickets for pre-trained language models . arXiv preprint arXiv:2211.03013 . Cited by: §2 . 

W. Zhong, R. Cui, Y. Guo, Y. Liang, S. Lu, Y. Wang, A. Saied, W. Chen, and N. Duan (2023) AGIEval: a human-centric benchmark for evaluating foundation models . External Links: 2304.06364 Cited by: 1st item . 

C. Zhou, P. Liu, P. Xu, S. Iyer, J. Sun, Y. Mao, X. Ma, A. Efrat, P. Yu, L. Yu, et al. (2023a) Lima: less is more for alignment . arXiv preprint arXiv:2305.11206 . Cited by: §2 . 

J. Zhou, T. Lu, S. Mishra, S. Brahma, S. Basu, Y. Luan, D. Zhou, and L. Hou (2023b) Instruction-following evaluation for large language models . External Links: 2311.07911 Cited by: §2 . 

Appendix A Base Model Knowledge Limitations Supplement 

Dataset Domain Sample Size Evaluation 

MedQA Medical 12,873 Accuracy 

LegalBench Legal 8,452 F1-score 

TechFAQ Technology 5,621 pass@5 

FinanceBench Finance 10,150 EM 


Table 3: Statistics of the SFT datasets and their corresponding evaluation metrics. 

A.1 Experimental Datasets 

As shown in Table 3 , the experiment employs standard test sets from diverse domains to validate the consistency and efficacy of the method in augmenting knowledge across various fields. The specific datasets utilized are as follows: 

MedQA: Jin et al. ( 2020 ) comprises question-and-answer pairs in the medical domain, assessing the model’s proficiency in medical expertise. 

LegalBench: Guha et al. ( 2023 ) Focused on legal knowledge and question-answering, this dataset evaluates the model’s capacity to comprehend and interpret legal statutes and case law. 

TechFAQ: Liang et al. ( 2021 ) encompasses common issues in the information technology sector, testing the model’s grasp of technical knowledge, such as programming and network security. 

FinanceBench : Islam et al. ( 2023 ) Centered on financial topics, which measures the model’s understanding of economics and financial accounting. 

A.2 Experimental Baselines 

To evaluate the impact of different models before and after addressing the knowledge gap, employs the following representative LLMs as baselines: qwen-7b , qwen-14b , llama2-8B , llama2-13B . These baselines vary in parameter scales, allowing for a more comprehensive assessment of the adaptability and enhancement effects of the proposed method across each model. 

A.3 Algorithm of Knowledge-Enhanced Continue Pre-training 

Our "knowledge-enhanced continual pre-training" method, illustrated in Algorithm 1 , addresses pre-training knowledge limitations. The process starts by identifying SFT samples the base model fails to learn. These are processed via OpenIE 2 2 2 https://nlp.stanford.edu/software/openie.html ) into candidate knowledge triplets ( 𝒦 cand \mathcal{K}_{\text{cand}} ). As outlined in Step 1 of Algorithm 1 , model proficiency on 𝒦 cand \mathcal{K}_{\text{cand}} is assessed using pass@N and BoN accuracy to identify ’blind knowledge triplets’ ( 𝒦 blind \mathcal{K}_{\text{blind}} ). 

Algorithm 1 Knowledge Continue Pre-train 
1: Require: SFT dataset 𝒟 SFT \mathcal{D}_{\text{SFT}} , base model M base M_{\text{base}} 2: Ensure: Optimized base model 3: Step 1: Identify Knowledge Gaps 4: Extract unlearned samples into knowledge graph triples 𝒦 cand = { ( h , r , t ) } \mathcal{K}_{\text{cand}}=\{(h,r,t)\} . 5: Use BoN and pass@N indicators to locate blind areas: 
𝒦 blind = { k ∣ \displaystyle\mathcal{K}_{\text{blind}}=\{k\mid pass@10 ​ ( k ) < 0.2 \displaystyle\text{pass@10}(k)<0.2 

∧ BoN-5 Acc ( k ) < 0.1 } . \displaystyle\land\text{BoN-5 Acc}(k)<0.1\}. 

6: Step 2: Collect External Knowledge 7: for Each blind area entity e ∈ 𝒦 blind e\in\mathcal{K}_{\text{blind}} do 8: Use WikiData, Google Search, and other extended background knowledge to build corpus 𝒞 aug \mathcal{C}_{\text{aug}} . 9: end for 10: Step 3: Continue Pre-training 11: Mix general data with augmented corpus: 
𝒞 mix = 0.8 ​ 𝒞 general + 0.2 ​ 𝒞 aug . \mathcal{C}_{\text{mix}}=0.8\mathcal{C}_{\text{general}}+0.2\mathcal{C}_{\text{aug}}. 

12: Continue pre-training with 𝒞 mix \mathcal{C}_{\text{mix}} . 13: Step 4: Validate with SFT 14: Perform SFT on the updated model and evaluate the performance improvement. 15: return Optimized base model 
Step 2 details the construction of an augmented corpus ( 𝒞 aug \mathcal{C}_{\text{aug}} ) for these deficient areas using external resources (WikiData API, Google Search, OpenAI API). We prioritize collecting foundational information and conceptual explanations pertinent to the knowledge area, deliberately avoiding direct content from the original unlearned SFT samples to ensure CPT supplements understanding. This yields approximately 20 ± 1.1 20\pm 1.1 documents per area. 

In Step 3, 𝒞 aug \mathcal{C}_{\text{aug}} is mixed with a general pre-training dataset 𝒞 g ​ e ​ n ​ e ​ r ​ a ​ l \mathcal{C}_{general} (e.g., 0.8 ​ 𝒞 general + 0.2 ​ 𝒞 aug 0.8\mathcal{C}_{\text{general}}+0.2\mathcal{C}_{\text{aug}} , found effective in experiments – discussion in Appendix V), and the base model undergoes CPT on this mix. Step 4 validates the enhanced model via SFT and subsequent evaluation on standard benchmarks, demonstrating improved knowledge coverage and performance. 

Dataset Method Acc (%) pass@10 Learn Rate (%) 

MedQA Baseline (2 epoch SFT) 0.0 0.0 65.3 

Increase epoch to 10 +1.2 +1.5 66.8 

Continued pre-training + SFT +8.3 +10.5 82.1 

LegalBench Baseline (2 epoch SFT) 0.0 0.0 62.5 

Increase epoch to 10 +1.0 +1.3 63.8 

Continued pre-training + SFT +7.9 +9.8 80.5 

TechFAQ Baseline (2 epoch SFT) 0.0 0.0 68.1 

Increase epoch to 10 +1.4 +1.8 69.5 

Continued pre-training + SFT +8.7 +11.2 83.6 

FinanceBench Baseline (2 epoch SFT) 0.0 0.0 63.8 

Increase epoch to 10 +1.1 +1.6 65.4 

Continued pre-training + SFT +8.0 +10.1 81.7 


Table 4: Comparison of SFT performance by increasing training epochs and applying continued pre-training (CPT + SFT) across four datasets. Performance improvements are highlighted in red. 

A.4 Verification of the Unlearnability of Knowledge Blind Spots by Increasing SFT Epochs 

A.4.1 Experimental Design 

To further investigate the characteristics of knowledge blind spots in the base model, we designed a comparative experiment, addressing the following questions: Can the knowledge gaps of the base model be filled by increasing the number of training rounds (epochs) of SFT? The experimental results are presented in Table 4 . 

The results indicate that increasing the number of epochs in Supervised Fine-Tuning shows limited effectiveness in improving the model’s performance in areas where it lacks knowledge. For example, in the MedQA dataset, extending the training from 2 to 10 epochs only marginally increased the coverage rate of knowledge blind spots from 65.3% to 66.8%. This suggests that simply increasing the number of SFT training epochs does not significantly address the knowledge gaps in the base model. 

Dataset Field Size Evaluation 

ARC Science 7,787 Accuracy 

Common Commonsense 12,247 Accuracy 

SocialIQA Social 33,410 Accuracy 

MedMCQA Medical 187,995 Accuracy 


Table 5: SFT Dataset statistics and evaluation index. 

In contrast, continuing pre-training with knowledge enhancement significantly improves the model’s ability to cover these blind spots. For instance, in the TechFAQ dataset, the coverage rate increased from 68.1% to 83.6%. This underscores the importance of incorporating external knowledge during the pre-training stage to enable the base model to acquire missing knowledge, which is critical for effective SFT. Furthermore, the experimental results reveal a certain "unlearnability" of the base model’s knowledge blind spots. Even with additional SFT training epochs, the model struggles to master the missing knowledge. This highlights the importance of addressing these gaps during the pre-training stage. 

This finding emphasizes the critical role of knowledge injection in the pre-training stage in the optimization process of large-scale language models. For the knowledge blind spot of the base model, it is not enough to rely solely on SFT. External knowledge must be introduced through a continued pre-training phase for optimizing large-scale language models. 

Appendix B Conflicts Between SFT and Base Model Supplement 

Model ARC (+CPT) CommonQA (+CPT) SocialIQA (+CPT) MedMCQA (+CPT) 

Qwen 7B 12.3% → \rightarrow 8.8% (–3.5) 10.1% → \rightarrow 7.3% (–2.8) 11.7% → \rightarrow 8.8% (–2.9) 14.5% → \rightarrow 10.7% (–3.8) 

Qwen 14B 11.2% → \rightarrow 8.0% (–3.2) 9.3% → \rightarrow 6.8% (–2.5) 10.8% → \rightarrow 8.2% (–2.6) 13.1% → \rightarrow 9.6% (–3.5) 

LLaMA2 7B 13.1% → \rightarrow 9.5% (–3.6) 10.7% → \rightarrow 7.7% (–3.0) 12.3% → \rightarrow 9.2% (–3.1) 15.2% → \rightarrow 11.2% (–4.0) 

LLaMA2 13B 12.5% → \rightarrow 9.2% (–3.3) 9.8% → \rightarrow 7.1% (–2.7) 11.5% → \rightarrow 8.7% (–2.8) 14.3% → \rightarrow 10.6% (–3.7) 


Table 6: Relative reduction of conflict rates on the SFT dataset before and after Continued Pre-Training (CPT) for each model. Negative improvements indicate a decrease in conflict rates, consistently observed across benchmarks and model sizes. 

B.1 Experimental Datasets 

As presented in Table 5 , the experiment utilizes datasets from multiple domains to validate the consistency and effectiveness of the method augmenting knowledge across various fields, as: 

ARC(AI2 Reasoning Challenge): Clark et al. ( 2018 ) This dataset comprises science-related questions, categorized into easy and challenging levels, focusing on the model’s reasoning capabilities and knowledge in the scientific domain. 

CommonsenseQA: Talmor et al. ( 2019 ) A multiple-choice dataset designed for commonsense reasoning, requiring the model to possess extensive commonsense knowledge. It evaluates the model’s performance in handling questions that demand background knowledge and logical reasoning. 

SocialIQA: 3 3 3 https://huggingface.co/datasets/allenai/social_i_qa This dataset covers questions related to social commonsense reasoning, involving emotions, social norms, and interpersonal interactions. It focuses on the model’s understanding of social contexts and human behavior. 

MedMCQA: Pal et al. ( 2022 ) A multiple-choice dataset in the medical field, encompassing a wide range of medical knowledge and clinical reasoning. It tests the model’s ability to handle complex medical questions and support clinical decision-making. 

B.2 Algorithm for Resolving Calibration Conflicts Between SFT and Base Model 

The optimization strategy, which leverages high-confidence error detection and CPT, is outlined in Algorithm 2 . Initially, high-confidence error samples are identified by comparing the model’s predictions with the ground truth labels in the SFT dataset. If the model’s confidence in an incorrect prediction surpasses a predefined threshold, the sample is classified as a high confidence error and included to the error set ℰ \mathcal{E} . Subsequently, for each identified error sample, relevant knowledge is gathered from external sources, such as WikiData or other knowledge repositories, to construct an enhanced knowledge corpus 𝒦 i \mathcal{K}_{i} . This step ensures that the model acquires additional context and information to rectify its errors. Furthermore, domain-specific databases and academic papers are considered to be utilized for a more comprehensive knowledge base. Finally, the enhanced knowledge corpus is integrated with the general pre-training dataset at a specified ratio α \alpha , and the model undergoes continued pre-training with this combined dataset. This approach aims to enhance the model’s accuracy by targeting specific areas where it previously made high-confidence errors. The model’s effectiveness is subsequently evaluated through SFT and validation steps to confirm performance improvements. 

The experimental results are presented in Table 6 . From the perspective of the reduction in the data conflict rate, all models across the four datasets exhibit a significant decrease in conflict rates. This indicates that CPT effectively mitigates the knowledge conflicts between the model and the SFT data. Notably, Qwen 14B outperforms other models in reducing the conflict rate, likely due to its larger parameter scale. Furthermore, the most substantial reduction in conflict rate is observed on the MedMCQA dataset, suggesting that external knowledge retrieval and continued pre-training have a particularly pronounced effect on knowledge calibration in the medical domain. In summary, the observed reduction in the data conflict rate further validates the effectiveness of the high-confidence error detection-based method. CPT significantly mitigates model knowledge conflicts, thereby enhancing the model’s performance and reliability. 

Algorithm 2 Optimization Strategy Based on High-Confidence Error Detection and Continued Pre-training 
1: Input: SFT dataset 𝒟 SFT \mathcal{D}_{\text{SFT}} ; base model M base M_{\text{base}} ; confidence threshold T conf T_{\text{conf}} ; external knowledge source 𝒦 \mathcal{K} 2: Output: Optimized base model 3: Initialize high-confidence error set ℰ ← ∅ \mathcal{E}\leftarrow\emptyset 4: for all ( x , y SFT ) ∈ 𝒟 SFT (x,y_{\text{SFT}})\in\mathcal{D}_{\text{SFT}} do 5: Obtain model prediction distribution P model ​ ( y ∣ x ) P_{\text{model}}(y\mid x) using M base M_{\text{base}} 6: if P model ​ ( y ∣ x ) > T conf P_{\text{model}}(y\mid x)>T_{\text{conf}} and y ≠ y SFT y\neq y_{\text{SFT}} then 7: ℰ ← ℰ ∪ { ( x , y SFT ) } \mathcal{E}\leftarrow\mathcal{E}\cup\{(x,y_{\text{SFT}})\} 8: end if 9: end for 10: for all e i ∈ ℰ e_{i}\in\mathcal{E} do 11: Retrieve relevant knowledge from 𝒦 \mathcal{K} and construct a knowledge-enhanced corpus K i K_{i} 12: end for 13: Mix the aggregated knowledge-enhanced corpus with the general pre-training data according to the ratio α \alpha 14: Continue pre-training M base M_{\text{base}} on the mixed corpus 15: return the optimized base model 
Appendix C Knowledge Conflicts Between SFT Data Supplement 

C.1 Experimental Datasets 

Dataset Field Size Evaluation 

SQuAD General 150,000 EM 

CoQA Conversational 127,000 F1 

TriviaQA Trivia 95,000 Acc 

Natural Questions Web Search 307,373 EM 


Table 7: SFT Dataset statistics and evaluation index. 

To evaluate the model’s performance in knowledge conflict scenarios, we utilize a diverse set of question-answering datasets, each designed to test different aspects of the model’s knowledge and reasoning capabilities, and summarized in Table 7 : 

SQuAD (Stanford QA Dataset): Rajpurkar et al. ( 2016 ) A widely-used dataset for reading comprehension, focusing on extracting answers from provided passages. This dataset evaluates the model’s ability to handle context-specific information and resolve potential conflicts within the text. 

CoQA (Conversational Question Answering Dataset): Reddy et al. ( 2019 ) A dataset designed for conversational question answering, requiring the model to maintain context across multiple dialogue turns. This tests the model’s ability to ensure knowledge consistency in dynamic interactions. 

TriviaQA Joshi et al. ( 2017 ) : A large-scale dataset containing trivia questions spanning a wide range of topics. It challenges the model’s general knowledge and its ability to resolve conflicts between different information sources. 

Natural Questions(NQ): Kwiatkowski et al. ( 2019b ) based on user queries from Google Search, focusing on open-domain question answering. This dataset evaluates the model’s capacity to integrate information from diverse knowledge sources. 

Experiment Qwen-7B Qwen-14B LLaMA-7B LLaMA-13B 

Knowledge conflict 82.3% → \rightarrow 85.1% (+2.8) 84.5% → \rightarrow 87.2% (+2.7) 81.8% → \rightarrow 84.3% (+2.5) 83.6% → \rightarrow 86.5% (+2.9) 

+ deletion 82.3% → \rightarrow 83.8% (+1.5) 84.5% → \rightarrow 85.9% (+1.4) 81.8% → \rightarrow 83.2% (+1.4) 83.6% → \rightarrow 85.1% (+1.5) 

+ grouping 82.3% → \rightarrow 84.5% (+2.2) 84.5% → \rightarrow 86.6% (+2.1) 81.8% → \rightarrow 83.9% (+2.1) 83.6% → \rightarrow 85.8% (+2.2) 


Table 8: The indicators of sub-optimization strategies (deletion and grouping) applied to four baselines are shown. 

C.2 Algorithm of Knowledge Conflicts Between SFT Data 

Algorithm 3 Optimization Strategy Based on Conflict Detection and Conflict Sample Bucketing 
1: Input: SFT dataset set { D 1 , D 2 , … , D n } \{D_{1},D_{2},\dots,D_{n}\} ; semantic similarity threshold X X ; number of buckets B B 2: Output: Optimized SFT dataset 3: Initialize conflict group set 𝒞 ← ∅ \mathcal{C}\leftarrow\emptyset 4: for all sample pair ( s i , s j ) (s_{i},s_{j}) in the dataset do 5: Compute semantic similarity Sim ​ ( s i , s j ) \mathrm{Sim}(s_{i},s_{j}) 6: if Sim ​ ( s i , s j ) > X \mathrm{Sim}(s_{i},s_{j})>X then 7: Use GPT to determine the correctness of s i s_{i} and s j s_{j} 8: if s i s_{i} is incorrect then 9: Remove s i s_{i} from the dataset 10: else if s j s_{j} is incorrect then 11: Remove s j s_{j} from the dataset 12: else 13: 𝒞 ← 𝒞 ∪ { ( s i , s j ) } \mathcal{C}\leftarrow\mathcal{C}\cup\{(s_{i},s_{j})\} 14: end if 15: end if 16: end for 17: for all conflict group G ∈ 𝒞 G\in\mathcal{C} do 18: Evenly distribute samples in G G into B B buckets 19: end for 20: return the optimized SFT dataset 
The "Optimization Strategy Based on Conflict Detection and Conflict Sample Bucketing" method, as illustrated in Algorithm 3 , initiates by initializing an empty conflict group set. For each pair of samples within the dataset, the semantic similarity is computed by a Sentence-BERT model Edoardo Federici ( 2022 ) . If the similarity surpasses a predefined threshold, GPT-4 is employed to assess the correctness of the samples. Incorrect samples are subsequently removed from the dataset, whereas conflicting pairs are incorporated into the conflict group. Following this, the samples within each conflict group are evenly distributed into a designated number of buckets. The process concludes by returning the optimized dataset, ensuring improved quality and reduced conflicts. 

C.3 Deleting and Grouping Conflicting Data 

The experiment is to evaluate the role of knowledge conflict detection and conflict grouping strategies in resolving sample-level contradictions in conflict datasets during SFT as depicted in Table 8 . In comparison to directly merging datasets, the proposed strategies have consistently improved the accuracy of all baseline models. This outcome demonstrates that integrating conflict detection with perceptually coherent grouping can effectively mitigate the interference caused by conflicting knowledge during batch training. Furthermore, after the removal of conflict data, the accuracy of the model trained with conflict detection and grouping has increased by 1-5%. This indicates that segregating conflict samples can prevent performance degradation due to label inconsistencies. Lastly, regarding dynamic grouping, periodically re-evaluating data conflicts (dynamic grouping) ensures superior learning outcomes. By isolating contradictory examples into distinct groups, knowledge conflicts between datasets can be effectively managed. This strategy maximally reduces interference while preserving the value of high-quality samples. 

Appendix D Left-side Forgetting Supplement 

D.1 Experimental Datasets 

Dataset Field Data Size Evaluation 

CNN/DailyMail News 312,000 Acc 

XSum Extreme 226,000 Acc 

OpenWebText Language 800,000 Acc 


Table 9: SFT Dataset statistics and evaluation index. 

As shown in Table 9 , the experiment employs datasets from various domains to validate the consistency and effectiveness of the method in enhancing knowledge across different fields, including: 

CNN/DailyMail: See et al. ( 2017 ) A widely-used dataset for news summarization tasks, comprising news articles paired with their summaries. This dataset is designed to evaluate the model’s ability to generate concise and informative summaries. 

XSum: Narayan et al. ( 2018 ) An extreme summarization dataset, where each sample consists of a news article and a single-sentence summary. This dataset tests the model’s capability to produce highly abstractive summaries. 

OpenWebText: Gokaslan et al. ( 2019 ) An open-source text dataset derived from Reddit submissions, utilized for training and evaluating language models on diverse and conversational text data. 
Parameter Settings for Dynamic Resampling. 
Our dynamic resampling (Algorithm 4 ) uses two key parameters: evaluation frequency K K and performance drop threshold T d ​ r ​ o ​ p T_{drop} . We set K K to 500 training steps, balancing timely forgetting detection with computational cost. T d ​ r ​ o ​ p T_{drop} was empirically set to a 5% relative performance decrease on a development set, aiming to capture significant degradation while avoiding noise-induced over-triggering. These parameters were based on preliminary experiments; comprehensive sensitivity analysis remains future work. 

Algorithm 4 Dynamic resampling 
1: Input: SFT dataset set { D 1 , D 2 , … , D n } \{D_{1},D_{2},\dots,D_{n}\} , training step interval K K , accuracy drop threshold T T 2: Output: Optimized SFT model 3: Initialize training steps t = 0 t=0 4: Randomly shuffle all dataset samples 5: while Training is not completed do 6: Perform K K steps of training 7: Update training steps t = t + K t=t+K 8: for Each SFT dataset D i D_{i} do 9: Calculate current accuracy A i ​ ( t ) A_{i}(t) 10: Calculate accuracy change Δ ​ A i ​ ( t ) = A i ​ ( t − K ) − A i ​ ( t ) \Delta A_{i}(t)=A_{i}(t-K)-A_{i}(t) 11: if Δ ​ A i ​ ( t ) > T \Delta A_{i}(t)>T then 12: Resample from D i D_{i} and add to the current training batch 13: end if 14: end for 15: end while 16: return the optimized model 
D.2 Algorithm of Left-side Forgetting 

The "Dynamic Resampling" method, as outlined in Algorithm 4 , is designed to enhance the performance of an SFT model by adaptively adjusting the data based on accuracy changes. The process begins by initializing training steps and shuffling all datasets. During training, the algorithm performs a fixed number of training steps and updates the step count. For each SFT dataset, it calculates the current accuracy and the change in accuracy compared to the previous interval. If the accuracy drop exceeds the threshold, the algorithm resamples from the corresponding dataset and incorporates these samples into the current training batch. 

Type Description Proportion 

I. Base Model Knowledge Limitations 𝒫 exist ​ ( x ) = 0 \mathcal{P}_{\text{exist}}(x)=0 generate wrong predict 18.7% 

II. Conflicts Between SFT and Base Model D JS > 0.3 D_{\text{JS}}>0.3 cognitive conflict 13.2% 

III. Knowledge Conflicts Between SFT Data Wrong answer or multiple positions 14.1% 

IV. Left-side Forgetting Previous training data is forgotten 17.4% 

V. Insufficient Training SFT data is not fully learned 14.6% 


Table 10: Classification of unlearned phenomena in SFT and their corresponding proportions. 

Position ROUGE-L Strategy Gain 

First 10% data 0.41 0.53 +29% 

Middle data 0.57 0.59 +3.5% 

Last 10% data 0.61 0.60 -1.6% 


Table 11: ROUGE-L results and gain comparison. 

D.3 Analysis of Alleviating Left-sided Forgetting 

The dynamic re-sampling mechanism has significantly mitigated the problem of early - stage data forgetting. The ROUGE - L score of the first 10% of the training data has increased by 29% (from 0.41 to 0.53), while the performance of subsequent data has not been significantly impaired (the last 10% of the data has only decreased by 1.6%). As shown in Table 11 , the gain for data in the middle stage is relatively small (+3.5%), confirming that the forgetting phenomenon is most pronounced during the initial stage of training. 

Dataset Field Data Size Evaluation 

AG News News 120,000 Acc 

IMDB Movie Reviews 50,000 Acc 

MultiNLI NLI 433,000 Acc 

QQP Quora 404,000 Acc 


Table 12: SFT Dataset statistics and evaluation index. 

Appendix E Insufficient Training Supplement 

E.1 Experimental Datasets 

As shown in Table 12 , the experiment employs datasets from various domains to validate the consistency and effectiveness of the method in enhancing knowledge across different fields. Specifically, the datasets include: 

AG News Zhang et al. ( 2015 ) : The news articles are categorized into four classes: World, Sports, Business, and Sci/Tech. It is commonly used for text classification tasks, evaluating the model’s ability to categorize news articles accurately. 

IMDB Maas et al. ( 2011 ) : A dataset of movie reviews labeled as positive or negative, widely used for sentiment analysis tasks. This dataset tests the model’s capability to understand and classify the sentiment expressed in text. 

MultiNLI Williams et al. ( 2018 ) : A dataset for natural language inference (NLI) tasks, containing sentence pairs labeled with their relationship (entailment, contradiction, or neutral). It evaluates the model’s ability to understand the logical relationship between two sentences. 

Quora Question Pairs 4 4 4 https://www.kaggle.com/datasets/quora/question-pairs-dataset : A dataset consisting of question pairs from Quora, labeled as either duplicate or non-duplicate. It is used for duplicate question detection tasks, assessing the model’s ability to identify semantically similar questions. 

E.2 Algorithm of Insufficient Training 

Algorithm 5 Epoch Increment Strategy 
1: Input: SFT dataset D D , initial epoch E = 1 E=1 , evaluation function Eval ​ ( ⋅ ) \text{Eval}(\cdot) 2: Output: optimal training round E optimal E_{\text{optimal}} 3: Initialize P best = 0 P_{\text{best}}=0 4: while P E ≥ P best P_{E}\geq P_{\text{best}} do 5: Train the model to round E E 6: Calculate performance using validation set P E = Eval ​ ( Model ) P_{E}=\text{Eval}(\text{Model}) 7: if P E > P best P_{E}>P_{\text{best}} then 8: Update P best = P E P_{\text{best}}=P_{E} 9: Increase training round E = E + 1 E=E+1 10: else 11: Stop training 12: end if 13: end while 14: return the best training round E optimal = E − 1 E_{\text{optimal}}=E-1 
The "Epoch Increment Strategy" as illustrated in Algorithm 5 , is designed to identify the optimal number of training epochs for a model by progressively increasing the epoch count and evaluating performance. The strategy commences with an initial epoch count, iteratively trains the model, and assesses its performance on a validation set. If performance improves, the epoch count is incremented, and training continues. Conversely, if no further improvement is detected, training is terminated, and the optimal epoch count is recorded. This approach ensures the model is trained to achieve the best possible performance without overfitting. 

Appendix F Experiment and Analysis with Olmo2-7B 

To further investigate the Incomplete Learning Phenomenon (ILP) and validate our proposed CPT strategies on a recent open-source model, we conducted a series of experiments using OLMo2-7B OLMo et al. ( 2025 ) . OLMo2-7B is a 7-billion parameter model, part of the OLMo suite, trained on the Dolma dataset, a 5 trillion token open corpus. 

F.1 Experimental Setup 
Expanded Evaluation Framework. 
For a comprehensive assessment of OLMo2-7B’s capabilities before and after CPT and SFT, we employed an expanded evaluation framework. This framework assesses performance across four key dimensions, utilizing the following standard benchmarks and their respective metrics: 

• 
General Ability: MMLU (Massive Multitask Language Understanding) Hendrycks et al. ( 2021b , a ) and AGIEval Zhong et al. ( 2023 ) . 


• 
Reasoning Ability: BBH (Big-Bench Hard, specifically the 3-shot version) Suzgun et al. ( 2022 ) . 


• 
Professional Knowledge: GPQA (Graduate-Level Google-Proof Q&A Benchmark) Rein et al. ( 2024 ) and NQ (Natural Questions) Kwiatkowski et al. ( 2019a ) . 


• 
Multilingual Ability: MMLU-Multi (a multilingual version of MMLU). 


Performance was measured using the primary accuracy metric reported for each benchmark. 

F.2 Analysis of SFT Data in Relation to OLMo2 Pre-training Corpus 

To quantitatively understand the extent of pre-training knowledge limitations and potential conflicts OLMo2 might face when fine-tuned on typical Supervised Fine-Tuning (SFT) datasets, we conducted an in-depth analysis comparing our SFT data collections against OLMo2’s pre-training corpus (Dolma). 
Methodology for Knowledge Relationship Assessment. 
Our methodology involved three primary steps to assess the relationship between individual SFT knowledge items (derived from various SFT datasets used in our study) and the Dolma corpus: 

Dataset Type (SFT) Total SFT Entries Non-Existence Rate (%) Conflict Rate (%) 

General Ability 10,000 18.6 13.8 

Reasoning Knowledge 8,000 13.1 10.3 

Professional Knowledge 9,500 27.4 18.4 

Multilingual Knowledge 7,500 16.5 15.0 

Total 35,000 19.3 14.5 


Table 13: Analysis of Knowledge Existence and Conflict between SFT Data and OLMo2 Pre-training Data. 

1. 
Relevant Pre-training Data Retrieval: Given the 5 trillion token scale of the Dolma corpus, an exhaustive comparison is infeasible. Therefore, for each SFT dataset, we first identified thematic keywords and concepts. We then utilized a distributed indexing cluster built on Elasticsearch 5 5 5 Elasticsearch BV. Elasticsearch. https://www.elastic.co/elasticsearch/ . to retrieve the Top-100,000 text snippets from Dolma that were most thematically relevant to these SFT dataset concepts. This step aimed to narrow down the search space to potentially pertinent pre-training data. 


2. 
Precise Semantic Matching: From these retrieved 100k snippets, we employed an Apache Spark 6 6 6 Apache Software Foundation. Apache Spark. https://spark.apache.org/ . cluster in conjunction with a Sentence-BERT model Edoardo Federici ( 2022 ) to perform fine-grained semantic matching. For each specific knowledge item or query from our SFT samples, this step extracted text segments from the retrieved Dolma snippets that exhibited high semantic similarity to the SFT item. 


3. 
Knowledge Existence and Conflict Evaluation using GPT: The core assessment was performed using GPT as an expert evaluator. For each SFT knowledge item, alongside its semantically matched pre-trained text segments from Dolma, GPT was prompted to determine two aspects: 

(a) 
Knowledge Existence: Whether corresponding or semantically equivalent knowledge to the SFT item was present in the provided Dolma segments. 


(b) 
Knowledge Conflict: If such knowledge was found, whether the information in the Dolma segments conflicted with the SFT item (e.g., factual discrepancies, outdated information, or contradictory statements). 


The prompt for GPT involved presenting both the SFT item and the retrieved pre-trained snippets, requesting a categorical judgment (exists/not_exists) along with a brief justification. Based on GPT’s judgments, we calculated the “Knowledge Non-Existence Rate” (the proportion of SFT items not found in the relevant retrieved Dolma segments) and the “Knowledge Conflict Rate” (the proportion of SFT items that were found but assessed as conflicting with the Dolma segments). 

Statistical Results. 
We applied this analysis pipeline to SFT datasets categorized by the primary capability they aim to instill or evaluate. The aggregated statistical results, showing the Non-Existence Rate and Conflict Rate for different types of SFT data in relation to OLMo2’s pre-training corpus, are presented in Table 13 . 
Discussion of Findings. 
The results in Table 13 indicate that a substantial portion of knowledge targeted by common SFT datasets may either be new to OLMo2 or in direct conflict with information encountered during its pre-training (overall Conflict Rate of 14.5%). For instance, SFT data aimed at "Professional Knowledge" exhibited particularly high rates of both non-existence (27.4%) and conflict (18.4%). These figures quantitatively underscore the significant challenges an LLM like OLMo2 faces during SFT, highlighting the necessity for robust mechanisms to inject new knowledge and resolve conflicts, which our CPT strategy aims to provide. 

F.3 CPT Performance and Knowledge Relationship Analysis on OLMo2-7B 

Following the analysis of knowledge gaps and conflicts, we applied our Continued Pre-Training (CPT) strategy to the OLMo2-7B model. The CPT data was specifically curated to address the identified areas of knowledge non-existence and to help resolve conflicts observed between SFT data and OLMo2’s pre-training corpus. 
Quantitative Results. 
Table 14 presents the percentage change ( Δ % \Delta\% ) in OLMo2-7B’s performance on various standard benchmarks post-CPT. These changes are juxtaposed with the "Knowledge Non-Existence Rate" and "Knowledge Conflict Rate" of the SFT data collections used to target each evaluation dimension. 

Evaluation Dimension Benchmark Non-Existence Rate Conflict Rate Performance Change 

(SFT Data, %) (SFT Data, %) after CPT ( Δ % \Delta\% ) 

General Ability MMLU 12.7 8.3 -3.5 

General Ability AGIEval 15.2 6.8 -2.9 

Reasoning Ability BBH 9.4 4.1 -1.2 

Professional Knowledge GPQA 21.5 11.6 -6.8 

Professional Knowledge NQ 18.3 9.7 -4.3 

Multilingual Ability MMLU-Multi 23.1 15.4 -8.1 


Table 14: CPT Performance Change on OLMo2-7B Across Evaluation Dimensions 
Discussion of CPT Impact on OLMo2-7B Generalization. 
As demonstrated by Table 14 , the application of CPT on OLMo2-7B led to a decrease in performance across all listed general ability, reasoning, professional knowledge, and multilingual benchmarks. This outcome, while seemingly counterintuitive when CPT is intended for knowledge enhancement, requires careful interpretation in the context of the ILP. 

We hypothesize that this observed performance degradation on broad generalization benchmarks reflects the significant cognitive effort and internal recalibration the model undergoes when attempting to integrate substantial amounts of new knowledge and reconcile information that conflicts with its pre-trained biases. The Dolma pre-training corpus is vast, and the knowledge targeted by CPT, while relevant to specific SFT tasks, might represent a relatively small yet potentially disruptive portion compared to the model’s overall representations. 

Particularly in dimensions like "Professional Knowledge" and "Multilingual Ability," where the SFT data exhibited high Non-Existence and Conflict Rates (up to 23.1% and 15.4% respectively, as per Table 13 ), the more pronounced performance drops (e.g., -6.8% on GPQA, -8.1% on MMLU-Multi) might signify a period of significant representational adjustment. The model is actively working to incorporate information that is either entirely novel or contradicts its established knowledge base. This process could temporarily disrupt performance on tasks that rely on the stability of its previous, broader knowledge representations. 

This suggests a potential trade-off: while our CPT strategy can be effective for targeted knowledge injection and resolving specific conflicts at a granular level, the process of assimilating this specialized or corrective information can have complex, and sometimes initially detrimental, impacts on broadly measured generalization capabilities. This is particularly relevant for highly adaptable open-source models like OLMo2, which might be more sensitive to such shifts. These findings highlight the necessity for carefully calibrated CPT strategies and possibly subsequent SFT stages or other alignment techniques to re-harmonize newly acquired specialized knowledge with the model’s general abilities. This observation of a nuanced interplay between targeted knowledge enhancement and general capability retention is an important aspect of understanding and addressing the ILP. 

F.4 Case Studies of Knowledge Conflict Resolution in OLMo2-7B 

While Appendix F.3 discussed CPT’s broader impacts on OLMo2-7B’s generalization, this section presents qualitative case studies illustrating its effectiveness in resolving specific knowledge conflicts at a granular level, as detailed in Table 15 . These examples show how model outputs shifted post-CPT to better align with SFT data. 
Timeliness Conflicts. 
When SFT data presented updated facts conflicting with OLMo2’s outdated pre-trained knowledge, CPT helped align the model with the newer information. For instance, when queried about a topic with a recently changed status (e.g., "Who is the current US President?", where the SFT data reflects a more recent administration than the base model’s cutoff), the post-CPT OLMo2 model showed an increased tendency to provide the SFT-aligned, more current answer. In contrast, its pre-CPT responses often defaulted to the older knowledge embedded during pre-training, potentially yielding factually outdated outputs. This shift demonstrates CPT’s effectiveness in resolving knowledge conflicts by prioritizing up-to-date supervised signals over stale pre-trained priors. 
Disciplinary Controversies or Evolving Terminology. 
When SFT data introduced perspectives on disciplinary controversies or newer terminology that differed from or were entirely absent in the model’s pre-training, CPT facilitated the incorporation of these new viewpoints by recalibrating the model’s internal priors. For example, if pre-trained OLMo2 leaned towards an established theory for a scientific question (e.g., "String Theory" for quantum gravity), and the SFT data emphasized an emerging alternative (e.g., "Loop Quantum Gravity"), the post-CPT model not only acknowledged but often leaned toward the SFT-emphasized perspective in its responses. A similar effect was observed for evolving terminology: when SFT data highlighted modern techniques such as "LayerScale" for neural network regularization—over older, more prevalent terms like "Dropout" from the pre-training era—the post-CPT model adapted its lexical and conceptual usage accordingly. This demonstrates CPT’s capacity to update both factual stances and technical vocabulary in alignment with contemporary supervised signals. 
Multilingual Ambiguities and Geo-Specificity. 
CPT also demonstrated utility in resolving conflicts arising from multilingual contexts or geo-specific information not well-represented in the primarily English-centric pre-training. For instance, if an SFT query used a Chinese geographical name (e.g., "库珀蒂诺" for Cupertino when asking about "Apple Inc. headquarters"), the post-CPT OLMo2 showed improved understanding and response generation within that specific Chinese language context, compared to a pre-CPT tendency to default to English-based processing or an inability to link the Chinese entity correctly. 
Cross-Cultural Differences and Regional Legal Nuances. 
Similarly, for knowledge involving cultural nuances or regional legal differences that might conflict with a more "default" or globally prevalent understanding in the pre-training data, CPT helped sensitize the model to SFT-provided specifics. For example, if SFT data provided context on the meaning of a gesture in a specific culture (e.g., a headshake in India signifying affirmation) that differed from a Western interpretation, post-CPT OLMo2 was more likely to reflect this SFT-aligned, culturally specific understanding. Likewise, for regional legal details (e.g., differing age limits for data privacy for minors across jurisdictions like GDPR vs. China), CPT helped the model adjust its responses based on the geographical context emphasized in the SFT data. 
Summary of Case Study Observations. 
These qualitative examples from various conflict types consistently demonstrate that CPT can effectively steer OLMo2-7B’s responses towards SFT-aligned knowledge in instances of direct conflict. By encouraging the model to update its internal representations or output tendencies for these particular conflicting concepts, CPT serves as a valuable tool for targeted knowledge correction. This granular effectiveness is crucial for tailoring LLMs to specific, nuanced requirements, complementing the broader (and sometimes complex) performance changes observed on general benchmarks, as discussed in Appendix F.3 . 

F.5 Summary and Implications of OLMo2 Experiments 

The experiments conducted with the OLMo2-7B model provide several critical insights into the Incomplete Learning Phenomenon (ILP) and the application of our proposed Continued Pre-Training (CPT) strategies to a recent, open-source LLM. 

First, quantitative analysis (Appendix F.2 ) confirmed that significant SFT knowledge portions are absent from or conflict with OLMo2’s pre-training corpus. This highlights the prevalence of pre-training knowledge limitations and conflicts as ILP root causes, corroborating findings on other architectures. 

Second, CPT’s application to OLMo2-7B showed nuanced impacts on generalization benchmarks (Appendix F.3 ). Observed performance decreases post-CPT likely indicate representational adjustments as the model integrates new or contradictory, task-relevant information. This suggests a trade-off between targeted knowledge injection and preserving broad generalization, especially in adaptable open models, potentially requiring further fine-tuning to re-optimize general capabilities after specialized CPT. 

Third, despite the complex interplay with broad generalization metrics, qualitative case studies (Appendix F.4 ) demonstrated CPT’s clear effectiveness at a granular level. In specific instances of knowledge conflict (e.g., timeliness, disciplinary views, cultural nuances), CPT successfully steered OLMo2’s responses to align more closely with SFT-provided knowledge, showcasing its utility as a targeted correction mechanism. 

In conclusion, the OLMo2 experiments enrich our understanding of ILP by providing a detailed look at an open-source model’s interaction with SFT data and CPT. They affirm the challenges posed by knowledge gaps and conflicts and demonstrate that while CPT is a potent tool for addressing these specific issues at a fine-grained level, its broader impact on model capabilities can be complex and warrants careful, context-dependent application and evaluation-especially when updating factual knowledge. These findings reinforce the need for comprehensive diagnostic frameworks and adaptable mitigation strategies in our main work. 

Conflict Type Example Scenario (Query/Context) Pre-trained OLMo2 Knowledge Tendency (Illustrative Output/Bias) SFT Knowledge Version (Target Output/Fact) OLMo2 Output Tendency (Post-CPT) 

Timeliness Conflict Query: "Who is the current US President?" (SFT data updated to 2023 context) Might output a president reflecting its pre-training data cutoff (e.g., "Donald Trump"). Specifies the president as per 2023 SFT data (e.g., "Joe Biden"). Increased tendency to output the SFT-aligned, more current president. 

Disciplinary Controversy Query: "What is the optimal theoretical path for quantum gravity?" May favor a historically prominent theory (e.g., "String Theory"). SFT data emphasizes an emerging perspective (e.g., "Loop Quantum Gravity"). Output may present a more balanced view, acknowledge multiple perspectives, or lean towards the SFT-emphasized theory. 

Multilingual Ambiguity / Geo-specificity Query (SFT in Chinese): "苹果公司总部的坐标是什么？" (Coordinates of Apple Inc. headquarters?) Primarily processes based on English name or common knowledge, may struggle with direct Chinese geo-entity. SFT provides query/context with the Chinese geographical name "库珀蒂诺" (Cupertino). Improved understanding and response generation within the Chinese language context for the query. 

Cross-cultural Differences Query: "Meaning of a headshake gesture in India." Default interpretation might be Western-centric (e.g., negation). SFT provides context for South Asian interpretation (e.g., affirmation or other nuances). Output demonstrates more context-dependent judgment, aligning with the SFT-provided cultural nuance. 

Terminology Evolution Query: "Describe methods for neural network regularization." May primarily list older, well-established methods (e.g., "Dropout"). SFT introduces or emphasizes newer terminology/methods (e.g., "LayerScale"). Output incorporates or gives due consideration to newer terminology/methods, possibly alongside established ones. 

Regional Legal Differences Query: "Age limit for data privacy protection of minors in [Specific Region]." May default to a widely known regulation (e.g., GDPR: 16 years). SFT specifies a different age for the particular region mentioned (e.g., China: 14 years). Adjusts response based on the specific geographical context provided in the SFT data or query. 


Table 15: Typical Case Analysis of Knowledge Conflict Resolution in OLMo2-7B via CPT. 
Experimental support, please view the build logs for errors. Generated by L A T E xml . 
Instructions for reporting errors 

We are continuing to improve HTML versions of papers, and your feedback helps enhance accessibility and mobile support. To report errors in the HTML that will help us improve conversion and rendering, choose any of the methods listed below: 

Click the "Report Issue" ( ) button, located in the page header. 

Tip: You can select the relevant text first, to include it in your report. 

Our team has already identified the following issues . We appreciate your time reviewing and reporting rendering errors we may not have found yet. Your efforts will help us improve the HTML versions for all readers, because disability should not be a barrier to accessing research. Thank you for your continued support in championing open access for all. 

Have a free development cycle? Help support accessibility at arXiv! Our collaborators at LaTeXML maintain a list of packages that need conversion , and welcome developer contributions . 
We gratefully acknowledge support from our major funders , member institutions , , and all contributors. About · Help · Contact · Subscribe · Copyright · Privacy · Accessibility · Operational Status (opens in new tab) Major funding support from 