
from pydantic import BaseModel, Field, root_validator
from typing import List, Optional, Union, Dict, Any, Literal
import copy
import json

# Para depuración
def print_structure(obj, indent=0):
    """Helper para imprimir la estructura de un objeto recursivamente"""
    indent_str = ' ' * indent
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, (dict, list)):
                print(f"{indent_str}{k}:")
                print_structure(v, indent + 2)
            else:
                print(f"{indent_str}{k}: {v}")
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            if isinstance(item, (dict, list)):
                print(f"{indent_str}[{i}]:")
                print_structure(item, indent + 2)
            else:
                print(f"{indent_str}[{i}]: {item}")
    else:
        print(f"{indent_str}{obj}")

# Definimos tipos literales para garantizar validación correcta
ComponentType = Literal["text", "button", "container", "grid", "input"]

class ComponentSchema(BaseModel):
    id: int
    type: ComponentType
    fill: Optional[str] = None
    text: Optional[str] = None
    
    # Agregar un campo extra para cualquier propiedad adicional
    extra: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        extra = "allow"  # Permitir campos adicionales
        arbitrary_types_allowed = True

class TextComponent(ComponentSchema):
    type: Literal["text"]
    text: str
    color: Optional[str] = None
    font_size: Optional[str] = None
    font_weight: Optional[str] = None
    text_align: Optional[str] = None
    text_decoration: Optional[str] = None

class ButtonComponent(ComponentSchema):
    type: Literal["button"]
    text: str
    background: Optional[str] = None
    hover: Optional[str] = None
    disabled: Optional[bool] = False
    color: Optional[str] = None
    size: Optional[str] = None
    icon: Optional[str] = None

class ContainerComponent(ComponentSchema):
    type: Literal["container"]
    background: Optional[str] = None
    border: Optional[str] = None
    padding: Optional[str] = None
    margin: Optional[str] = None
    children: List[Dict[str, Any]] = Field(default_factory=list)

class GridComponent(ComponentSchema):
    type: Literal["grid"]
    columns: int
    rows: int
    gap: Optional[str] = None
    children: List[Dict[str, Any]] = Field(default_factory=list)

class InputComponent(ComponentSchema):
    type: Literal["input"]
    placeholder: Optional[str] = None
    value: Optional[str] = None
    size: Optional[str] = None
    color: Optional[str] = None
    border: Optional[str] = None
    border_radius: Optional[str] = None
    box_shadow: Optional[str] = None
    disabled: Optional[bool] = False

class ViewSchema(BaseModel):
    name: str
    components: List[Dict[str, Any]] = Field(default_factory=list)
    
    class Config:
        arbitrary_types_allowed = True

class ProjectSchema(BaseModel):
    name: str
    author: str
    layers: List[ViewSchema] = Field(default_factory=list)
    
    class Config:
        arbitrary_types_allowed = True
    
    def model_dump_json(self, **kwargs):
        """Personalizar la serialización a JSON"""
        return json.dumps(self._process_dump(self.dict(**kwargs)), **kwargs)
    
    def dict(self, **kwargs):
        """Personalizar la serialización a diccionario"""
        data = super().dict(**kwargs)
        return self._process_dump(data)
    
    def _process_dump(self, data):
        """Procesar recursivamente el diccionario para manejar componentes anidados"""
        if 'layers' in data:
            for layer in data['layers']:
                if 'components' in layer:
                    layer['components'] = [self._process_component_dict(comp) for comp in layer['components']]
        return data
    
    def _process_component_dict(self, component):
        """Procesar un componente y sus hijos recursivamente"""
        result = component.copy()
        
        # Procesar los hijos si existen
        if 'children' in result:
            result['children'] = [self._process_component_dict(child) for child in result['children']]
        
        # Eliminar campos "extra" innecesarios
        if 'extra' in result and not result['extra']:
            del result['extra']
            
        return result
    
    @root_validator(pre=True)
    def process_components(cls, values):
        """Validador para procesar componentes antes de la validación completa"""
        if 'layers' in values:
            layers = values['layers']
            for i, layer in enumerate(layers):
                if 'components' in layer:
                    components = layer['components']
                    processed_components = []
                    
                    for component in components:
                        processed = cls._process_component_data(component)
                        processed_components.append(processed)
                    
                    layer['components'] = processed_components
        
        return values
    
    @classmethod
    def _process_component_data(cls, data):
        """Procesar un componente basado en su tipo"""
        if not isinstance(data, dict):
            return data
            
        component_type = data.get('type')
        result = copy.deepcopy(data)
        
        # Procesar recursivamente los hijos si existen
        if 'children' in result:
            children = result['children']
            processed_children = []
            
            for child in children:
                processed_child = cls._process_component_data(child)
                processed_children.append(processed_child)
            
            result['children'] = processed_children
        
        # No necesitamos convertir a clases específicas aquí
        # Solo asegurarnos de que la estructura esté bien procesada
        return result
