# Literature Review: From Prompt to Render — A Systematic Literature Review on LLMs for Educational Video/Animation Generation

**Date:** 2026-08-06 (Round 1) / 2026-08-13 (Round 2 — SLR expansion)
**Query:** From Prompt to Render: A Systematic Literature Review on Large Language Models for Educational Video/Animation Generation — expanded from a narrative survey (Round 1, 15 sources) into a full SLR with search strategy, inclusion/exclusion criteria, PRISMA-style selection flow, and an animation-specific literature thread (Round 2, +10 primary sources, +2 methodology references, +2 related-work secondary studies).
**Verification status:** Two independent Post-Flight (CoVe) runs — Round 1 block and Round 2 blocks at the end of this document.

---

## Summary

The last eighteen months have seen a sharp pivot in how AI-generated educational video is built. Early systems (2023-era diffusion text-to-video models like ModelScope, and general talking-head synthesis) treated "video" as a single pixel-generation problem: a prompt goes in, a clip comes out. The architectures surveyed here show the field abandoning that approach almost entirely for *structured, agentic* pipelines — an LLM (or a team of LLM agents) first produces an intermediate, checkable artifact (a script, a set of editable slides, executable code, a structured event graph) and only then renders it deterministically into video. This shift is driven by exactly the failure mode end-to-end video diffusion models cannot fix: educational content requires "strict logical rigor and precise knowledge representation" (Yan et al., 2026), which pixel-space generation has no mechanism to guarantee.

Benchmarking has followed the same split. General video-generation benchmarks (VBench, EvalCrafter) evaluate *any* text-to-video output on dimensions like temporal consistency, motion smoothness, and text-video alignment — none of which say anything about whether a viewer learned something. A newer, education-specific generation of benchmarks (SlidesBench, MMMC/TeachQuiz, Paper2Video's PresentQuiz/IP-Memory suite) has emerged specifically because the general-purpose metrics don't transfer, but these are still new, small, and largely self-reported by the groups that built the generation systems they evaluate.

The gap this survey's title points at is real and is the central finding here: **almost no paper in this space measures learning outcomes with a controlled study**. Of the ~19 papers reviewed, exactly one (Stavrinou et al., 2025, "The Reel Deal") ran a genuine user study measuring quiz performance and cognitive load against a control condition; one other (Leinonen, Zhang & Hellas, 2026) deployed AI-generated slides in a real course and asked students to blind-rate them. Everything else — including the field's most cited benchmarks — measures a proxy: visual quality, design coherence, text-video alignment, or (at best) whether a separate LLM judge, watching the video, can answer quiz questions about it. That last category (TeachQuiz, PresentQuiz) is the closest thing to a pedagogical-effectiveness metric currently in circulation, and it is itself a proxy — an LLM answering quiz questions after "watching" a video is not a human learner retaining knowledge.

## Key Papers

### Yan, Wu, Xie, Shi, Xia & Huang (2026) — LASEV: Beyond End-to-End Video Models
- **Main contribution:** A hierarchical multi-agent system — an Orchestrating Agent supervising a Solution Agent, an Illustration Agent, and a Narration Agent — that produces a structured, executable video script rather than synthesizing pixels directly, explicitly to fix the "logical rigor and precise knowledge representation" gap in end-to-end video models.
- **Method:** Multi-agent orchestration → deterministic compilation of the structured script into final video.
- **Key finding:** Reports production at >1M videos/day with >95% cost reduction vs. industry standard — a scale/cost claim, not a learning-outcome claim. Accepted at ACM SIGKDD 2026.
- **Relevance:** The clearest statement in the literature of *why* pixel-space T2V models are being abandoned for educational content specifically.

### Chen, Lin & Shou (2025) — Code2Video: A Code-centric Paradigm for Educational Video Generation
- **Main contribution:** Planner → Coder → Critic agent pipeline that generates *executable Manim code* rather than pixels, giving the output the reproducibility and editability of source code.
- **Method:** VLM-based Critic refines spatial layout via "visual anchor prompts"; introduces the MMMC benchmark (professionally produced, discipline-specific educational videos).
- **Key finding:** 40% improvement over direct code generation; introduces **TeachQuiz**, a metric that has a VLM "unlearn" a concept, then measures how much knowledge it recovers by watching the generated video — the closest thing in this literature to a knowledge-transfer metric.
- **Relevance:** TeachQuiz is a template worth naming explicitly in any evaluation-gap discussion — it is a genuine attempt at outcome measurement, but the "learner" is an LLM, not a student.

### Zhu, Lin & Shou (2025) — Paper2Video: Automatic Video Generation from Scientific Papers
- **Main contribution:** PaperTalker, a multi-agent framework producing slides + subtitles + speech + talking-head video from a paper, with parallelized slide-wise generation.
- **Method:** Introduces the first benchmark pairing 101 research papers with author-created presentation videos/slides/speaker metadata.
- **Key finding:** Four purpose-built metrics — Meta Similarity, PresentArena, **PresentQuiz**, and IP Memory — the most metric-diverse evaluation suite found in this survey.
- **Relevance:** PresentQuiz is architecturally similar to Code2Video's TeachQuiz (quiz-based knowledge-transfer proxy); IP Memory (does the video preserve the paper's key claims) is a rare attempt at a factual-fidelity metric.

### Zheng, Guan, Kong et al. (2025) — PPTAgent: Generating and Evaluating Presentations Beyond Text-to-Slides
- **Main contribution:** Two-stage, edit-based slide generation (analyze reference decks for structural patterns → draft outline → generate via editing actions), explicitly optimizing for design and structural coherence, not just content.
- **Method:** Companion evaluation framework **PPTEval** scoring Content, Design, and Coherence.
- **Key finding:** Substantially outperforms prior automatic presentation generators on all three PPTEval dimensions.
- **Relevance:** PPTEval is the most-cited slide-specific evaluation framework in this space; none of its three dimensions measure pedagogical effect.

