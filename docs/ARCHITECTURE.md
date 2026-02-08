# AI-DAC Project Architecture

## Overview

This document describes the architecture and modules of the AI-DAC project, a diagram generation tool for creating HiveMQ architecture diagrams.

## Project Structure

```
ai-dac/
├── src/
│   └── hivemq_theme.py      # Core palette management
├── examples/
│   ├── themed_main.py       # Main example with custom HiveMQ icons
│   └── one-click-main.py    # Template for automated diagram generation
├── icons/
│   └── (icon files)
├── docs/
│   ├── ARCHITECTURE.md      # This file
│   └── USAGE.md             # Usage instructions
├── README.md
├── requirements.txt
└── pyproject.toml
```

## Core Modules

### src/hivemq_theme.py

The `HiveMQPalette` class is the central component of this project:

- **Class**: `HiveMQPalette`
- **Purpose**: Manages icon configuration, node creation, and documentation generation
- **Key Features**:
  - Automatic configuration file creation (YAML, JSON, or CSV)
  - Custom icon node creation using the diagrams library
  - Bill of materials generation for diagrams
  - Git integration for committing changes
  - S3 upload functionality for documentation hosting

### Key Methods

- `__init__(self, config_path="icons.yaml")`: Initializes palette with configuration file
- `_bootstrap()`: Creates icons directory and default config if missing
- `load_icons()`: Loads icon configuration from file
- `get_node(self, symbol, label)`: Creates a diagram node with custom icon
- `generate_readme(self, diagram_name, image_file)`: Generates README with bill of materials
- `push_to_github(self, repo_path, commit_msg)`: Commits and pushes changes to Git
- `upload_to_s3(self, file_list, bucket_name, region)`: Uploads files to S3

## Examples Directory

### examples/themed_main.py

Demonstrates the core functionality:
- Initialize HiveMQPalette with CSV configuration
- Create diagram with custom HiveMQ icons
- Use clustering for logical grouping
- Shows proper usage of `get_node()` method

### examples/one-click-main.py

Template for automated workflow:
- Initialize palette with YAML configuration
- Create diagram with automatic documentation generation
- Shows usage of Git and S3 integration capabilities

## Configuration Files

### icons.yaml

Defines available symbols and their icon paths:
```yaml
- symbol: edge
  path: ./icons/edge.png
  notes: HiveMQ Edge Gateway
- symbol: broker
  path: ./icons/broker.png
  notes: Enterprise Broker
```

### icons/ Directory

Contains actual icon image files referenced in configuration.

## Dependencies

### Required Libraries
- `diagrams`: Core diagram generation library
- `pyyaml`: YAML configuration support
- `gitpython`: Git integration
- `boto3`: AWS S3 integration

## Architecture Patterns

1. **Configuration-Driven**: All icon mapping is handled through external configuration files
2. **Extensible**: Easy to add new symbols and icon types
3. **Automated Documentation**: Automatic README generation from diagram components
4. **Cloud Integration**: Supports publishing diagrams to S3 for documentation hosting
5. **Git Integration**: Supports version control of diagram changes