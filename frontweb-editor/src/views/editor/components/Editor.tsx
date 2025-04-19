import React, { useEffect, useRef, useState } from 'react';
import grapesjs from 'grapesjs';
import { Editor as GrapesEditor } from 'grapesjs';
import io from 'socket.io-client';
import 'grapesjs/dist/css/grapes.min.css';
import { customBlocks } from '../../../constants/CustomBlocks';
import Navbar from './Navbar';
import { useEditor } from '../../../contexts/AppContext';
import { AppContext } from '../../../contexts/AppContext';

// Tipo para los datos del proyecto (opcional, pero recomendado)
interface ProjectData {
  components: any; // Cambiado a 'any' para aceptar el tipo devuelto por editor.getComponents()
  styles: string;
}

const Editor: React.FC = () => {
  const editorRef = useRef<HTMLDivElement | null>(null);
  const [editor, setEditor] = useState<GrapesEditor | null>(null);
  //const socket = useRef(io('http://localhost:3000')); // Conexión a Socket.IO

  useEffect(() => {
    if (!editorRef.current) return;

    // Inicializar GrapesJS
    const e = grapesjs.init({
        container: '#gjs',
        fromElement: true,
        height: '100vh',
        width: '100%',
        storageManager: false, // Desactivar almacenamiento automático
        blockManager: {
          //appendTo: '#blocks',
        },
        
      })
      customBlocks.forEach(block => e.BlockManager.add(block.id, block));
      setEditor(e);
    

    // // Escuchar cambios locales y enviar al servidor
    // editor.on('change', () => {
    //   const projectData: ProjectData = {
    //     components: editor.getComponents(),
    //     styles: JSON.stringify(editor.getStyle()),
    //   };
    //   socket.current.emit('update', projectData);
    // });

    // // Escuchar cambios remotos y actualizar el editor
    // socket.current.on('update', (data: ProjectData) => {
    //   editor.setComponents(data.components);
    //   editor.setStyle(data.styles);
    // });

    // // Limpiar el socket cuando se desmonta el componente
    // return () => {
    //   socket.current.disconnect();
    // };
  }, []);

  return (
    <div>
      <AppContext.Provider value={editor}>
        <Navbar />
          <div 
          id="gjs" 
          ref={editorRef} 
          style={{ height: '80vh', width: '99%', border: '1px solid #ccc' }} ></div>
        <button id="export-btn">Exportar proyecto</button>
      </AppContext.Provider>
    </div>
  );
};

export default Editor;