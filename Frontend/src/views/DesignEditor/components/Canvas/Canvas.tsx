import { Canvas as LayerhubCanvas, useEditor } from "@layerhub-io/react"
import Playback from "../Playback"
import useDesignEditorContext from "~/hooks/useDesignEditorContext"
import ContextMenu from "../ContextMenu"
import React, { useRef, useEffect, useState } from "react"
import { fabric } from "fabric"

const Canvas = () => {
  const editor = useEditor()
  const { displayPlayback } = useDesignEditorContext()
  const wrapperRef = useRef<HTMLDivElement>(null)

  const [isSpacePressed, setIsSpacePressed] = useState(false)
  const [isDragging, setIsDragging] = useState(false)
  const [lastPos, setLastPos] = useState<{ x: number; y: number } | null>(null)


  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.code === "ControlLeft") {
        setIsSpacePressed(true)
        e.preventDefault()
      }
    }

    const handleKeyUp = (e: KeyboardEvent) => {
      if (e.code === "ControlLeft") {
        setIsSpacePressed(false)
      }
    }

    window.addEventListener("keydown", handleKeyDown)
    window.addEventListener("keyup", handleKeyUp)

    return () => {
      window.removeEventListener("keydown", handleKeyDown)
      window.removeEventListener("keyup", handleKeyUp)
    }
  }, [])

  useEffect(() => {
    if (!editor || !editor.canvas?.canvas) return;
    
    const canvas = editor.canvas.canvas;
    const wrapper = wrapperRef.current;
    
    if (!wrapper) return;
    
    const handleMouseDown = (e: MouseEvent) => {
      if (!isSpacePressed) return;
      
      // Deshabilitar eventos temporalmente
      canvas.selection = false;
      canvas.isDrawingMode = false;
      canvas.skipTargetFind = true;
      
      setIsDragging(true);
      setLastPos({ x: e.clientX, y: e.clientY });
      canvas.defaultCursor = "grabbing";
    };
    
    const handleMouseMove = (e: MouseEvent) => {
      if (!isDragging || !lastPos) return;
      
      const deltaX = e.clientX - lastPos.x;
      const deltaY = e.clientY - lastPos.y;
      
      // Utilizar requestAnimationFrame para evitar problemas de rendimiento
      requestAnimationFrame(() => {
        canvas.relativePan(new fabric.Point(deltaX, deltaY));
      });
      
      setLastPos({ x: e.clientX, y: e.clientY });
    };
    
    const handleMouseUp = () => {
      if (!isDragging) return;
      
      // Restaurar configuración del canvas
      canvas.selection = true;
      canvas.skipTargetFind = false;
      
      setIsDragging(false);
      setLastPos(null);
      canvas.defaultCursor = isSpacePressed ? "grab" : "default";
    };
    
    if (isSpacePressed) {
      canvas.defaultCursor = isDragging ? "grabbing" : "grab";
    } else {
      canvas.defaultCursor = "default";
    }
    
    wrapper.addEventListener("mousedown", handleMouseDown);
    window.addEventListener("mousemove", handleMouseMove); // Usa window para capturar movimientos fuera del wrapper
    window.addEventListener("mouseup", handleMouseUp);
    
    return () => {
      wrapper.removeEventListener("mousedown", handleMouseDown);
      window.removeEventListener("mousemove", handleMouseMove);
      window.removeEventListener("mouseup", handleMouseUp);
      
      // Asegura restaurar el estado del canvas al desmontar
      if (canvas) {
        canvas.selection = true;
        canvas.skipTargetFind = false;
        canvas.defaultCursor = "default";
      }
    };
  }, [editor, isSpacePressed, isDragging, lastPos]);
  return (
    <div ref={wrapperRef} style={{ flex: 1, display: "flex", position: "relative" }}>
      {displayPlayback && <Playback />}
      <ContextMenu />
      <LayerhubCanvas
        config={{
          background: "#f1f2f6",
          controlsPosition: {
            rotation: "BOTTOM",
          },
          shadow: {
            blur: 4,
            color: "#fcfcfc",
            offsetX: 0,
            offsetY: 0,
          },
        }}
      />
    </div>
  )
}

export default Canvas
