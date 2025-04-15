import { BrowserRouter, Routes, Route } from "react-router-dom"
import DesignEditor from "~/views/DesignEditor"
import Dashboard from "~/views/Dashboard"
import GraphicEditor from "./views/DesignEditor/GraphicEditor"

const Router = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/manage" element={<Dashboard />} />
        <Route path="/" element={<DesignEditor />} />
        <Route path="/project" element={<GraphicEditor />} />
      </Routes>
    </BrowserRouter>
  )
}

export default Router
