# 🏗️ C2CAD-Bench

**A Large-Scale Benchmark for 3D Spatial Reasoning and CAD Geometry Generation.**

![Overall Rankings](results/fig1_overall_rankings.png)

C2CAD-Bench evaluates the ability of Large Language Models (LLMs) to reason about 3D space and generate valid CAD-style geometry. Unlike simplified benchmarks, C2CAD-Bench requires models to translate complex natural-language engineering specifications into deterministic parametric primitives.

---

## 🌟 Key Highlights

- **75 Test Cases**: Spanning 25 test families across 3 difficulty levels.
- **13 LLMs Evaluated**: Benchmark results for major frontier models (Gemini, GPT, Claude, DeepSeek).
- **Multimodal Scoring**: Automated evaluation using **Coverage (20%)**, **Geometry (30%)**, and **Semantic (50%)** scores.
- **Parametric Golden References**: Every case is compared against deterministic ground truth.

---

## 📈 Metric Decomposition

Our scoring methodology accounts for shape count (Coverage), dimensional accuracy (Geometry), and functional/structural validity (Semantic). The chart below shows the decomposition across frontier models.

![Score Components](results/fig2_score_components.png)

---

## 🖼️ Showcase Gallery: Model Performance

The following table showcases how different LLMs handle various structural and engineering challenges. Notice the varying degrees of "hallucination" and spatial detachment.

| Challenge | Comparison & Results |
| :--- | :--- |
| **Spiral Staircase**<br>(Phase 1: Geometric Forms)<br><br>Tests trigonometry, repetition, and bolt-circle patterns. | ![Spiral Staircase Comparison](results/fig17_spiral_staircase_comparison.png) |
| **Radiolarian Skeleton**<br>(Phase 4: Bio-Inspired)<br><br>Tests biological morphology, geodesic frames, and large-scale recursive patterns. | ![Radiolarian Comparison](results/fig21_radiolarian_skeleton_comparison.png) |
| **Pipe Manifold**<br>(Phase 3: Engineering)<br><br>Tests concentricity, clearance, and mechanism layout under gravity mates. | *The Pipe Manifold challenge requires models to align multiple ports and support structures with strict dimensional constraints.*<br>[View results for Pipe Manifold in Heatmap ↓](#-full-model-family-score-matrix) |
| **Voxel Grid & DNA Helix**<br>(Phases 1 & 2)<br><br>Tests volumetric filling and parametric double-helix path generation. | *Frontier models like Gemini 3.1 Pro and GPT-5.4 consistently achieve 100% coverage on these complex parametric tasks.*<br>[View Detailed Matrix ↓](#-full-model-family-score-matrix) |

---

## 📊 Full Model-Family Score Matrix

The heatmap below shows the global score for every model across all 25 test families. This provides a granular view of where models excel (e.g., standard geometric forms) and where they struggle (e.g., complex engineering assemblies like the Pipe Manifold).

![Family Heatmap](results/fig3_family_heatmap.png)

---

## 📈 Robustness & Scaling Analysis

### Performance vs. Difficulty
As difficulty increases from Level 1 to Level 3, we observe a characteristic "performance cliff" even for frontier models. This analysis breaks down how coverage, geometry, and semantic logic degrade under pressure.

![Difficulty Scaling](results/fig5_difficulty_scaling.png)

### Shape Hallucination Analysis
We track "hallucinations" (producing significantly more shapes than specified) and "under-production" (ignoring core structural components). This chart illustrates the production ratio accuracy across all tested models.

![Hallucination Analysis](results/fig13_hallucination_analysis.png)

---

## 🧠 Cognitive Capacity Profiles

We use radar charts to visualize the performance profiles across different reasoning dimensions. This highlights the "hallucination finger-print" of different model families.

![Cognitive Profiles](results/fig19_cognitive_capacity_profiles.png)

---

## 🛤️ Benchmark Phases

C2CAD-Bench is divided into four distinct phases of increasing complexity:

- **🟦 Phase 1: Geometric Forms**: Basic primitive grouping, bolt patterns, and simple rotations.
- **🟪 Phase 2: Complex Structures**: Lattice connectivity, formula derivation, and pitch-circle constraints.
- **🟧 Phase 3: Engineering Constraints**: Concentricity, clearance, and gravity-mated assemblies (e.g., **Pipe Manifold**).
- **🟩 Phase 4: Bio-Inspired Assemblies**: Biological morphology and geodesic frames.

---

## 🚀 Quick Start

### 📦 Setup

Requires Python 3.10+.

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

python -m pip install -r requirements.txt
```

### 🔍 Dry Checks

Verify your environment without calling APIs:

```bash
python runners\run_unified.py --list-models
python runners\check_artifact.py
```

### ⚡ Running Live Evaluations

Copy the example environment file and add your API keys:

```bash
cp .env.example .env
# Run a specific model
python runners\run_unified.py --all --model gemini-2.5-pro
```

---

## 📂 Repository Structure

```text
C2CAD-Bench/
├── probe/          # Core package and schema helpers
├── runners/        # Benchmark runner & scoring utilities
├── stages/         # Golden-reference generators by phase
├── results/        # Generated figures and result database
├── ui/             # WebGL visualizer and static dashboard
├── SCORING_RULES.md
└── requirements.txt
```

---

## ⚖️ License

Released under the **MIT License**. For anonymous review artifacts, please respect the metadata constraints specified in the paper.
