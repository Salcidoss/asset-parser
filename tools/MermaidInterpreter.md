# Tool: MermaidInterpreter

## Descripción

La herramienta `MermaidInterpreter` es un módulo diseñado para interpretar y parsear diagramas codificados en la sintaxis de Mermaid.js. Esta herramienta extrae elementos estructurales de los diagramas (nodos, conexiones, etiquetas) y los mapea a componentes, actores, entidades y flujos según la especificación definida en `docs/spec.md`.

Es útil para procesar diagramas de flujo, Gantt, secuencia, etc., que representen arquitecturas de sistemas, procesos o interacciones.

## Funcionalidad Principal

- **Parsing de Sintaxis**: Analiza el código Mermaid y construye un AST (Abstract Syntax Tree) interno.
- **Extracción de Elementos**:
  - Nodos: Identifica componentes, actores o entidades.
  - Edges: Extrae flujos de datos o interacciones.
  - Labels: Captura descripciones y tipos.
- **Mapeo a Modelo**: Convierte elementos Mermaid a la estructura JSON definida (componentes, actores, entidades, flujos).
- **Validación**: Verifica sintaxis Mermaid y coherencia con el dominio (ej: diagramas de secuencia para UML).

## Entradas

- **Código Mermaid**: String con el diagrama en formato Mermaid (ej: `graph TD; A-->B;`).
- **Tipo de Diagrama**: Opcional, para guiar el mapeo (flowchart, sequence, etc.).
- **Contexto Adicional**: Texto descriptivo para resolver ambigüedades.

## Salidas

- **Estructura JSON**: Objeto con `componentes`, `actores`, `entidades`, `flujos`, según `docs/spec.md`.
- **Errores**: Lista de problemas de sintaxis o mapeo.
- **Resumen Markdown**: Descripción de alto nivel del diagrama interpretado.

Ejemplo de Salida:

```json
{
  "componentes": ["Nodo A", "Nodo B"],
  "flujos": [
    {"origen": "Nodo A", "destino": "Nodo B", "tipo": "conexión"}
  ],
  "faltantes_inconsistencias": ["Tipo de conexión no especificado"]
}
```

## Implementación Técnica

### Dependencias
- **Librería Mermaid**: Usar `mermaid` para renderizado y parsing (si disponible), o parser custom.
- **NLP Tools**: spaCy o Hugging Face para interpretar labels.
- **Lenguaje**: Python, integrado con LangChain para agentes.

### Algoritmo
1. **Tokenización**: Dividir el código en tokens (nodos, edges, directivas).
2. **Construcción de Grafo**: Crear un grafo dirigido con nodos y aristas.
3. **Mapeo Semántico**:
   - Nodos con labels descriptivos → componentes/actores.
   - Edges con tipos → flujos.
   - Usar IA para inferir roles (ej: nodos externos → actores).
4. **Validación**: Chequear referencias y coherencia.
5. **Generación de Salida**: Formatear a JSON/Markdown.

### Integración con Agentes
- Usado por `ParsingAgent` en `agents/agents.md` para diagramas Mermaid.
- Invocado automáticamente si se detecta sintaxis Mermaid en la entrada.

### Limitaciones
- Soporta diagramas básicos (flowchart, sequence); extensiones para otros tipos.
- No renderiza gráficos, solo extrae estructura.
- Requiere sintaxis correcta; errores de parsing se reportan.

### Ejemplo de Uso
```python
from tools.mermaid_interpreter import MermaidInterpreter

interpreter = MermaidInterpreter()
result = interpreter.parse("""
graph TD;
    A[Usuario] --> B[API];
    B --> C[Base de Datos];
""")
print(result)  # Salida JSON con componentes y flujos
```

Esta tool mejora la capacidad del sistema para manejar diagramas visuales textuales, facilitando la ingesta automática de arquitecturas representadas en Mermaid.