### AutoPresent / SlidesBench (2025), arXiv:2501.00912
- **Main contribution:** An 8B Llama-based model trained on 7k instruction→code pairs for slide generation, performing comparably to GPT-4o.
- **Method:** Introduces **SlidesBench** — 7k train / 585 test examples from 310 real slide decks across 10 domains, with both reference-based (similarity to a target) and reference-free (design quality alone) evaluation tracks.
- **Key finding:** Programmatic (code-based) generation methods produce higher-quality, more editable slides than end-to-end image generation.
- **Relevance:** SlidesBench is the largest, most systematically constructed slide-generation benchmark found in this survey — but its metrics are design/similarity metrics, not learning metrics.

### Aggarwal & Bhand (2025) — PASS: Presentation Automation for Slide Generation and Speech
- **Main contribution:** Generalizes slide+narration generation beyond academic papers to arbitrary Word documents.
- **Method:** LLM-based evaluation framework scoring relevance, coherence, and redundancy.
- **Key finding:** Public code/dataset release for reproducibility.
- **Relevance:** A representative example of the still-common pattern of using an LLM to judge an LLM's own output category (relevance/coherence) rather than measuring downstream effect on a human audience.

### Holmberg (2025) — Generating Narrated Lecture Videos from Slides with Synchronized Highlights
- **Main contribution:** A highlight-alignment module mapping narration to specific slide regions, combining Levenshtein-distance and LLM-based semantic alignment at configurable granularity.
- **Method:** Evaluated on 1,000 manually annotated slides.
- **Key finding:** LLM-based alignment reaches F1 > 92% for highlight location accuracy; ~$1/video-hour, ~100× cheaper than manual production.
- **Relevance:** A rare case with a genuine, human-annotated ground truth and a real accuracy number — but the metric (highlight placement accuracy) is a production-fidelity metric, not a learning metric.

### Islam, Manik & Wang (2025) — ALIVE: Avatar-Lecture Interactive Video Engine
- **Main contribution:** Real-time interactive avatar lecture system running fully on local hardware, combining avatar-delivered explanation, content-aware (semantic + timestamp) retrieval, and in-video Q&A.
- **Method:** Demonstrated on a medical-imaging course; lightweight embedding models + progressive preloading for responsiveness.
- **Key finding:** Local deployment + content-aware retrieval materially improves interactivity (system-level demonstration, not a controlled learning-outcome study).
- **Relevance:** Represents the "avatar/narration synthesis" architecture family named in this review's scope; evaluation here is almost entirely systems-level (latency, retrieval accuracy), not pedagogical.

### Huang et al. (2024) — VBench: Comprehensive Benchmark Suite for Video Generative Models (CVPR 2024) / VBench++ (2024)
- **Main contribution:** The most widely adopted general-purpose text-to-video benchmark, decomposing "video quality" into 16 hierarchical, disentangled dimensions (subject consistency, motion smoothness, temporal flickering, spatial relationships, etc.).
- **Method:** Tailored prompts + automated evaluators per dimension, validated against human perception judgments.
- **Key finding:** Provides fine-grained, per-dimension rankings across major T2V models.
- **Relevance:** The default benchmark any "educational video" system built on a general T2V backbone would be compared against — and none of its 16 dimensions touch content accuracy or comprehension.

### Liu, Cun, Liu et al. (2023/2024) — EvalCrafter: Benchmarking and Evaluating Large Video Generation Models (CVPR 2024)
- **Main contribution:** 17 objective metrics spanning visual quality, content, and motion, combined with subjective user-opinion scores, to produce a reliable model ranking.
- **Method:** Open-source toolkit (GitHub) pairing automated metrics with human evaluation.
- **Key finding:** Established one of the two dominant general T2V evaluation toolkits (alongside VBench).
- **Relevance:** Same gap as VBench — general video-quality benchmarking, no education-specific or comprehension-specific dimension.

### Liu, Xiang, Li et al. (2024, rev. 2026) — A Survey of AI-Generated Video Evaluation (AIGVE)
- **Main contribution:** A meta-survey formalizing "AI-Generated Video Evaluation" as a field, taxonomizing existing approaches into metric-based, human-involved, and emerging model-centered (LLM/VLM-as-judge) evaluation.
- **Method:** Literature synthesis across quality, semantic accuracy, instruction alignment, and real-world consistency dimensions.
- **Key finding:** Explicitly argues current evaluation frameworks are insufficient for video's "multifaceted," temporally complex nature and calls for more sophisticated systems.
- **Relevance:** The strongest existing meta-level acknowledgment that AIGVE lags generation capability — this survey's own "evaluation gaps" pillar sits directly inside the gap this paper identifies, narrowed specifically to the educational-effectiveness axis that even this AIGVE survey does not focus on.

### Stavrinou, Constantinides, Belk, Vassiliou, Liarokapis & Constantinides (2025) — The Reel Deal: Designing and Evaluating LLM-Generated Short-Form Educational Videos
- **Main contribution:** ReelsEd, an LLM-based system converting long-form lecture video into short-form "reels" while preserving instructor-authored material.
- **Method:** A genuine controlled **user study** — 62 university students, comparing reels against traditional long-form video on engagement, quiz performance, task efficiency, and cognitive load.
- **Key finding:** Reels outperformed long-form video on engagement, quiz performance, and task efficiency *without increasing cognitive load*; students reported high confidence in and appreciation for the system's pedagogical design.
- **Relevance:** **The single strongest learning-outcome evaluation found in this entire survey.** It is the exception that proves the rule: everything else in this list evaluates the artifact; this evaluates the learner.

### Leinonen, Zhang & Hellas (2026) — AI-Generated Slides: Are They Good? Can Students Tell?
- **Main contribution:** Real classroom deployment of AI-generated slides (from instructor notes) built with five different tools (NotebookLM, Claude, M365 Copilot, Cursor, Claude Code), with instructors pre-screening quality before deployment.
- **Method:** Blind student ratings of deployed AI-generated vs. instructor-created slides in an actual course.
- **Key finding:** Coding-assistant-style tools produced the most accurate/complete/pedagogically sound slides; students **could not reliably distinguish** AI-generated from instructor-made slides and rated them similarly — though slides *suspected* of being AI-generated were rated lower, a bias effect independent of actual quality.
- **Relevance:** One of only two papers in this survey with a real classroom deployment and human (student) judges; also surfaces a specific evaluation confound (perception bias) that artifact-only benchmarks cannot detect.

