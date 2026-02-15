# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AI-DAC (AI Diagrams as Code) — a Python tool for generating professional HiveMQ-branded architecture diagrams programmatically. Targeted at Technical Account Managers and engineers who need version-controlled, automatically generated architecture diagrams for IoT systems.

## Setup & Running

```bash
# Virtual environment setup
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Or with uv (lock file present)
uv sync

# System dependency: Graphviz must be installed (required by diagrams library)
# macOS: brew install graphviz

# Run the main demo
python demo.py                    # generates images/demo_architecture.png
./run_demo.sh                     # runs demo.py with venv checks

# Run tests
python -m unittest tests/test_hivemq_theme.py
python -m unittest test_bom.py test_docs_bom.py

# Docker
docker-compose build
docker-compose run diagram-gen python demo.py
```

## Architecture

### Core Module: `hivemq_theme.py`

The `HiveMQPalette` class is the central abstraction. It:
- Loads icon definitions from YAML, JSON, or CSV config files
- Creates `diagrams.custom.Custom` nodes via `get_node(symbol, label)`
- Tracks which symbols are used to auto-generate a Bill of Materials table
- Provides `generate_readme()` for markdown documentation with BOM
- Has Git (`push_to_github()`) and S3 (`upload_to_s3()`) integration methods
- Auto-bootstraps icons directory and default config if missing (`_bootstrap()`)

### HiveMQ Brand Constants (defined in `hivemq_theme.py`)

- `YELLOW = "#FFC000"`, `BLACK = "#000000"`, `TEAL = "#037DA5"`, `DARK_GREY = "#181818"`
- `GLOBAL_ATTR`: Graph-level styling (black background, yellow text, ortho splines)
- `BASE_NODE_ATTR`: Node styling (yellow fill, black text, box shape)

### Diagram Creation Pattern

Every diagram script follows this pattern:
1. `palette = HiveMQPalette("icons.csv")` — initialize with config
2. Create `Diagram(...)` context with `GLOBAL_ATTR` and `BASE_NODE_ATTR`
3. Use `palette.get_node(symbol, label)` for custom HiveMQ-branded nodes
4. Connect nodes with `Edge()` operators (use `>>` syntax)
5. Call `palette.generate_readme(name, image_file)` to produce documentation

### Icon Configuration

Icons are defined in `icons.csv` (root) or `icons/icons.yaml`. Each entry has `symbol`, `path`, and `notes` fields. The symbol is the key used in `get_node()` calls; notes appear in the generated BOM.

### Key Files

- `demo.py` — Primary example: Unified IIoT Architecture with Factory Floor and Cloud clusters
- `one-click-main.py` — Minimal template for quick single-node diagrams
- `example_runner.py` — Educational utility listing available examples
- `examples/` — Four examples showing different patterns (basic init, themed, mixed icons, multi-region DR)

### Output

Diagrams render to `images/` as PNG or SVG. The `generate_readme()` method writes a `README.md` with the diagram image and a Bill of Materials table.

## Notes

- Python 3.13+ required (see `.python-version` and `pyproject.toml`)
- The Dockerfile uses Python 3.11-slim (diverges from project requirement)
- `print_bom()` is referenced in `test_bom.py` but not implemented in `hivemq_theme.py`
- `docker-build-n-run.sh` and `old3_hivemq_theme.py` are empty placeholder files
