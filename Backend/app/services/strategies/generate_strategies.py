import subprocess
import zipfile
import os
import shutil
from fastapi import HTTPException
from abc import ABC, abstractmethod

from ...models.project import Project
from ...schemas.config_schemas import ProjectConfig
from ...utils.constants.modules_template import NO_STAND_ALONE_DEFAULT
from ...utils.constants.mock_data import MOCK_DATA
from .utils.file_processor import replace_entire_file
from .utils.code_processor import generate_components_from_mock

app_module_ts = NO_STAND_ALONE_DEFAULT.get('app_module_ts')
app_component_html = NO_STAND_ALONE_DEFAULT.get('app_componet_html')
app_component_css = MOCK_DATA[0].get('css')

components_mock = MOCK_DATA



class GenerateProjectStrategy(ABC):
    @abstractmethod
    def execute(self, *args, **kwargs):
        pass

class GenerateByCommand(GenerateProjectStrategy):
    def __init__(self):
        # Directorio temporal donde se guardarán los proyectos
        self.temp_dir = os.path.join(os.getcwd(), "temp-projects")
        os.makedirs(self.temp_dir, exist_ok=True)  # Crear el directorio si no existe

    def execute(self, project_name: str, config: ProjectConfig, component_type: str, output_dir: str) -> dict:
        """Ejecuta la generación de un componente en el directorio especificado."""
        project_name = config.project_name.strip()
        if not project_name:
            raise HTTPException(status_code=400, detail="El nombre del proyecto no puede estar vacío.")

        # Opciones adicionales para ng new
        options = [
            "--routing" if config.routing else "",
            f"--style={config.style}",
            "--skip-install",
            "--skip-git" if config.skip_git else "",
            "--standalone=false",
        ]
        options = [opt for opt in options if opt]

        try:
            ng_path = shutil.which("ng") or r"C:\Users\modos\AppData\Roaming\nvm\v20.13.0\ng.cmd"
            if not ng_path:
                raise HTTPException(status_code=500, detail="No se encontró el ejecutable de Angular CLI (ng)")

            # Generar el proyecto en el directorio temporal
            temp_project_path = os.path.join(self.temp_dir, project_name)
            subprocess.run(
                [ng_path, "new", project_name] + options,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=self.temp_dir  # Cambiar el directorio de trabajo al directorio temporal
            )
        except subprocess.CalledProcessError as e:
            raise HTTPException(status_code=500, detail=f"Error al generar el proyecto: {e.stderr.decode()}")

        # Modificar el archivo angular.json antes de empaquetar
        # angular_json_path = os.path.join(temp_project_path, "app.module.ts")
        app_module_ts_path = os.path.join(f"{temp_project_path}/src/app", "app.module.ts")
        if os.path.exists(app_module_ts_path):
            try:
                replace_entire_file(app_module_ts_path, app_module_ts)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error al leer/modificar app.module.ts: {str(e)}")
            
        app_component_html_path = os.path.join(f"{temp_project_path}/src/app", "app.component.html")
        if os.path.exists(app_component_html_path):
            try:
                replace_entire_file(app_component_html_path, app_component_html)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error al leer/modificar app.component.html: {str(e)}")
            
        app_component_css_path = os.path.join(f"{temp_project_path}/src/app", "app.component.css")
        if os.path.exists(app_component_css_path):
            try:
                replace_entire_file(app_component_css_path, app_component_css)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error al leer/modificar app.component.css: {str(e)}")
        
        generate_components_from_mock(components_mock, project_path=temp_project_path)

        # Empaquetar el proyecto en un archivo ZIP
        zip_filename = f"{project_name}.zip"
        zip_path = os.path.join(self.temp_dir, zip_filename)

        try:
            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(temp_project_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, temp_project_path)
                        zipf.write(file_path, arcname)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al comprimir el proyecto: {str(e)}")

        # Limpiar la carpeta del proyecto después de comprimirla
        try:
            shutil.rmtree(temp_project_path)
        except Exception as e:
            print(f"Advertencia: No se pudo eliminar la carpeta del proyecto: {str(e)}")

        return {"zip_path": zip_path, "filename": zip_filename}
    
    
    def process_file(self, file_path, new_content):
        try:
            replace_entire_file(file_path, new_content)
            print(f"Contenido de {os.path.basename(file_path)}:")
            print(new_content)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error al procesar {os.path.basename(file_path)}: {str(e)}"
            )