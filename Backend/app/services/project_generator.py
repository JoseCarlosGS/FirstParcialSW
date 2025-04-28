import os
import shutil
import uuid

from fastapi import HTTPException, Response

from ..schemas.config_schemas import ProjectConfig
from ..services.template_engine import TemplateEngine
from .utils.component_generator import ComponentGenerator
from ..services.strategies.generate_strategies import GenerateProjectStrategy, GenerateByCommand
from ..services.strategies.generate_code import DefaultCodeGenerationStrategy
from ..models.project import Project

class AngularProjectGenerator:
    def __init__(self):
        self.strategy = None
        self.template_engine = TemplateEngine()
        self.component_generator = ComponentGenerator()
        self.projects_dir = os.path.join(os.getcwd(), "generated_projects")
        os.makedirs(self.projects_dir, exist_ok=True)
        
    def set_strategy(self, strategy):
        self.strategy = strategy
        
    def execute_strategy(self, *args, **kwargs):
        if self.strategy is None:
            raise ValueError("Strategy not set")
        return self.strategy.execute(*args, **kwargs)
        
    def generate_project(self, config: ProjectConfig, project_schema: ProjectConfig = None, ) -> str:
        """Genera un proyecto Angular completo basado en el esquema y devuelve la ruta al zip"""
        # Crear directorio temporal para el proyecto
        self.set_strategy(GenerateByCommand())
        return self.execute_strategy(project_name="hola-mundo", config= config, component_type="text", output_dir=self.projects_dir)
        # project_id = str(uuid.uuid4())
        # project_dir = os.path.join(self.projects_dir, project_id)
        # os.makedirs(project_dir)
        
        # try:
        #     # 1. Generar estructura base del proyecto Angular
        #     self._generate_base_structure(project_dir, project_schema)
            
        #     # 2. Generar componentes basados en el esquema
        #     self._generate_components(project_dir, project_schema)
            
        #     # 3. Generar archivos de configuración
        #     self._generate_config_files(project_dir, project_schema)
            
        #     # 4. Instalar dependencias
        #     self._install_dependencies(project_dir)
            
        #     # 5. Empaquetar el proyecto
        #     zip_path = self._package_project(project_dir)
            
        #     return zip_path
        # except Exception as e:
        #     # Limpiar en caso de error
        #     shutil.rmtree(project_dir, ignore_errors=True)
        #     raise HTTPException(status_code=500, detail=f"Error generando proyecto: {str(e)}")
    
    def generate_component(self, prompt:str, project_schema: ProjectConfig = None, component_type: str= None):
        """Genera un componente Angular basado en el esquema y devuelve la ruta al zip"""
        self.set_strategy(DefaultCodeGenerationStrategy())
        return self.execute_strategy(prompt=prompt)
    
    def _generate_base_structure(self, project_dir: str, project_schema: ProjectConfig):
        """Genera la estructura base de un proyecto Angular"""
        # Generar estructura de directorios
        os.makedirs(os.path.join(project_dir, "src", "app"), exist_ok=True)
        os.makedirs(os.path.join(project_dir, "src", "assets"), exist_ok=True)
        os.makedirs(os.path.join(project_dir, "src", "environments"), exist_ok=True)
        
        # Generar archivos base desde plantillas
        self.template_engine.render_to_file(
            "angular.json", 
            os.path.join(project_dir, "angular.json"),
            {"project_name": project_schema.name}
        )
        self.template_engine.render_to_file(
            "package.json", 
            os.path.join(project_dir, "package.json"),
            {"project_name": project_schema.name, "author": project_schema.author}
        )
        self.template_engine.render_to_file(
            "tsconfig.json", 
            os.path.join(project_dir, "tsconfig.json"),
            {}
        )
        self.template_engine.render_to_file(
            "index.html", 
            os.path.join(project_dir, "src", "index.html"),
            {"project_name": project_schema.name}
        )
        self.template_engine.render_to_file(
            "main.ts", 
            os.path.join(project_dir, "src", "main.ts"),
            {}
        )
    
    def _generate_components(self, project_dir: str, project_schema: ProjectConfig):
        """Genera componentes Angular basados en el esquema"""
        app_dir = os.path.join(project_dir, "src", "app")
        
        # Generar modelos compartidos
        models_dir = os.path.join(app_dir, "models")
        os.makedirs(models_dir, exist_ok=True)
        self.template_engine.render_to_file(
            "component.interface.ts", 
            os.path.join(models_dir, "component.interface.ts"),
            {}
        )
        
        # Generar componentes para cada tipo de componente
        components_dir = os.path.join(app_dir, "components")
        os.makedirs(components_dir, exist_ok=True)
        
        # Generar componentes básicos
        component_types = ["text", "button", "container", "grid", "input"]
        for comp_type in component_types:
            comp_dir = os.path.join(components_dir, f"{comp_type}-component")
            os.makedirs(comp_dir, exist_ok=True)
            self.component_generator.generate_component(comp_type, comp_dir)
        
        # Generar componente dinámico
        dynamic_dir = os.path.join(components_dir, "dynamic-component")
        os.makedirs(dynamic_dir, exist_ok=True)
        self.component_generator.generate_dynamic_component(dynamic_dir)
        
        # Generar componente de proyecto
        project_comp_dir = os.path.join(components_dir, "project-renderer")
        os.makedirs(project_comp_dir, exist_ok=True)
        self.component_generator.generate_project_component(project_comp_dir)
        
        # Generar módulo principal
        self.template_engine.render_to_file(
            "app.module.ts", 
            os.path.join(app_dir, "app.module.ts"),
            {"project_name": project_schema.name}
        )
        
        # Generar componente principal y servicio
        self.template_engine.render_to_file(
            "app.component.ts", 
            os.path.join(app_dir, "app.component.ts"),
            {"project": project_schema.dict()}
        )
        
        # Generar servicios
        services_dir = os.path.join(app_dir, "services")
        os.makedirs(services_dir, exist_ok=True)
        self.template_engine.render_to_file(
            "component-renderer.service.ts", 
            os.path.join(services_dir, "component-renderer.service.ts"),
            {}
        )
    
    def _generate_config_files(self, project_dir: str, project_schema: ProjectConfig):
        """Genera archivos de configuración adicionales"""
        # Generar archivos de entorno
        env_dir = os.path.join(project_dir, "src", "environments")
        self.template_engine.render_to_file(
            "environment.ts", 
            os.path.join(env_dir, "environment.ts"),
            {"production": False}
        )
        self.template_engine.render_to_file(
            "environment.prod.ts", 
            os.path.join(env_dir, "environment.prod.ts"),
            {"production": True}
        )
        
        # Generar archivo de estilos globales
        self.template_engine.render_to_file(
            "styles.scss", 
            os.path.join(project_dir, "src", "styles.scss"),
            {}
        )
    
    def _install_dependencies(self, project_dir: str):
        """Instala las dependencias del proyecto"""
        # Opcionalmente, instalar dependencias con npm
        # Esto es opcional y puede tomar tiempo
        # subprocess.run(["npm", "install", "--prefix", project_dir], check=True)
        pass
    
    def _package_project(self, project_dir: str) -> str:
        """Empaqueta el proyecto en un archivo ZIP"""
        # Nombre basado en el directorio
        project_name = os.path.basename(project_dir)
        zip_path = os.path.join(self.projects_dir, f"{project_name}.zip")
        
        # Crear ZIP
        shutil.make_archive(
            os.path.splitext(zip_path)[0],  # Quitar extensión .zip
            'zip',
            project_dir
        )
        
        return zip_path