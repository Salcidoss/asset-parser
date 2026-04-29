# Tool: DiagramGenerator

## Descripción

La herramienta `DiagramGenerator` toma un inventario de activos (producido por el skill de AssetIdentification) y genera un diagrama visual representando la arquitectura del sistema. El diagrama se genera en formato Mermaid (para compatibilidad con herramientas como draw.io, GitHub, etc.) o XML para draw.io nativo.

Esta tool mapea componentes, actores, entidades y flujos a elementos visuales: nodos para activos, conexiones para interacciones.

## Funcionalidad Principal

- **Mapeo de Activos**: Convierte dataAssets, componentAssets, credentialAssets a nodos con etiquetas y estilos.
- **Generación de Conexiones**: Basado en dependencias y flujos, crea edges entre nodos.
- **Estilos y Layout**: Aplica colores y formas según clasificación (ej: rojo para críticos).
- **Formato de Salida**: Mermaid por defecto; opcional XML para draw.io.

## Entradas

- **Inventario JSON**: Estructura con dataAssets[], componentAssets[], credentialAssets[] (de AssetIdentification).
- **Opciones**: Tipo de diagrama (flowchart, architecture), formato de salida (Mermaid/XML).
- **Contexto**: Descripciones adicionales para etiquetas.

## Salidas

- **Código Mermaid**: String con diagrama (ej: `graph TD; A[Componente] --> B[Base de Datos];`).
- **Archivo XML**: Para importación directa en draw.io.
- **Errores**: Lista de problemas en el mapeo.

Ejemplo de Salida Mermaid:

```
graph TD
    A[Usuario] --> B[API de Autenticación]
    B --> C[Base de Datos]
    style C fill:#f96
```

## Implementación Técnica

### Dependencias
- **Librerías**: Python con templates para Mermaid; xml.etree para draw.io XML.
- **IA**: Opcional, usar LLM para optimizar layout y etiquetas.

### Algoritmo
1. **Parseo de Inventario**: Leer JSON y extraer activos.
2. **Construcción de Grafo**: Crear nodos y edges basados en dependencias.
3. **Aplicación de Estilos**: Asignar colores por clasificación (Public: verde, Critical: rojo).
4. **Generación de Código**: Usar templates para output Mermaid o XML.

### Integración con Agentes
- Usado por agentes de salida o visualización.
- Invocado después de AssetIdentification para representar gráficamente el inventario.

### Limitaciones
- Diagramas simples; no soporta layouts complejos automáticamente.
- Requiere inventario válido; errores se reportan.

### Ejemplo de Uso
```python
from tools.diagram_generator import DiagramGenerator

generator = DiagramGenerator()
mermaid_code = generator.generate(inventory_json, format='mermaid')
print(mermaid_code)
```

Esta tool facilita la visualización de arquitecturas identificadas, compatible con draw.io y Mermaid.