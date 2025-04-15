import React from "react"
import { styled } from "baseui"
import { Theme } from "baseui/theme"
import Icons from "~/components/Icons"
import { Button, KIND, SIZE } from "baseui/button"
import { Slider } from "baseui/slider"
import { Input } from "baseui/input"
import { useEditor, useZoomRatio } from "@layerhub-io/react"
import useAppContext from "~/hooks/useAppContext"
import useSetIsSidebarOpen from "~/hooks/useSetIsSidebarOpen"
import useIsSidebarOpen from "~/hooks/useIsSidebarOpen"
import panelItems from "../../Panels/panelItems"

const Container = styled<"div", {}, Theme>("div", ({ $theme }) => ({
  height: "50px",
  background: $theme.colors.white,
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
}))

interface Options {
  zoomRatio: number
}

const Common = () => {
  const zoomMin = 10
  const zoomMax = 240
  const [options, setOptions] = React.useState<Options>({
    zoomRatio: 20,
  })
  const editor = useEditor()
  const zoomRatio: number = useZoomRatio()
  const previousZoomRef = React.useRef(zoomRatio);
  const { activePanel, setActivePanel, activeSubMenu, setActiveSubMenu } = useAppContext();
  const setIsSidebarOpen = useSetIsSidebarOpen()
  const isSidebarOpen = useIsSidebarOpen()

  React.useEffect(() => {
    setOptions({ ...options, zoomRatio: Math.round(zoomRatio * 100) })

    if (editor && Math.abs(previousZoomRef.current - zoomRatio) > 0.001) {
      const container = document.querySelector('.layerhub-canvas-container');
      
      if (container) {
        // Calcular el centro actual del viewport
        const scrollLeft = container.scrollLeft;
        const scrollTop = container.scrollTop;
        const viewportWidth = container.clientWidth;
        const viewportHeight = container.clientHeight;
        
        const centerX = scrollLeft + viewportWidth / 2;
        const centerY = scrollTop + viewportHeight / 2;
        
        // Calcular el factor de escala entre el zoom anterior y el actual
        const scaleFactor = zoomRatio / previousZoomRef.current;
        
        // Calcular la nueva posición de desplazamiento para mantener el centro
        const newScrollLeft = centerX * scaleFactor - viewportWidth / 2;
        const newScrollTop = centerY * scaleFactor - viewportHeight / 2;
        
        // Aplicar el desplazamiento
        requestAnimationFrame(() => {
          container.scrollLeft = newScrollLeft;
          container.scrollTop = newScrollTop;
        });
      }
    }
    previousZoomRef.current = zoomRatio;

  }, [zoomRatio])

  const handleChange = (type: string, value: any) => {
    if (value < 0) {
      editor.zoom.zoomToRatio(zoomMin / 100)
    } else if (value > zoomMax) {
      editor.zoom.zoomToRatio(zoomMax / 100)
    } else {
      editor.zoom.zoomToRatio(value / 100)
    }
  }

  const handleLayersMenu = () => {
    if (!isSidebarOpen) {
      setIsSidebarOpen(true)
    }
    setActiveSubMenu("Layers");
  }

  return (
    <Container>
      <div>
        <Button kind={KIND.tertiary} size={SIZE.compact} onClick={() => handleLayersMenu()}>
          <Icons.Layers size={20} />
        </Button>
      </div>
      <div style={{ display: "flex", alignItems: "center", justifyContent: "center" }}>
        <Button kind={KIND.tertiary} size={SIZE.compact}>
          <Icons.Expand size={16} />
        </Button>
        <Button kind={KIND.tertiary} size={SIZE.compact}>
          <Icons.Compress size={16} />
        </Button>
        <Button kind={KIND.tertiary} size={SIZE.compact} onClick={() => editor.zoom.zoomOut()}>
          <Icons.RemoveCircleOutline size={24} />
        </Button>
        <Slider
          overrides={{
            InnerThumb: () => null,
            ThumbValue: () => null,
            TickBar: () => null,
            Root: {
              style: { width: "140px" },
            },
            Thumb: {
              style: {
                height: "12px",
                width: "12px",
                paddingLeft: 0,
              },
            },
            Track: {
              style: {
                paddingLeft: 0,
                paddingRight: 0,
              },
            },
          }}
          value={[options.zoomRatio]}
          onChange={({ value }) => {
            handleChange("zoomRatio", value[0])
          }}
          min={zoomMin}
          max={zoomMax}
        />
        <Button kind={KIND.tertiary} size={SIZE.compact} onClick={() => editor.zoom.zoomIn()}>
          <Icons.AddCircleOutline size={24} />
        </Button>
        <Input
          type="number"
          value={options.zoomRatio}
          endEnhancer="%"
          overrides={{
            Root: {
              style: {
                width: "96px",
              },
            },
          }}
          size={SIZE.mini}
          max={zoomMax}
          min={zoomMin}
          onChange={(e: any) => handleChange("zoomRatio", e.target.value)}
        />
      </div>
      <div style={{ display: "flex", alignItems: "center", justifyContent: "end" }}>
        <Button kind={KIND.tertiary} size={SIZE.compact}>
          <Icons.Refresh size={16} />
        </Button>
        <Button kind={KIND.tertiary} size={SIZE.compact}>
          <Icons.Undo size={22} />
        </Button>
        <Button kind={KIND.tertiary} size={SIZE.compact}>
          <Icons.Redo size={22} />
        </Button>
        <Button kind={KIND.tertiary} size={SIZE.compact}>
          <Icons.TimePast size={16} />
        </Button>
      </div>
    </Container>
  )
}

export default Common