### "Hallucination to Truth" survey (2026), arXiv:2508.03860 — Review of Fact-Checking and Factuality Evaluation in LLMs
- **Main contribution:** Systematic review of how LLM-generated content is checked for factual accuracy, covering RAG-based mitigation, domain-specific fine-tuning, and the limits of self-evaluation without external validation.
- **Method:** Literature synthesis.
- **Key finding:** LLMs cannot reliably self-evaluate their own factual claims without external grounding (knowledge graphs, retrieval, human oversight) — directly relevant to educational content, where an unchecked factual error is pedagogically worse than a stylistic flaw.
- **Relevance:** None of the video/slide-generation papers surveyed above report a dedicated factual-accuracy metric on their *generated educational content specifically* — this survey establishes that the general problem is known and largely unsolved, which sharpens rather than closes the gap.

## Thematic Organization

### Architectures: from pixels to structured intermediates

The architectural throughline across nearly every 2025-2026 system surveyed is **decomposition**: instead of one model mapping prompt → pixels, systems now insert a checkable, editable, or executable intermediate representation between the LLM and the rendered output.

- **Script/event-graph intermediates** — LASEV's "structured executable video script," compiled deterministically (Yan et al., 2026).
- **Code intermediates** — Code2Video's executable Manim code (Chen, Lin & Shou, 2025), which trades some visual richness for reproducibility, editability, and (crucially) the ability to run a Critic agent against the code rather than against raw pixels.
- **Slide + multimodal-channel intermediates** — PaperTalker's slides/subtitles/speech/talking-head decomposition (Zhu, Lin & Shou, 2025); ALIVE's avatar + retrieval + Q&A decomposition (Islam, Manik & Wang, 2025).
- **Pure slide-code intermediates** — PPTAgent's edit-action sequences (Zheng et al., 2025) and AutoPresent's instruction→code pairs (2501.00912), both explicitly finding that programmatic generation beats direct image generation for editability and quality.

General-purpose text-to-video diffusion/transformer models (Sora, VideoPoet, CogVideoX, ModelScope, VideoCrafter2 — as characterized in the general T2V literature surveyed via search, not individually re-verified here) remain the substrate for the *rendering* step in some pipelines, but essentially no educational-video-specific system surveyed here treats a diffusion model as the entire pipeline. This is the paper's first architectural claim: **agentic decomposition, not end-to-end generation, is now the dominant educational-video architecture.**

### Benchmarks: general-purpose vs. education-specific, and the metrics gap between them

Two generations of benchmark coexist:

1. **General T2V benchmarks** (VBench/VBench++, Huang et al. 2024; EvalCrafter, Liu et al. 2024) — mature, widely adopted, methodologically rigorous *for their stated purpose*, which is video-generation quality: temporal consistency, motion smoothness, text-video semantic alignment, visual fidelity. Neither benchmark has a dimension for factual correctness of spoken/depicted content or comprehension.
2. **Education-specific benchmarks**, all published within roughly the last year: SlidesBench (slide design/similarity), MMMC + TeachQuiz (Code2Video), and the Paper2Video 101-paper benchmark with its Meta Similarity / PresentArena / PresentQuiz / IP Memory suite. These are a direct response to generation 1's inadequacy for this domain, and they represent real progress — TeachQuiz and PresentQuiz in particular are the first metrics in this literature that ask "did watching this convey the intended knowledge?" rather than "does this look/sound right?"

The catch, and the paper's second architectural/methodological claim: **every education-specific "knowledge transfer" metric found in this survey substitutes an LLM/VLM judge for a human learner.** TeachQuiz has a VLM "unlearn" and re-learn from the video; PresentQuiz appears to follow a similar quiz-based, judge-model pattern. This is a reasonable and scalable proxy, but it inherits every known limitation of LLM-as-judge evaluation (the AIGVE survey's own "emerging model-centered methods" category, Liu, Xiang, Li et al. 2024/2026) and has an unresolved construct-validity question: does a VLM's post-hoc quiz performance actually correlate with a human student's?

### Evaluation gaps: what's measured vs. what matters

This is where the review's title's third pillar concentrates the most consequential finding. Ranking what is actually measured across the ~19 papers, from most- to least-common:

- **Visual/production quality** (near-universal): VBench, EvalCrafter, PPTEval's Design dimension, Code2Video's aesthetic VLM-judge score.
- **Structural/design coherence**: PPTEval's Coherence dimension, SlidesBench's design-quality track.
- **Text-content alignment / similarity to a reference**: SlidesBench's reference-based track, Paper2Video's Meta Similarity, PASS's relevance/coherence/redundancy scoring.
- **Knowledge-transfer proxy via LLM/VLM judge**: TeachQuiz, PresentQuiz — present, but rare, and unvalidated against human outcomes in the papers that introduce them.
- **Factual accuracy of the generated educational content itself**: effectively absent as a *dedicated, reported metric* in every generation-system paper surveyed; the general factuality/hallucination literature (arXiv:2508.03860) establishes the problem exists and is hard, but no paper here closes the loop by applying a factuality metric to its own generated video/slide content.
- **Actual human learning outcomes** (quiz performance, retention, engagement, cognitive load, in a controlled comparison): exactly one paper (Stavrinou et al., 2025).
- **Real classroom deployment with human perception/quality judgment**: exactly one additional paper (Leinonen, Zhang & Hellas, 2026).
- **Accessibility** (captioning quality, multilingual support, disability accommodation, cognitive-load-adjusted pacing for diverse learners): not addressed as a dedicated evaluation axis in any paper surveyed here.

## Gaps and Opportunities

