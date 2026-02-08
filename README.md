# AI-DAC Project

This repository contains diagram generation tools for creating HiveMQ architecture diagrams using the diagrams Python library.

## Project Structure

### Main Components

- **hivemq_theme.py**: Core palette management class that handles icon configuration, node creation, and documentation generation
- **main.py**: Simple entry point that initializes the HiveMQ palette
- **themed_main.py**: Example showing how to create a diagram with custom HiveMQ icons and styling
- **one-click-main.py**: Template for creating diagrams with automated documentation generation

### Icon Management

- **icons.yaml**: Configuration file defining available symbols and their icon paths
- **icons/** directory: Storage for actual icon images
- **icons.csv**: Alternative configuration format (auto-generated)

## Documentation

- **docs/ARCHITECTURE.md**: Detailed documentation of the project architecture and modules
- **tests/**: Unit tests for the HiveMQPalette class
- **example_runner.py**: Example demonstrating how to use the HiveMQPalette class

## Usage

The core functionality is accessed through the HiveMQPalette class:

1. Initialize with `HiveMQPalette('icons.yaml')`
2. Create diagram nodes with `palette.get_node('symbol', 'label')`
3. Generate documentation with `palette.generate_readme('diagram_name', 'output.svg')`
4. Use Git integration or S3 upload capabilities as needed