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
- Python 3.9 o superior.
- Git para clonar el repositorio.
- (Opcional) Ollama para ejecutar LLMs open-source localmente.

### Pasos de Instalación
1. Clona el repositorio:
   ```bash
   git clone https://github.com/Salcidoss/asset-parser.git
   cd asset-parser
   ```

2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. (Opcional) Instala spaCy model para NLP:
   ```bash
   python -m spacy download en_core_web_sm
   ```

4. Configura las variables de entorno (ver sección siguiente).

### Verificación de Instalación
Ejecuta las pruebas para verificar que todo funciona correctamente:
```bash
pytest tests/
```
Si todas las pruebas pasan (4/4), la instalación es correcta. También puedes ejecutar un ejemplo simple:
```bash
python main.py --input "Usuario -> Portal Web: login" --output test_output
```
Verifica que se generen `test_output.json`, `test_output.md`, `test_output.mermaid` y `test_output_faltantes.md`.

## Configuración

### Variables de Entorno
El sistema utiliza LLMs para parsing y generación. Para priorizar open-source, recomendamos usar Ollama con modelos como Llama 3 o Mistral. Si no tienes acceso a APIs, usa modelos locales de Hugging Face.

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```bash
# Para Ollama (recomendado para open-source local)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:3b  # O mistral:7b para mejor calidad

# Alternativa: Hugging Face local (sin API keys)
HF_MODEL=microsoft/DialoGPT-medium  # Modelo local para NLP básico

# Si usas APIs (no recomendado para privacidad)
OPENAI_API_KEY=tu_clave_aqui  # Solo si es necesario
```

### Configuración de LLMs Open-Source
1. Instala Ollama: Descárgalo desde [ollama.ai](https://ollama.ai) e instala.
2. Ejecuta un modelo: `ollama run llama3.2:3b`
3. El sistema detectará automáticamente si Ollama está corriendo y usará el modelo configurado.

Si prefieres Hugging Face sin servidor, instala transformers y usa modelos como `microsoft/DialoGPT-medium` para tareas básicas.

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
El sistema genera archivos separados para diferentes propósitos:
- `output.json`: Estructura JSON para validación automática y procesamiento.
- `resumen.md`: Documento Markdown con tablas y descripciones para validación humana.
- `diagrama.mermaid`: Código Mermaid para visualización del diagrama.
- `faltantes.md`: Lista de faltantes e inconsistencias en Markdown.

### Ejemplo de Salida
- **output.json**:
  ```json
  {
    "componentes": ["Portal Web", "API de Autenticación"],
    "actores": ["Usuario"],
    "entidades": ["Cuenta"],
    "flujos": [{"origen": "Usuario", "destino": "Portal Web", "tipo": "solicitud"}]
  }
  ```
- **resumen.md**:
  ```markdown
  # Resumen
  ## Componentes
  | Nombre | Descripción |
  |--------|-------------|
  | Portal Web | Interfaz de usuario |
  ```
- **diagrama.mermaid**:
  ```mermaid
  graph TD; Usuario --> PortalWeb;
  ```
- **faltantes.md**:
  ```markdown
  # Faltantes
  - Falta especificar autenticación.
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