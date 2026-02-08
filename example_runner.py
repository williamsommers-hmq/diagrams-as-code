#!/usr/bin/env python3
"""
Simple example runner for the AI-DAC project.
This shows how to use the HiveMQPalette class.
"""

import os
import sys

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("AI-DAC Example Runner")
print("=====================")
print("This demonstrates the functionality of the HiveMQPalette class.")
print("")

# Show what files exist in the project
print("Files in project:")
for file in os.listdir("."):
    if file.endswith(".py") and file != "example_runner.py":
        print(f"  - {file}")

print("")
print("Basic functionality demonstration:")
print("- HiveMQPalette class manages icon configuration")
print("- Supports YAML, JSON, and CSV configuration formats")
print("- Automatically creates icons directory and default config")
print("- Generates README files with bill of materials")
print("- Supports Git integration and S3 uploads")
print("")

print("To run actual diagram generation, you would:")
print("1. Initialize HiveMQPalette with config file")
print("2. Use get_node() method to create nodes with custom icons")
print("3. Build diagram with the diagrams library")
print("4. Generate documentation with generate_readme()")
print("")

print("Example usage (in a real environment):")
print("palette = HiveMQPalette('icons.yaml')")
print("node = palette.get_node('edge', 'HiveMQ Edge')")
print("palette.generate_readme('Diagram Name', 'output.svg')")
