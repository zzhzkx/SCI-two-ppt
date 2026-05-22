# SCI-two-ppt

AI-powered scientific paper to presentation PPT generator.

## Features

- Multi-paper input with context-aware analysis
- Multi-round requirement gathering for presentation goals
- Critic agent for plan review and optimization
- Specialized sub-agents: paper retrieval, core principles, simulation, UI design, content strategy
- Academic-first layout with pre-reserved scholarly sections
- Per-slide iterative refinement with live preview
- Final PPTX generation via python-pptx

## Installation

```bash
pip install -r requirements.txt
cp config/settings.yaml config/settings.local.yaml
# Edit settings.local.yaml with your API keys
```

## Quick Start

```bash
python -m src.core.pipeline --papers paper1.pdf paper2.pdf
```

## Project Structure

```
src/
  agents/       # Sub-agent system (critic, retrieval, design, etc.)
  core/         # Pipeline orchestration, goal building, review loop
  pptx_gen/     # PPTX builder, academic templates, renderer
  utils/        # Helpers
templates/      # PPT template assets
docs/           # Workflow documentation
tests/          # Tests
```

## License

MIT
