import os
from typing import Dict, Any, List
from ..template_engine import TemplateEngine

class ComponentGenerator:
    def __init__(self):
        self.template_engine = TemplateEngine()
    
    def generate_component(self, component_type: str, output_dir: str):
        """Genera archivos para un componente básico"""
        # Generar archivo .ts
        self.template_engine.render_to_file(
            f"{component_type}-component.ts", 
            os.path.join(output_dir, f"{component_type}-component.component.ts"),
            {}
        )
        
        # Generar archivo HTML template si se necesita
        if component_type not in ['dynamic-component']:
            self.template_engine.render_to_file(
                f"{component_type}-component.html", 
                os.path.join(output_dir, f"{component_type}-component.component.html"),
                {}
            )
        
        # Generar archivo CSS/SCSS
        self.template_engine.render_to_file(
            f"{component_type}-component.scss", 
            os.path.join(output_dir, f"{component_type}-component.component.scss"),
            {}
        )
    
    def generate_dynamic_component(self, output_dir: str):
        """Genera el componente dinámico que crea componentes basados en el tipo"""
        self.template_engine.render_to_file(
            "dynamic-component.ts", 
            os.path.join(output_dir, "dynamic-component.component.ts"),
            {}
        )
    
    def generate_project_component(self, output_dir: str):
        """Genera el componente que renderiza el proyecto completo"""
        self.template_engine.render_to_file(
            "project-renderer.ts", 
            os.path.join(output_dir, "project-renderer.component.ts"),
            {}
        )
        self.template_engine.render_to_file(
            "project-renderer.html", 
            os.path.join(output_dir, "project-renderer.component.html"),
            {}
        )
        self.template_engine.render_to_file(
            "project-renderer.scss", 
            os.path.join(output_dir, "project-renderer.component.scss"),
            {}
        )