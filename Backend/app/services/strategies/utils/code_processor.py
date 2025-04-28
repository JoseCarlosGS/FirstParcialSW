import re
import os
import subprocess
from fastapi import HTTPException
import shutil

def insert_code_into_component_ts(file_path: str, code_to_insert: str):
    """Inserta código dentro del cuerpo de la clase exportada en un archivo de componente Angular."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        # Buscar la clase exportada
        class_pattern = r"(export\s+class\s+\w+\s*\{)"
        match = re.search(class_pattern, content)

        if not match:
            raise ValueError("No se encontró una clase exportada en el archivo.")

        insert_position = match.end()

        # Insertar el código justo después de la apertura de la clase
        updated_content = content[:insert_position] + "\n" + code_to_insert.strip() + "\n" + content[insert_position:]

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(updated_content)

    except Exception as e:
        raise Exception(f"Error al insertar código en {file_path}: {str(e)}")
    
def generate_components_from_mock(components_list: list, project_path: str):
    """Genera componentes Angular a partir de una lista mock y reemplaza sus archivos."""

    ng_path = shutil.which("ng") or r"C:\Users\modos\AppData\Roaming\nvm\v20.13.0\ng.cmd"
    if not ng_path:
        raise HTTPException(status_code=500, detail="No se encontró el ejecutable de Angular CLI (ng)")

    components_folder = os.path.join(project_path, "src", "app", "components")
    os.makedirs(components_folder, exist_ok=True)

    for comp in components_list:
        name = comp.get("name")
        html = comp.get("html", "")
        css = comp.get("css", "")
        typescript = comp.get("typescript", "")

        if not name:
            print("Componente sin nombre, saltando...")
            continue

        try:
            # Generar el componente
            subprocess.run(
                [ng_path, "generate", "component", f"components/{name}", "--skip-tests"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=project_path
            )
        except subprocess.CalledProcessError as e:
            raise HTTPException(status_code=500, detail=f"Error al generar el componente {name}: {e.stderr.decode()}")

        # Paths de los archivos generados
        component_dir = os.path.join(components_folder, name)
        html_path = os.path.join(component_dir, f"{name}.component.html")
        css_path = os.path.join(component_dir, f"{name}.component.css")
        ts_path = os.path.join(component_dir, f"{name}.component.ts")

        # Reemplazar HTML
        if os.path.exists(html_path):
            try:
                with open(html_path, "w", encoding="utf-8") as f:
                    f.write(html)
            except Exception as e:
                raise Exception(f"Error al escribir en {html_path}: {str(e)}")

        # Reemplazar CSS
        if os.path.exists(css_path):
            try:
                with open(css_path, "w", encoding="utf-8") as f:
                    f.write(css)
            except Exception as e:
                raise Exception(f"Error al escribir en {css_path}: {str(e)}")

        # Insertar en el TypeScript
        if os.path.exists(ts_path):
            try:
                insert_code_into_component_ts(ts_path, typescript)
            except Exception as e:
                raise Exception(f"Error al procesar el archivo TypeScript {ts_path}: {str(e)}")

