# C2CAD-Bench

C2CAD-Bench is a benchmark for evaluating 3D spatial reasoning in large language models for CAD-style geometry generation. Models receive natural-language engineering specifications and return JSON arrays of geometric primitives. The scorer compares the output against deterministic parametric golden references using coverage, geometry, and semantic scores.

This repository contains the code and data artifact for the paper submission. The evaluated benchmark version contains 25 test families, 3 difficulty levels per family, 75 total test cases, and results for 13 LLMs.

## What Is Included

- Prompt definitions and deterministic golden-reference generators.
- The unified benchmark runner and scoring pipeline.
- Semantic validators for family-specific constraints.
- A WebGL viewer and static result database for inspecting outputs.
- Raw model outputs and per-case scores in `results/showcase_db.js`.
- Documentation for scoring and zero-scaffolding prompt design.

## Benchmark Summary

| Phase | Families | Main challenge |
| --- | ---: | --- |
| P1: Geometric Forms | 6 | Trigonometry, repetition, bolt-circle patterns |
| P2: Complex Structures | 6 | Hidden formula derivation, lattice connectivity, pitch-circle constraints |
| P3: Engineering Constraints | 6 | Concentricity, clearance, gravity mates, mechanism layout |
| P4: Bio-Inspired Assemblies | 7 | Biological morphology, large-scale patterns, geodesic frames |

The JSON schema uses seven primitive types:

```text
box, cylinder, sphere, cone, torus, pipe, beam
```

All dimensions are in millimetres. The expected primitive count ranges from 5 to 805 shapes.

## Fresh Environment Setup

Use Python 3.10 or newer.

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Dry Checks

These commands do not call any model API:

```bash
python runners\run_unified.py --list-models
python -m compileall -q probe runners stages
python runners\check_artifact.py
```

Expected output:

```text
75 golden test cases
13 models
975 model-case results
```

## Running Live Evaluations

Live evaluation requires provider API keys. Copy the example environment file and fill only the providers you intend to use:

```bash
cp .env.example .env
```

Required variables by provider:

| Provider | Environment variable |
| --- | --- |
| Google Gemini | `GOOGLE_API_KEY` or `GEMINI_API_KEY` |
| OpenAI | `OPENAI_API_KEY` |
| Anthropic | `ANTHROPIC_API_KEY` |
| DeepSeek | `DEEPSEEK_API_KEY` |
| Moonshot/Kimi | `MOONSHOT_API_KEY` |

Run a single model:

```bash
python runners\run_unified.py --all --model gemini-2.5-pro
```

Run a single phase:

```bash
python runners\run_unified.py --phase 1 --model gpt-4.1
```

Re-run failed or zero-score cases:

```bash
python runners\run_unified.py --all --model claude-sonnet-4-6 --redo
```

## Viewing Results

Open the static dashboard and visualizer in a browser:

```bash
ui\results.html
ui\visualizer.html
```

On macOS/Linux:

```bash
open ui/results.html
open ui/visualizer.html
```

## Repository Structure

```text
C2CAD-Bench/
  probe/                    Core package and schema helpers
  runners/                  Benchmark runner, scoring utilities, database builders
  stages/                   Golden-reference generators by phase
  results/                  Result database and analysis figures
  ui/                       Static dashboard and 3D visualizer
  SCORING_RULES.md          Scoring methodology
  prompt_design_rules.md    Zero-scaffolding prompt design rules
  requirements.txt          Python dependencies
  .env.example              API-key template
  LICENSE                   Release license
```

## License

The code and data are released under the MIT License. For an anonymous review artifact, restore author-identifying copyright metadata only after the review period or for the camera-ready public release.
