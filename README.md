# AI-DAC Project

This repository contains diagram generation tools for creating HiveMQ architecture diagrams using the diagrams Python library.

## Project Structure

### Main Components

- **hivemq_theme.py**: Core palette management class that handles icon configuration, node creation, and documentation generation
- **main.py**: Simple entry point that initializes the HiveMQ palette
- **themed_main.py**: Example showing how to create a diagram with custom HiveMQ icons and styling
- **one-click-main.py**: Template for creating diagrams with automated documentation generation
- **diagram-hivemq-high-availability.py**: Example of a high availability architecture diagram
- **diagrams-1.py through diagrams-3.py**: Various diagram examples
- **diagrams-hybrid-bridge.py**: Hybrid bridge architecture diagram
- **diagram-sparklplug.py**: Sparklplug integration diagram
- **diagram-architecture-slide.py**: Architecture slide diagram
- **diagram-svg-out.py**: SVG output diagram example

### Icon Management

- **icons.yaml**: Configuration file defining available symbols and their icon paths
- **icons/** directory: Storage for actual icon images
- **icons.csv**: Alternative configuration format (auto-generated)

## Cleanup Recommendations

1. **Remove Duplicate Files**: There are several versions of the theme files:
   - hivemq_theme.py
   - old_hivemq_theme.py
   - old2_hivemq_theme.py
   - old3_hivemq_theme.py
   - hivemq_theme-2.py
   - ehanced_hivemq_themed_main.py

2. **Consolidate Diagram Examples**: There's a lot of redundancy in diagram generation files. Consider:
   - Keeping only one main example file
   - Using a single generic diagram script with parameters
   - Moving examples to a separate examples/ directory

3. **Code Organization**:
   - Create a clear folder structure (src/, examples/, utils/)
   - Standardize naming conventions for diagram files
   - Document all functions and classes with docstrings
   - Move diagram examples to a dedicated examples/ directory

4. **Documentation**:
   - Create a proper documentation system
   - Add usage examples for the HiveMQPalette class
   - Document all configuration options
   - Include setup and installation instructions