1. **The learning-outcome evaluation gap is the field's central, structural weakness.** Two out of roughly nineteen papers surveyed measure anything about human learners; the rest measure the artifact. This is not a minor omission — for a literature whose stated purpose is *educational* video generation, this is the field evaluating itself on almost everything except its actual goal. Any research program (including a future paper matching this survey's own title) has an immediately obvious, high-value contribution available: a controlled study, or a standard benchmark protocol, that measures retention/comprehension against a human control group across *multiple* systems, not just one lab's own tool.

2. **LLM/VLM-as-judge knowledge-transfer metrics (TeachQuiz, PresentQuiz) need external validation against human learners.** These are the most promising proxy metrics in the current literature, but neither Code2Video nor Paper2Video reports a human-subject correlation study showing the VLM-judge score actually predicts human quiz performance. This is a concrete, tractable next study: run TeachQuiz/PresentQuiz and a human-subject quiz on the same video set and report the correlation.

3. **Factual accuracy of generated educational content is measured nowhere in this literature, despite the general factuality/hallucination problem being well documented.** Every reviewed generation system reports design, coherence, or alignment metrics; none reports a dedicated fact-checking pass against its own generated narration/slide text, despite RAG-based and knowledge-graph-based mitigation techniques being available (per the "Hallucination to Truth" survey). This is a direct, low-effort extension available to any of the surveyed systems.

4. **Accessibility is entirely unaddressed as an evaluation axis.** No paper surveyed reports caption quality, multilingual generation fidelity, or evaluation across learners with different accessibility needs (e.g., cognitive load for neurodivergent learners, or comprehension for non-native speakers of the narration language). Given several of these systems (ALIVE, ReelsEd) are explicitly aimed at real classroom use, this is a significant, addressable blind spot.

5. **The architecture and benchmark literatures are converging faster than the evaluation-methodology literature.** New architectures (LASEV, Code2Video, PaperTalker) and new benchmarks (MMMC, the Paper2Video benchmark) are appearing roughly monthly; the AIGVE meta-survey's call for better evaluation methodology (2024/2026) has not yet produced a widely adopted, cross-system, human-outcome-validated standard comparable to what VBench achieved for general video quality. There is room for a "VBench for pedagogical effectiveness."

## Suggested Next Steps

- If this is heading toward an original contribution (not just a survey): the highest-leverage next step is a **cross-system human-subject study** — take 2-3 of the surveyed generation systems (e.g., Code2Video, PPTAgent+narration, a general T2V baseline) and run the same Stavrinou-et-al.-style controlled comparison (quiz performance, cognitive load, engagement) across all of them, since currently every learning-outcome result in the literature comes from a single lab evaluating its own single system.
- Validate TeachQuiz/PresentQuiz against human quiz performance on a shared video set — a focused, tractable paper on its own.
- Watch for a "VBench-for-education" benchmark; none exists yet per this search, and the gap analysis above suggests it is the most obviously missing artifact in the field.
- Re-run targeted searches closer to submission time for `Code2Video` (ICML 2026, per its GitHub repo tag) and `PPTAgent` (EMNLP 2025, per its ACL Anthology listing) to confirm final camera-ready venue/citation details before finalizing any BibTeX used in a submitted paper — both were captured here at preprint/proceedings-adjacent stage.

## BibTeX Entries

```bibtex
@article{yan2026lasev,
  title   = {Beyond End-to-End Video Models: An {LLM}-Based Multi-Agent System for Educational Video Generation},
  author  = {Yan, Lingyong and Wu, Jiulong and Xie, Dong and Shi, Weixian and Xia, Deguo and Huang, Jizhou},
  journal = {arXiv preprint arXiv:2602.11790},
  year    = {2026}
}

@article{chen2025code2video,
  title   = {Code2Video: A Code-centric Paradigm for Educational Video Generation},
  author  = {Chen, Yanzhe and Lin, Kevin Qinghong and Shou, Mike Zheng},
  journal = {arXiv preprint arXiv:2510.01174},
  year    = {2025},
  note    = {ICML 2026}
}

@article{zhu2025paper2video,
  title   = {Paper2Video: Automatic Video Generation from Scientific Papers},
  author  = {Zhu, Zeyu and Lin, Kevin Qinghong and Shou, Mike Zheng},
  journal = {arXiv preprint arXiv:2510.05096},
  year    = {2025}
}

@article{zheng2025pptagent,
  title   = {PPTAgent: Generating and Evaluating Presentations Beyond Text-to-Slides},
  author  = {Zheng, Hao and Guan, Xinyan and Kong, Hao and Zheng, Jia and Zhou, Weixiang and Lin, Hongyu and Lu, Yaojie and He, Ben and Han, Xianpei and Sun, Le},
  journal = {arXiv preprint arXiv:2501.03936},
  year    = {2025},
  note    = {EMNLP 2025}
}

@article{autopresent2025,
  title   = {AutoPresent: Designing Structured Visuals from Scratch},
  journal = {arXiv preprint arXiv:2501.00912},
  year    = {2025},
  note    = {CVPR 2025; SlidesBench benchmark introduced in this paper}
}

@article{aggarwal2025pass,
  title   = {{PASS}: Presentation Automation for Slide Generation and Speech},
  author  = {Aggarwal, Tushar and Bhand, Aarohi},
  journal = {arXiv preprint arXiv:2501.06497},
  year    = {2025}
}

@article{holmberg2025lectures,
  title   = {Generating Narrated Lecture Videos from Slides with Synchronized Highlights},
  author  = {Holmberg, Alexander},
  journal = {arXiv preprint arXiv:2505.02966},
  year    = {2025}
}

@article{islam2025alive,
  title   = {{ALIVE}: An Avatar-Lecture Interactive Video Engine with Content-Aware Retrieval for Real-Time Interaction},
  author  = {Islam, Md Zabirul and Manik, Md Motaleb Hossen and Wang, Ge},
  journal = {arXiv preprint arXiv:2512.20858},
  year    = {2025}
}

@inproceedings{huang2024vbench,
  title     = {{VBench}: Comprehensive Benchmark Suite for Video Generative Models},
  author    = {Huang, Ziqi and He, Yinan and Yu, Jiashuo and Zhang, Fan and others},
  booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
  year      = {2024},
  note      = {arXiv:2311.17982}
}

@article{huang2024vbenchpp,
  title   = {{VBench++}: Comprehensive and Versatile Benchmark Suite for Video Generative Models},
  author  = {Huang, Ziqi and others},
  journal = {arXiv preprint arXiv:2411.13503},
  year    = {2024}
}

@inproceedings{liu2024evalcrafter,
  title     = {{EvalCrafter}: Benchmarking and Evaluating Large Video Generation Models},
  author    = {Liu, Yaofang and Cun, Xiaodong and Liu, Xuebo and Wang, Xintao and Zhang, Yong and Chen, Haoxin and Liu, Yang and Zeng, Tieyong and Chan, Raymond and Shan, Ying},
  booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
  year      = {2024},
  note      = {arXiv:2310.11440}
}

@article{liu2024aigve,
  title   = {A Survey of {AI}-Generated Video Evaluation},
  author  = {Liu, Xiao and Xiang, Xinhao and Li, Zizhong and Wang, Yongheng and Li, Zhuoheng and Liu, Zhuosheng and Zhang, Weidi and Ye, Weiqi and Zhang, Jiawei},
  journal = {arXiv preprint arXiv:2410.19884},
  year    = {2024}
}

@article{stavrinou2025reeldeal,
  title   = {The Reel Deal: Designing and Evaluating {LLM}-Generated Short-Form Educational Videos},
  author  = {Stavrinou, Lazaros and Constantinides, Argyris and Belk, Marios and Vassiliou, Vasos and Liarokapis, Fotis and Constantinides, Marios},
  journal = {arXiv preprint arXiv:2509.05962},
  year    = {2025}
}

@article{leinonen2026aislides,
  title   = {{AI}-Generated Slides: Are They Good? Can Students Tell?},
  author  = {Leinonen, Juho and Zhang, Lisa and Hellas, Arto},
  journal = {arXiv preprint arXiv:2605.13532},
  year    = {2026}
}

@article{hallucination2026review,
  title   = {Hallucination to Truth: A Review of Fact-Checking and Factuality Evaluation in Large Language Models},
  journal = {arXiv preprint arXiv:2508.03860},
  year    = {2026},
  note    = {Also published in Artificial Intelligence Review (Springer)}
}
```

