from fastapi import HTTPException
from abc import ABC, abstractmethod
from ...models.project import Project
import subprocess
import zipfile
import os
import shutil

class GenerateProjectStrategy(ABC):
    @abstractmethod
    def execute(self, *args, **kwargs):
        pass

class GenerateByCommand(GenerateProjectStrategy):
    def __init__(self):
        # Directorio temporal donde se guardarán los proyectos
        self.temp_dir = os.path.join(os.getcwd(), "temp-projects")
        os.makedirs(self.temp_dir, exist_ok=True)  # Crear el directorio si no existe

    def execute(self, project_name: str, config: Project, component_type: str, output_dir: str) -> dict:
        """Ejecuta la generación de un componente en el directorio especificado."""
        project_name = config.project_name.strip()
        if not project_name:
            raise HTTPException(status_code=400, detail="El nombre del proyecto no puede estar vacío.")

        # Opciones adicionales para ng new
        options = [
            "--routing" if config.routing else "",
            f"--style={config.style}",
            "--skip-install",
            "--skip-git" if config.skip_git else ""
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
        angular_json_path = os.path.join(temp_project_path, "angular.json")
        if os.path.exists(angular_json_path):
            try:
                with open(angular_json_path, "r", encoding="utf-8") as file:
                    angular_json_content = file.read()
                    print("Contenido de angular.json:")
                    print(angular_json_content)

                # Aquí puedes realizar modificaciones en el archivo si es necesario
                # Por ejemplo, agregar o cambiar alguna configuración
                # angular_json_content = angular_json_content.replace("old_value", "new_value")

                # Guardar los cambios (si los hiciste)
                # with open(angular_json_path, "w", encoding="utf-8") as file:
                #     file.write(angular_json_content)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error al leer/modificar angular.json: {str(e)}")

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