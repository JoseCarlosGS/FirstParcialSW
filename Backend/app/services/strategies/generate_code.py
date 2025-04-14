import os
import zipfile
import tempfile

from fastapi import HTTPException
from abc import ABC, abstractmethod
from ...utils.constants.mock_data import MOCK_DATA

class GenerateCodeStrategy(ABC):
    @abstractmethod
    def execute(self, prompt: str) -> str:
        pass

class DefaultCodeGenerationStrategy(GenerateCodeStrategy):
    """
    Base class for code generation strategies.
    By default, it returns a simple string.
    """

    def execute(self, prompt: str) -> str:
        try:
            # Crear carpeta temporal
            with tempfile.TemporaryDirectory() as temp_dir:
                # Crear archivos
                html_path = os.path.join(temp_dir, "registro-usuario.component.html")
                css_path = os.path.join(temp_dir, "registro-usuario.component.css")
                ts_path = os.path.join(temp_dir, "registro-usuario.component.ts")

                with open(html_path, "w", encoding="utf-8") as f:
                    f.write(MOCK_DATA["html"].strip())
                with open(css_path, "w", encoding="utf-8") as f:
                    f.write(MOCK_DATA["css"].strip())
                with open(ts_path, "w", encoding="utf-8") as f:
                    f.write(MOCK_DATA["typescript"].strip())

                # Ruta para el ZIP en un lugar fuera del contexto temporal
                final_zip_path = os.path.join(tempfile.gettempdir(), "component_code.zip")

                with zipfile.ZipFile(final_zip_path, 'w') as zipf:
                    zipf.write(html_path, os.path.basename(html_path))
                    zipf.write(css_path, os.path.basename(css_path))
                    zipf.write(ts_path, os.path.basename(ts_path))

            # Verificamos si se creó correctamente
            if not os.path.exists(final_zip_path):
                raise Exception("No se pudo generar el archivo ZIP.")

            return final_zip_path

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error generando el código: {str(e)}")