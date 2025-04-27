import StudioEditor from '@grapesjs/studio-sdk/react';
import '@grapesjs/studio-sdk/style';
import { useEditor } from '../../../contexts/AppContext';
import { useEffect } from 'react';
import { useWebSocketContext } from '../../../contexts/WebSocketContext';

// ...
const GrapesEditor = () => {
    const { setEditor } = useEditor();
    const socket = useWebSocketContext();
    
    const handleEditorReady = (editorInstance:any) => {
        // Guardar la instancia del editor en el contexto
        setEditor(editorInstance);
        //console.log('Editor listo y guardado en contexto: ', editorInstance);
        editorInstance.on('component:add', (component: any) => {
            console.log("Nuevo componente añadido:", component);

            if (socket?.sendMessage) {
                socket.sendMessage(JSON.stringify({
                type: "editor-update",
                data: {
                    action: "add",
                    component: component.toJSON()
                }
                }));
            }
        });
    };

return(
    <StudioEditor
    options={{
        // ...
        licenseKey: 'TU_CLAVE_DE_LICENCIA', 
        project: {
        type: 'web',
        // The default project to use for new projects
        default: {
            pages: [
            { name: 'Home', component: '<h1>Home page</h1>' },
            { name: 'About', component: '<h1>About page</h1>' },
            { name: 'Contact', component: '<h1>Contact page</h1>' },
            ]
        },
        },
        onReady: handleEditorReady,
    }}
    
    />
)}

export default GrapesEditor;