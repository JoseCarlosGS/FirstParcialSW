import os
import jinja2
from typing import Dict, Any

class TemplateEngine:
    def __init__(self):
        self.template_dir = os.path.join(os.path.dirname(__file__), "utils")
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.template_dir),
            autoescape=jinja2.select_autoescape(['html', 'xml'])
        )
    
    def render(self, template_name: str, context: Dict[str, Any]) -> str:
        """Renderiza una plantilla con el contexto dado y devuelve el resultado"""
        template = self.env.get_template(template_name)
        return template.render(**context)
    
    def render_to_file(self, template_name: str, output_path: str, context: Dict[str, Any]):
        """Renderiza una plantilla a un archivo"""
        content = self.render(template_name, context)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)