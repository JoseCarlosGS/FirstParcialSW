import os
from fastapi import HTTPException

def replace_in_file(file_path: str, old_value: str, new_value: str) -> str:
    """
    Abre un archivo, reemplaza una cadena específica y devuelve el contenido modificado.
    
    :param file_path: Ruta completa al archivo.
    :param old_value: Cadena a buscar en el archivo.
    :param new_value: Cadena que reemplazará a old_value.
    :return: El contenido del archivo modificado.
    :raises HTTPException: Si ocurre un error al leer o escribir el archivo.
    """
    try:
        # Leer el contenido del archivo
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        # Realizar el reemplazo
        modified_content = content.replace(old_value, new_value)

        # Guardar los cambios en el archivo
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(modified_content)

        return modified_content  # Devuelve el contenido modificado si es necesario
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail=f"El archivo no fue encontrado: {file_path}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar el archivo {file_path}: {str(e)}")
    
def replace_entire_file(file_path: str, new_content: str):
    """
    Reemplaza todo el contenido de un archivo con el nuevo contenido proporcionado.
    
    :param file_path: Ruta completa al archivo.
    :param new_content: Nuevo contenido que reemplazará el contenido existente del archivo.
    :raises HTTPException: Si ocurre un error al escribir el archivo.
    """
    try:
        # Sobrescribir el archivo con el nuevo contenido
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(new_content)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail=f"El archivo no fue encontrado: {file_path}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al escribir en el archivo {file_path}: {str(e)}")