import { useEditor } from "@layerhub-io/react";
import { fabric } from "fabric";
import { useEffect } from "react";

// Extender fabric.Canvas para incluir propiedades personalizadas
interface CustomFabricCanvas extends fabric.Canvas {
  lastPosX?: number;
  lastPosY?: number;
}

function MyEditor() {
  const editor = useEditor();

  // Activar/desactivar panning
  const enablePanning = () => {
    const canvas = editor.canvas.canvas as CustomFabricCanvas; // Acceder al canvas de Fabric.js
    canvas.isDrawingMode = true;
    canvas.selection = false; // Deshabilitar selección de objetos
    canvas.defaultCursor = "grab"; // Cambiar el cursor
  };

  const disablePanning = () => {
    const canvas = editor.canvas.canvas as CustomFabricCanvas;
    canvas.isDrawingMode = false;
    canvas.selection = true; // Volver a permitir selección
    canvas.defaultCursor = "default";
  };

  // Eventos del mouse para arrastrar
  const handleMouseDown = (e: fabric.IEvent) => {
    const canvas = editor.canvas.canvas as CustomFabricCanvas;
    if (canvas.isDrawingMode) {
      canvas.lastPosX = (e.e as MouseEvent).clientX;
      canvas.lastPosY = (e.e as MouseEvent).clientY;
    }
  };

  const handleMouseMove = (e: fabric.IEvent) => {
    const canvas = editor.canvas.canvas as CustomFabricCanvas;
    if (canvas.isDrawingMode && canvas.lastPosX !== undefined && canvas.lastPosY !== undefined) {
      const deltaX = (e.e as MouseEvent).clientX - canvas.lastPosX;
      const deltaY = (e.e as MouseEvent).clientY - canvas.lastPosY;
      canvas.viewportTransform![4] += deltaX;
      canvas.viewportTransform![5] += deltaY;
      canvas.requestRenderAll();
      canvas.lastPosX = (e.e as MouseEvent).clientX;
      canvas.lastPosY = (e.e as MouseEvent).clientY;
    }
  };

  // Configurar eventos al montar el componente
  useEffect(() => {
    const canvas = editor?.canvas.canvas as CustomFabricCanvas;
    if (canvas) {
      canvas.on("mouse:down", handleMouseDown);
      canvas.on("mouse:move", handleMouseMove);
      canvas.on("mouse:up", disablePanning);
    }

    return () => {
      if (canvas) {
        canvas.off("mouse:down", handleMouseDown);
        canvas.off("mouse:move", handleMouseMove);
        canvas.off("mouse:up", disablePanning);
      }
    };
  }, [editor]);

  return (
    <div>
      <button onMouseDown={enablePanning} onMouseUp={disablePanning}>
        🖐️ Activar desplazamiento
      </button>
    </div>
  );
}

export default MyEditor;