// hooks/useLoadGraphicTemplate.ts
import { useState, useCallback } from "react"
import { loadTemplateFonts } from "~/utils/fonts"
import { useEditor } from "@layerhub-io/react" 
import { IScene } from "@layerhub-io/types"
import { IDesign } from "~/interfaces/DesignEditor"
import { loadVideoEditorAssets } from "~/utils/video"

interface UseLoadGraphicTemplateResult {
  load: (payload: IDesign) => Promise<void>
  loading: boolean
  error: string | null
}

export const useLoadGraphicTemplate = (
  setScenes: (s: IScene[]) => void,
  setCurrentDesign: (d: Partial<IDesign>) => void
): UseLoadGraphicTemplateResult => {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const editor = useEditor()
  const load = useCallback(async (payload: IDesign) => {
    setLoading(true)
    setError(null)

    try {
      const scenes: IScene[] = []
      const { scenes: scns, ...design } = payload

      for (const scn of scns) {
        const scene: IScene = {
          name: scn.name,
          frame: payload.frame,
          id: scn.id,
          layers: scn.layers,
          metadata: {},
        }
        const loadedScene = await loadVideoEditorAssets(scene)
        console.log("Editor status", editor.state)
        console.log("Editor not ready, waiting...")
        await loadTemplateFonts(loadedScene)


        const preview = (await editor.renderer.render(loadedScene)) as string
        scenes.push({ ...loadedScene, preview })
      }

      setScenes(scenes)
      setCurrentDesign(design);

      setTimeout(() => {
        const objectToLock = editor.objects.findById("imgbck")
        if (objectToLock) {
          editor.objects.lock("imgbck")
        }
      }, 500)

    } catch (err) {
      setError((err as Error).message)
    } finally {
      setLoading(false)
    }
  }, [setScenes, setCurrentDesign])

  return { load, loading, error }
}
