from fastapi import HTTPException
from ...models.project import ProjectConfig
import subprocess
import zipfile
import os
import shutil

class GenerateByComand():
    
    def __init__(self):
        pass
    
    def execute(self, project_name: str, config : ProjectConfig , component_type: str, output_dir: str) -> None:
        """Ejecuta la generación de un componente en el directorio especificado."""
        # Lógica para ejecutar la generación de componentes
        project_name = project_name.strip()
        if not project_name:
            raise HTTPException(status_code=400, detail="El nombre del proyecto no puede estar vacío.")
        
        # Opciones adicionales para ng new
        options = [
            "--routing" if config.routing else "",
            f"--style={config.style}",
            "--skip-git" if config.skip_git else ""
        ]
        options = [opt for opt in options if opt]
        
        try:
            ng_path = shutil.which("ng") or r"C:\Users\modos\AppData\Roaming\nvm\v20.13.0\ng.cmd"
            if not ng_path:
                raise HTTPException(status_code=500, detail="No se encontró el ejecutable de Angular CLI (ng)")

            subprocess.run(
                [ng_path, "new", project_name] + options,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        except subprocess.CalledProcessError as e:
            raise HTTPException(status_code=500, detail=f"Error al generar el proyecto: {e.stderr.decode()}")   
            # 3. Empaquetar el proyecto en un archivo ZIP
        zip_filename = f"{project_name}.zip"
        project_path = os.path.join(os.getcwd(), project_name)
        zip_path = os.path.join(os.getcwd(), zip_filename)
        
        try:
            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(project_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, project_path)
                        zipf.write(file_path, arcname)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al comprimir el proyecto: {str(e)}")

        # 4. Limpiar la carpeta del proyecto después de comprimirla
        try:
            shutil.rmtree(project_path)
        except Exception as e:
            print(f"Advertencia: No se pudo eliminar la carpeta del proyecto: {str(e)}")

        return {"zip_path": zip_path, "filename": zip_filename}