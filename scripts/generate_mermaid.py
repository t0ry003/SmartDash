#!/usr/bin/env python3
"""
Generate Mermaid Class Diagram for Flask Application

This script parses Python files using the ast library to identify classes and functions,
then generates a Mermaid classDiagram representation.
"""

import ast
import os
from pathlib import Path


class MermaidDiagramGenerator:
    """Generator for Mermaid class diagrams from Python source code."""
    
    def __init__(self):
        self.classes = []
        self.functions = {}  # Organized by file
        
    def parse_file(self, filepath, module_name):
        """Parse a Python file and extract classes and functions."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                source = f.read()
            
            tree = ast.parse(source)
            self._extract_definitions(tree, module_name)
        except Exception as e:
            print(f"Warning: Could not parse {filepath}: {e}")
    
    def _extract_definitions(self, tree, module_name):
        """Extract class and function definitions from AST."""
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                self._extract_class(node, module_name)
            elif isinstance(node, ast.FunctionDef):
                # Only capture top-level functions (not methods)
                if self._is_top_level_function(tree, node):
                    if module_name not in self.functions:
                        self.functions[module_name] = []
                    self.functions[module_name].append(node.name)
    
    def _is_top_level_function(self, tree, func_node):
        """Check if a function is top-level (not a method inside a class)."""
        for node in tree.body:
            if node == func_node:
                return True
            if isinstance(node, ast.ClassDef):
                for item in node.body:
                    if item == func_node:
                        return False
        return False
    
    def _extract_class(self, class_node, module_name):
        """Extract class information including methods."""
        class_info = {
            'name': class_node.name,
            'module': module_name,
            'methods': [],
            'bases': []
        }
        
        # Extract base classes
        for base in class_node.bases:
            if isinstance(base, ast.Name):
                class_info['bases'].append(base.id)
            elif isinstance(base, ast.Attribute):
                class_info['bases'].append(base.attr)
        
        # Extract methods
        for item in class_node.body:
            if isinstance(item, ast.FunctionDef):
                class_info['methods'].append(item.name)
        
        self.classes.append(class_info)
    
    def generate_mermaid(self):
        """Generate Mermaid classDiagram syntax."""
        lines = ["classDiagram"]
        lines.append("")
        
        # Generate classes
        for cls in self.classes:
            lines.append(f"    class {cls['name']} {{")
            for method in cls['methods']:
                lines.append(f"        +{method}()")
            lines.append("    }")
            lines.append("")
        
        # Generate pseudo-classes for standalone functions
        for module_name, functions in self.functions.items():
            if functions:
                # Create a meaningful class name from module name
                class_name = self._module_to_class_name(module_name)
                lines.append(f"    class {class_name} {{")
                lines.append(f"        <<module>>")
                for func in functions:
                    lines.append(f"        +{func}()")
                lines.append("    }")
                lines.append("")
        
        # Add inheritance relationships
        for cls in self.classes:
            for base in cls['bases']:
                # Check if base class exists in our classes
                if any(c['name'] == base for c in self.classes):
                    lines.append(f"    {base} <|-- {cls['name']}")
        
        return "\n".join(lines)
    
    def _module_to_class_name(self, module_name):
        """Convert module name to a class-like name."""
        if module_name == "app":
            return "AppRoutes"
        elif module_name == "setup":
            return "SetupFunctions"
        elif module_name == "device_setup":
            return "DeviceSetupRoutes"
        else:
            # Generic conversion: capitalize and remove special chars
            return module_name.replace("_", "").capitalize() + "Module"


def main():
    """Main function to generate Mermaid diagram."""
    # Get the project root directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    # Files to parse
    files_to_parse = [
        (project_root / "app.py", "app"),
        (project_root / "setup.py", "setup"),
        (project_root / "device_setup" / "__init__.py", "device_setup"),
    ]
    
    # Initialize generator
    generator = MermaidDiagramGenerator()
    
    # Parse all files
    for filepath, module_name in files_to_parse:
        if filepath.exists():
            print(f"Parsing {filepath}...")
            generator.parse_file(filepath, module_name)
        else:
            print(f"Warning: {filepath} not found, skipping...")
    
    # Generate Mermaid diagram
    mermaid_output = generator.generate_mermaid()
    
    # Ensure docs directory exists
    docs_dir = project_root / "docs"
    docs_dir.mkdir(exist_ok=True)
    
    # Write to file
    output_file = docs_dir / "diagram.mmd"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(mermaid_output)
    
    print(f"\nMermaid diagram generated successfully at {output_file}")
    print(f"Found {len(generator.classes)} classes and {sum(len(funcs) for funcs in generator.functions.values())} functions")


if __name__ == "__main__":
    main()
