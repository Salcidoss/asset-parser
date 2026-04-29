# Sistema de Ingesta y Parsing de Información Técnica

## Descripción

Esta aplicación nace de la necesidad de inventariar y clasificar los activos, actores, componentes y cualquier entidad involucrada en una aplicación a partir de su documentación. La documentación habitualmente consiste en diagramas y descripciones de los componentes, pero muchas veces ni está actualizada ni está documentada en su totalidad.

El sistema analiza los inputs suministrados (texto, diagramas UML/DFD, código Mermaid, etc.) y construye un listado estructurado de activos, sus actores y la interrelación entre ellos. Además, genera un diagrama visual compatible con herramientas como draw.io o Mermaid para representar la arquitectura identificada.

## Características Principales

- **Ingesta Inteligente**: Soporta múltiples formatos de entrada (texto plano, JSON, YAML, diagramas Mermaid, UML, DFD).
- **Parsing con IA**: Utiliza modelos de lenguaje grandes (LLMs) y técnicas de NLP para extraer componentes, actores, entidades y flujos.
- **Clasificación de Activos**: Identifica y clasifica activos por sensibilidad (Public, Internal, Confidential, Critical) y objetivos de protección (CIA).
- **Validación y Coherencia**: Detecta inconsistencias, faltantes y sugiere aclaraciones.
- **Generación de Diagramas**: Produce diagramas Mermaid o XML para draw.io a partir del inventario.
- **Salida Estructurada**: Genera JSON con elementos extraídos, resumen Markdown con tablas, y código de diagrama.

## Arquitectura

El sistema se basa en un pipeline de agentes y herramientas:

- **Agentes**: IngestionAgent, ParsingAgent, ValidationAgent, AssetAgent, OutputAgent (ver `agents/agents.md`).
- **Skills**: skill_AssetIdentification para catalogar activos; skill_DiagramGeneration para visualización (ver `.github/skills/`).
- **Tools**: MermaidInterpreter para parsear diagramas; DiagramGenerator para crear visualizaciones (ver `tools/`).
- **Documentación**: Especificaciones en `docs/spec.md`; arquitectura técnica en `docs/architecture.md`.

## Instalación

### Prerrequisitos
- Python 3.9+
- Dependencias: Instalar con `pip install -r requirements.txt` (LangChain, spaCy, Hugging Face Transformers, etc.).

### Pasos
1. Clona el repositorio: `git clone <url>`
2. Instala dependencias: `pip install -r requirements.txt`
3. Configura variables de entorno (ej: API keys para LLMs).
4. Ejecuta el pipeline: `python main.py --input archivo.txt`

## Uso

### Entrada
- Archivos de texto con descripciones.
- Diagramas en formato Mermaid o DFD/UML.
- JSON/YAML con metadatos.

### Ejemplo de Comando
```bash
python main.py --input spec.txt --output result.json --diagram mermaid
```

### Salida
- `result.json`: Inventario completo con componentes, actores, flujos, faltantes.
- `summary.md`: Resumen con tablas de interoperabilidad.
- `diagram.mmd`: Código Mermaid para el diagrama.

### Ejemplo de Salida JSON
```json
{
  "componentes": ["Portal Web", "API"],
  "actores": ["Usuario"],
  "flujos": [{"origen": "Usuario", "destino": "Portal Web"}],
  "diagrama_mermaid": "graph TD; Usuario --> PortalWeb;"
}
```

## Desarrollo

### Estructura del Proyecto
```
/
├── .github/
│   ├── copilot-instructions.md  # Instrucciones para Copilot
│   └── skills/                  # Skills personalizadas
├── docs/                        # Especificaciones y arquitectura
├── agents/                      # Definición de agentes
├── tools/                       # Herramientas especializadas
├── app/                         # Código principal del pipeline
├── tests/                       # Pruebas unitarias
├── main.py                      # Punto de entrada CLI
├── pyproject.toml               # Configuración del proyecto
├── requirements.txt             # Dependencias
└── .gitignore                   # Archivos ignorados por Git
```

### Contribución
- Reporta issues en GitHub.
- Envía PRs con mejoras.
- Sigue las guías en `docs/architecture.md`.

## Regenerar la aplicación desde IA

La aplicación puede regenerarse utilizando el repositorio y las instrucciones de Copilot en `.github/copilot-instructions.md`.

Pasos sugeridos:
1. Actualiza o modifica `docs/spec.md` y `docs/architecture.md` con los nuevos requisitos.
2. Ajusta el pipeline en `app/` o crea nuevos módulos según la lógica esperada.
3. Ejecuta las pruebas con `pytest`.
4. Revisa `README.md` y `.github/copilot-instructions.md` para mantener la documentación alineada.

## Licencia

MIT License. Ver `LICENSE` para detalles.

## Contacto

Para preguntas, contacta al equipo de desarrollo.