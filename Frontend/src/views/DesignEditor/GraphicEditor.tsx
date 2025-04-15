import Navbar from "./components/Navbar"
import Panels from "./components/Panels"
import Canvas from "./components/Canvas"
import Footer from "./components/Footer"
import Toolbox from "./components/Toolbox"
import EditorContainer from "./components/EditorContainer"
import { useLocation } from "react-router-dom";
import useDesignEditorContext from "~/hooks/useDesignEditorContext"
import { useEditor } from "@layerhub-io/react"
import { useEffect } from "react"
import api from "~/services/api"
import { useLoadGraphicTemplate } from "../../hooks/useLoadTemplate"
import { IDesign } from "~/interfaces/DesignEditor"

const GraphicEditor = () => {
  const location = useLocation();
  const editor = useEditor()
  const { setEditorType, setScenes, setCurrentDesign: originalSetCurrentDesign } = useDesignEditorContext()
  const setCurrentDesign = (design: Partial<IDesign>) => {
    originalSetCurrentDesign((prev) => ({ ...prev, ...design }));
  };
  const queryParams = new URLSearchParams(location.search);
  const idProject = queryParams.get("id");
  const { load, loading, error } = useLoadGraphicTemplate(setScenes, setCurrentDesign)
  
  console.log("Id from URL:", idProject);

  useEffect(() => {
    // Establecer el tipo de editor manualmente
    setEditorType("GRAPHIC");
  }, []);

  useEffect(() => {
    if (!editor) return
  
    if (idProject) {
      loadProject()
    }
  }, [editor, idProject])


  const loadProject = async () => {
    const project = await api.getTemplateById(idProject || "")
    if (project) {
      await load(project)
    }
  }

  if (error) {
    console.log("Error:", error)
  }

  const LoadingOverlay = () => (
    <div style={{
      position: "absolute",
      top: 0,
      left: 0,
      width: "100%",
      height: "100%",
      backgroundColor: "rgba(255, 255, 255, 0.8)",
      zIndex: 9999,
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
    }}>
      <div className="spinner" />
      <style>
        {`
          .spinner {
            width: 50px;
            height: 50px;
            border: 5px solid #ccc;
            border-top-color: #000;
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
          }
          @keyframes spin {
            to { transform: rotate(360deg); }
          }
        `}
      </style>
    </div>
  )
  

  return (
    <EditorContainer>
      <Navbar />
      <div style={{ display: "flex", flex: 1 }}>
        <Panels />
        <div style={{ flex: 1, display: "flex", flexDirection: "column", position: "relative" }}>
          <Toolbox />
          <Canvas />
          <Footer />
        </div>
      </div>
      {loading && <LoadingOverlay />}
    </EditorContainer>
  )
}

export default GraphicEditor