---

## Round 2 — SLR Expansion (2026-08-13)

Round 1 (above) was a narrative survey. Per user request, Round 2 adds: (a) formal SLR machinery (RQs, search strategy, inclusion/exclusion criteria, PRISMA-style selection counts — now implemented directly in the manuscript's Methodology section, not duplicated here), (b) an animation-specific literature thread the Round 1 search under-covered, and (c) a wider search for human-subject learning-outcome studies. This section documents the *content* additions; the formal SLR apparatus lives in `Papers/prompt-to-render-educational-video-generation.tex` §Methodology.

### New Key Papers (animation-specific thread)

### Silva, Lotfi, Ihianle, Shahtahmassebi & Bird (2026) — Training and Agentic Inference Strategies for LLM-based Manim Animation Generation
- **Main contribution:** ManimTrainer (SFT + GRPO reinforcement learning) and ManimAgent (renderer-in-the-loop inference strategies) for generating Manim animation code.
- **Method:** Evaluates 17 open-source sub-30B LLMs across nine training/inference combinations on a new benchmark, ManimBench.
- **Key finding:** Qwen 3 Coder 30B reaches 94% Render Success Rate and 85.7% Visual Similarity, +3 percentage points over a GPT-4.1 baseline.
- **Relevance:** The first systematic training-strategy comparison for LLM-based Manim generation — complements Code2Video's Planner-Coder-Critic architecture with an orthogonal question (how do you *train* the coder, not just orchestrate it).

### Li, He, Li, Chen, Xia, Su, Zhang & Ye (2026) — See Before You Code: Learning Visual Priors for Spatially Aware Educational Animation Generation
- **Main contribution:** OmniManim, a render-feedback-aware framework with a Vision Agent that predicts sparse keyframe layouts before code generation, addressing the layout/overlap defects that only surface after rendering.
- **Method:** Introduces two datasets, ManimLayout-1K and EduRequire-500 (the latter used as the evaluation benchmark).
- **Key finding:** Outperforms single-model and multi-agent baselines on layout-related metrics.
- **Relevance:** Directly targets a failure mode (spatial/layout defects) none of the Round 1 architecture papers evaluate explicitly.

### Liao, Ma, Lin, Zeng, Zheng & Ji (2026) — ALGOGEN: Tool-Generated Verifiable Traces for Reliable Algorithm Visualization
- **Main contribution:** Decouples algorithm execution from rendering via a "Visualization Trace Algebra" (VTA) and a "Rendering Style Language" (RSL), rather than having an LLM generate animation code end-to-end.
- **Method:** Python trackers produce verifiable VTA-JSON traces; a deterministic renderer compiles them.
- **Key finding:** 99.8% vs. 82.5% success rate against end-to-end baselines; 17.3% average improvement on a 200-task LeetCode algorithm-visualization benchmark.
- **Relevance:** The clearest algorithm-visualization-specific instance of this survey's central architectural claim (decomposition beats end-to-end generation) — here decomposing all the way down to a verifiable intermediate trace format, one level more granular than Code2Video's "generate correct code" approach.

### Samarth, Jain, Golugula & Sathvik (2025) — Manimator: Transforming Research Papers into Visual Explanations
- **Main contribution:** An open-source two-stage LLM pipeline (paper/prompt → structured scene description → Manim Python code) for turning research papers into animated explanations.
- **Relevance:** A simpler, earlier (July 2025) instance of the "paper-to-animation" pattern that Code2Video and ManimAgent (below) later extend with critics and memory.

### Joshi, Ke, Gajjar, Christian, Wang & Chen (2026) — LLM2Manim: Pedagogy-Aware AI Generation of STEM Animations
- **Main contribution:** A human-in-the-loop pipeline embedding multimedia-learning principles (segmentation, signaling, dual coding) directly into constrained prompt templates for Manim generation.
- **Method:** Within-subject A-B study, 100 undergraduate students.
- **Key finding:** Animation-based instruction produced modestly higher post-test scores (83% vs. 78%, p < .001, authors characterize this as a "slight" improvement), with a larger engagement effect (d = 0.94) and a moderate learning-gains effect (d = 0.67) and cognitive-load reduction (d = 0.41).
- **Relevance:** **The third genuine controlled human-learning-outcome study found across the full corpus** (after Stavrinou et al. and Leinonen et al. in Round 1) — and the first one specific to generated *animation* rather than video or slides. This directly updates this survey's central finding (see Round 2 gap re-analysis below).

### Jiang, Cai, Shao, Wang, Han, Song, Chen, An, Yang & Yang (2026) — ManimAgent: Self-Evolving Multimodal Agents for Visual Education
- **Main contribution:** A self-evolving agent (project name Paper2Manim) that carries reflection experience across tasks via a dual-channel Episodic Memory Bank (positive: success rationales; negative: validated failure patterns), built entirely from its own task stream with no weight updates.
- **Key finding:** Blind human Pass@1 rises and reflection rounds fall as memory size grows, versus no-memory and shuffled-memory controls.
- **Relevance:** **Name collision warning:** this is a *different* system from Silva et al.'s "ManimAgent" (both 2026, both Manim-focused, unrelated). Disambiguated in the manuscript by author + arXiv ID.

### Prasad & Mahapatra (2026) — Speech-Synchronized Whiteboard Generation via VLM-Driven Structured Drawing Representations
- **Main contribution:** The first dataset (24 paired Excalidraw demonstrations with narrated audio, millisecond-precision stroke timestamps, 8 STEM domains) for whiteboard-style educational video generation, plus a fine-tuned Qwen2-VL-7B (LoRA) that predicts stroke sequences synchronized to speech.
- **Relevance:** A structurally distinct decomposition strategy — the "intermediate representation" here is a stroke-sequence/drawing representation, not code or a script, extending this survey's architecture taxonomy to a new modality (whiteboard/freehand illustration).

### Ku, Chong, Leung, Shah, Yu & Chen (2025) — TheoremExplainAgent: Towards Video-based Multimodal Explanations for LLM Theorem Understanding
- **Main contribution:** An agent-based system generating 5+ minute Manim videos explaining mathematical theorems; introduces TheoremExplainBench (240 theorems, 5 automated evaluation metrics).
- **Key finding:** An o3-mini-based agent reaches 93.8% success rate and an overall score of 0.77; the authors also show multimodal (video) explanations expose LLM reasoning failures that text-only evaluation misses.
- **Relevance:** One of the earliest (Feb 2025) and largest-benchmark instances of the Manim-code-intermediate pattern; also a rare case where the generated artifact is used to *probe the generating model itself*, not just to teach a human.

### Jo, Zhao, Liu & Suzuki (2025) — Generative Lecture: Making Lecture Videos Interactive with LLMs and AI Clone Instructors
- **Main contribution:** Converts existing lecture videos into interactive experiences via an AI-cloned instructor (HeyGen avatar + ElevenLabs voice + GPT-5), supporting on-demand clarification, adaptive quizzes, personalized explanation, and six other features.
- **Method:** Design elicitation study (N=8), user evaluation study (N=12), expert feedback (N=5).
- **Relevance:** A genuine (if small-N) human-evaluation study, extending Round 1's "avatar/narration synthesis" architecture family (ALIVE) toward post-hoc interactivity rather than generation from scratch.

### Pellas (2025) — The Impact of AI-Generated Instructional Videos on Problem-Based Learning in Science Teacher Education
- **Main contribution:** A controlled comparison of two AI-generated instructional video formats (with vs. without an embedded preview feature) on self-efficacy, task performance, and knowledge retention/transfer.
- **Method:** 55 Greek pre-service science teachers (mean age 27.3, range 22–35).
- **Key finding:** Both video formats effectively supported self-efficacy, task performance, and retention; no significant difference between preview conditions.
- **Relevance:** **The fourth genuine controlled human-learning-outcome study** in the full corpus, and — unlike LLM2Manim, Stavrinou et al., and Leinonen et al. — evaluates AI-generated instructional *video* (not animation or slides) with a real classroom-adjacent population (pre-service teachers), published in a peer-reviewed journal (*Education Sciences*) rather than as an arXiv preprint.
- **Citation:** Pellas, N. (2025). *Education Sciences*, 15(1), 102. https://doi.org/10.3390/educsci15010102

### Related-Work secondary studies (NOT part of the primary corpus — discussed for positioning, per Related Work protocol)

### Zhang & Shukor (2025) — Role of AI-Generated Instructional Videos: A Systematic Literature Review
- PRISMA-based SLR: 3,271 initial records across six databases → 21 included. Scope: educational theories and the role of AI-generated instructional video in higher education.
- **Why it doesn't substitute for this SLR:** covers pedagogical role/theory, not generation *architectures* or *benchmarks* — the two pillars this survey's title promises.
- **Citation:** Zhang, J. & Shukor, N.A. (2025). *International Journal of Academic Research in Progressive Education and Development*, 14(4), 31–42.

### Shu, Kou, Zhang, Zhang, Zhang, Xu & Zhou (2025) — AI-Generated Instructional Videos: A Systematic Review of Learning Impacts, Applications, and Research Perspectives
- SLR: 143 initial records across four databases (Web of Science, ERIC, IEEE Xplore, Google Scholar) → 12 included.
- **Key finding (corrected — see Round 2 Post-Flight discrepancy below):** AI-generated instructional video quality is "sufficient for educational use" but the authors conclude it "cannot yet replace traditionally produced videos," citing limitations in learning motivation and social presence.
- **Why it doesn't substitute for this SLR:** learning-impact/applications focused; does not review generation architectures, code/script/trace intermediates, or technical benchmarks (VBench-style or education-specific).
- **Citation:** Shu, J., Kou, H., Zhang, J., Zhang, T., Zhang, H., Xu, T., & Zhou, Y. (2025). Proceedings of CSTE 2025 (7th Intl. Conf. on Computer Science and Technologies in Education), pp. 877–881. https://doi.org/10.1109/CSTE64638.2025.11091997

### Methodology references (cited in the manuscript's Methodology section only — not part of the surveyed-systems corpus)

- Page, M.J. et al. (2021). "The PRISMA 2020 statement: an updated guideline for reporting systematic reviews." *BMJ*, 372, n71.
- Kitchenham, B. & Charters, S. (2007). "Guidelines for performing Systematic Literature Reviews in Software Engineering." EBSE 2007-001, Keele University and Durham University Joint Report.

### Screened-and-excluded examples (illustrative, not exhaustive — full PRISMA counts are in the manuscript)

| Record | Reason excluded |
|---|---|
| ViMax (arXiv:2606.07649) | General-purpose long-form video generation; no education-specific framing (retained only as brief narrative context, like Sora/CogVideoX, not counted in the included corpus) |
| ViviDoc (arXiv:2603.27991) | Generates interactive documents, not video/animation; not education-specific |
| Data Playwright (arXiv:2410.03093) | LLM-powered, but generates data-journalism videos, not educational content |
| "AI instructional agent…RCT" (arXiv:2505.22526) | Real-time live-taught agent; produces no pre-rendered video/animation/slide artifact |
| "Faster Completion, Less Learning" (arXiv:2605.21629) | About general genAI use on math problems (ALEKS); no video/animation generation system involved |
| VideoWeaver, Co-Director, Crayotter, OmniShow, CausalCine | General-purpose video generation/editing systems, no education-specific framing |
| AnimatedLLM (arXiv:2601.04213), VISTA (arXiv:2411.05423) | Adjacent LLM+visualization work, but not educational-content animation generation (LLM-internals visualization; math problem generation, respectively) |

### Round 2 gap re-analysis

With the animation-specific thread and wider human-subject search added, the corpus grows to **25 included systems/benchmarks/studies** (15 Round 1 + 10 Round 2). The central finding is **updated, not overturned**: the count of papers reporting a genuine controlled human-learning-outcome study rises from **2 of 19** (Round 1) to **4 of 25** (Round 1 + 2) — Stavrinou et al. (ReelsEd), Leinonen et al. (AI slides), LLM2Manim (animation), and Pellas (instructional video). Two of the four new-thread additions (LLM2Manim, Generative Lecture) do include human evaluation, suggesting the newer (2026) wave of animation/interactivity-focused systems is somewhat more likely to report human data than the 2025 wave of end-to-end video pipelines — but at 4/25 (16%), the field's evaluation practice still overwhelmingly measures the generated artifact, not the learner.

---

## Post-Flight Verification

**Claims extracted:** 15 (one per cited paper: title, authors, and the specific factual assertion attributed to it)
**Verified independently:** 15 (forked `claim-verifier` agent — fresh context, never saw this draft, fetched each arXiv abstract page directly, plus CVF Open Access pages for two venue attributions)
**Outcome:** **PASS** — 0 contradictions, 0 unverifiable claims, no fabricated citations (including the three most recent IDs, 2512.20858 / 2602.11790 / 2605.13532, which a stale reference set might otherwise have flagged as nonexistent).

### Verified

| ID | Claim | Evidence |
|----|-------|----------|
| C1 | LASEV (Yan et al., arXiv:2602.11790): title, 6 authors, agent structure, "structured executable video script" | arXiv abstract, verbatim match |
| C2 | Code2Video (arXiv:2510.01174): Planner/Coder/Critic, MMMC, TeachQuiz, "40% improvement" | arXiv abstract, verbatim match |
| C3 | Paper2Video (arXiv:2510.05096): 101-paper benchmark, PaperTalker, 4 named metrics | arXiv abstract, verbatim match |
| C4 | PPTAgent (arXiv:2501.03936): authors, PPTEval's 3 dimensions | arXiv abstract |
| C5 | AutoPresent/SlidesBench (arXiv:2501.00912): 7k/585 examples, 310 decks, 10 domains, 8B Llama | arXiv abstract, verbatim match |
| C6 | PASS (arXiv:2501.06497): title, 2 authors | arXiv abstract |
| C7 | Holmberg (arXiv:2505.02966): F1 > 92%, 1,000-sample dataset, sole author | arXiv abstract, verbatim match |
| C8 | ALIVE (arXiv:2512.20858): title, 3 authors | arXiv abstract |
| C9 | VBench (arXiv:2311.17982): lead author, 16 dimensions, CVPR 2024 | arXiv abstract + CVF Open Access proceedings |
| C10 | VBench++ (arXiv:2411.13503): extension of VBench | arXiv listing |
| C11 | EvalCrafter (arXiv:2310.11440): 10-author order, 17 metrics, CVPR 2024 | arXiv abstract + CVF Open Access / DOI |
| C12 | AIGVE survey (arXiv:2410.19884): title, author order | arXiv abstract |
| C13 | ReelsEd / "The Reel Deal" (arXiv:2509.05962): 6 authors, 62 students, verbatim finding | arXiv abstract, verbatim match |
| C14 | "AI-Generated Slides" (arXiv:2605.13532): 3 authors, 5 tools, verbatim finding | arXiv abstract, verbatim match |
| C15 | "Hallucination to Truth" (arXiv:2508.03860): title, survey scope | arXiv abstract |

### Unverifiable (user review recommended)

None.

### Discrepancies (regenerated)

- **C1** — original draft characterized LASEV as a three-agent system (Solution/Illustration/Narration); the source describes a fourth, supervising Orchestrating Agent. Corrected above.

### Verifier's non-blocking notes (not corrections, worth knowing)

- Code2Video's "executable Manim code" detail is confirmed but comes from the paper's method section, not its abstract — cite accordingly if you pull this into a formal manuscript.
- VBench's and EvalCrafter's CVPR 2024 venue is correct but not stated in either paper's arXiv "comments" field — cite the CVF proceedings version, not the bare arXiv ID, if venue precision matters for a submission.
- PASS's evaluation dimensions (relevance/coherence/redundancy) are distinct from PPTAgent's PPTEval dimensions (Content/Design/Coherence) — easy to conflate; kept distinct in this draft.

---

## Round 2 Post-Flight Verification (Batch 1 — new primary-corpus claims)

**Claims extracted:** 13
**Verified independently:** 13 (forked `claim-verifier` agent, fresh context)
**Outcome:** **PASS** — 0 HIGH-WARN, 0 MED-WARN, 0 discrepancies. All 11 author lists (5, 8, 6, 4, 6, 10, 2, 6, 6, 4, 5 authors respectively) matched exactly.

### Verified

| ID | Claim | Evidence |
|----|-------|----------|
| N1 | Silva et al. (arXiv:2604.18364): 5 authors, ManimTrainer/ManimAgent, ManimBench, Qwen 3 Coder 30B 94% RSR / 85.7% VS, +3pp over GPT-4.1 | arXiv abstract, verbatim |
| N2 | Li et al. (arXiv:2605.15585): 8 authors, OmniManim, Vision Agent, ManimLayout-1K + EduRequire-500 | arXiv abstract, verbatim |
| N3 | Liao et al. (arXiv:2605.12159): 6 authors, VTA+RSL, 200-task LeetCode, 17.3% improvement, 99.8% vs 82.5% | arXiv abstract, verbatim |
| N4 | Samarth et al. (arXiv:2507.14306): 4 authors, two-stage LLM pipeline | arXiv abstract |
| N5 | Joshi et al. (arXiv:2604.05266): 6 authors, 100 UG students, 83% vs 78% p<.001, d=0.67/0.94/0.41 | arXiv abstract, verbatim |
| N6 | Jiang et al. (arXiv:2606.30296): 10 authors, dual-channel Episodic Memory Bank, Paper2Manim (confirmed via arXiv comments/code field, not abstract) | arXiv abstract + comments field |
| N7 | Prasad & Mahapatra (arXiv:2603.25870): 2 authors, 24 Excalidraw demos, 8 STEM domains, Qwen2-VL-7B+LoRA | arXiv abstract, verbatim |
| N8 | Ku et al. (arXiv:2502.19400): 6 authors, TheoremExplainBench 240 theorems, o3-mini 93.8%/0.77 | arXiv abstract, verbatim |
| N9 | Huang et al. (arXiv:2606.07649, ViMax): 6 authors, general-purpose, no education framing | arXiv abstract |
| N10 | Jo et al. (arXiv:2512.21796): 4 authors, N=8/12/5 studies, HeyGen+ElevenLabs+GPT-5 | arXiv abstract |
| N11 | Qin et al. (arXiv:2505.22526): 5 authors, real-time live agent (not a generated artifact) — confirms exclusion rationale | arXiv abstract |
| N12 | Page et al., PRISMA 2020, BMJ 2021;372:n71 | PMC8005924 + PLOS Med + PMC8008539, cross-confirmed |
| N13 | Kitchenham & Charters (2007), EBSE 2007-001 | Retrieved report cover page |

### Advisory notes (non-blocking, applied in the manuscript)

- N1: "percentage points," not "points" (VS is itself a %); the 17-model set is specifically sub-30B.
- N2: ManimLayout-1K and EduRequire-500 are both "datasets"; only EduRequire-500 is the evaluation benchmark.
- N5: authors themselves call the 83%-vs-78% gap a "slight" improvement — manuscript should not overstate it.
- N1/N6: genuine name collision — two unrelated 2026 papers both name a system "ManimAgent." Disambiguated in the manuscript by author name + arXiv ID at first use.
- N13: report-number variant exists ("EBSE-2007-01" vs "EBSE 2007-001"); used the more common form consistently.

---

## Round 2 Post-Flight Verification (Batch 2 — Related Work secondary studies)

**Claims extracted:** 5
**Verified independently:** 5 (forked `claim-verifier` agent, fresh context)
**Outcome:** **FAIL → regenerated.** 1 HIGH-WARN caught and corrected before use; 1 MED-WARN qualified; 3 PASS.

### Discrepancy (HIGH-WARN, corrected)

- **M3** — Draft claim (from an uncorroborated web-search summary) attributed "134 publications from EBSCO, EI Compendex, Scopus, and Web of Science" to Shu et al. (2025, CSTE). The verifier traced this to a **different paper** — Chen, X., Hu, Z., & Wang, C. (2024), "Empowering education development through AIGC: A systematic literature review," *Educational and Information Technologies*, 29(13), 17485–17537 (DOI 10.1007/s10639-024-12549-7). Shu et al.'s actual numbers, confirmed via OpenAlex/Crossref/Semantic Scholar: **143 initial records** across **Web of Science, ERIC, IEEE Xplore, and Google Scholar**, **12 included** in the final analysis. **Corrected in the manuscript and in this document** (see "Related-Work secondary studies" above) — the erroneous 134/EBSCO/EI-Compendex figures do not appear anywhere in the final output.

### Qualified (MED-WARN)

- **M3 finding statement** — original draft phrasing ("no significant performance difference between human and AI-generated instructors") drops a caveat present in the abstract ("cannot yet replace traditionally produced videos... limitations in learning motivation and social presence"). Manuscript uses the fuller, caveated phrasing.

### Verified

| ID | Claim | Evidence |
|----|-------|----------|
| M1 | Pellas (2025), *Educ. Sci.* 15(1):102, DOI 10.3390/educsci15010102; 55 Greek pre-service teachers, mean age 27.3 | Crossref + OpenAlex + Semantic Scholar abstract, verbatim |
| M2 | Zhang & Shukor (2025), IJARPED 14(4):31–42; 3,271 records / 6 databases → 21 included | Publisher article page, verbatim |
| M4 | ViviDoc (arXiv:2603.27991): interactive documents, not video; 101-topic/11-domain benchmark (corrected framing — 11 domains describe topic provenance, not 11 separate evaluations) | arXiv abstract |
| M5 | Data Playwright (arXiv:2410.03093): LLM-powered, data-journalism focus, not education-specific; year corrected to 2024 (OpenAlex), accepted at IEEE TVCG | arXiv abstract + OpenAlex |
