# Definición de Agentes

Este documento define los agentes utilizados en el sistema de ingesta y parsing de información técnica. Los agentes son componentes autónomos que ejecutan tareas específicas utilizando skills y herramientas de IA.

## 1. Agente de Ingesta (IngestionAgent)

- **Propósito**: Recibir y preprocesar entradas de diversos formatos.
- **Skills utilizados**: Ninguno específico (usa herramientas estándar de procesamiento de texto).
- **Entradas**: Archivos de texto, diagramas, especificaciones.
- **Salidas**: Contenido normalizado listo para parsing.
- **Comportamiento**: Detecta formato, limpia texto, segmenta en bloques.

## 2. Agente de Parsing (ParsingAgent)

- **Propósito**: Extraer componentes, actores, entidades y flujos de la información procesada.
- **Skills utilizados**: Técnicas de NLP, NER, relación extraction.
- **Tools utilizadas**: MermaidInterpreter (para diagramas Mermaid).
- **Entradas**: Texto normalizado, diagramas Mermaid.
- **Salidas**: Estructura JSON intermedia con elementos extraídos.
- **Comportamiento**: Usa LLMs para identificar patrones y conectar piezas coherentemente; invoca MermaidInterpreter para diagramas específicos.

## 3. Agente de Validación (ValidationAgent)

- **Propósito**: Verificar coherencia, detectar inconsistencias y faltantes.
- **Skills utilizados**: Reglas heurísticas, validación cruzada.
- **Entradas**: Estructura JSON intermedia.
- **Salidas**: Lista de faltantes/inconsistencias, estructura validada.
- **Comportamiento**: Aplica reglas determinísticas y IA para asegurar calidad.

## 4. Agente de AssetIdentification (AssetAgent)

- **Propósito**: Identificar y clasificar activos en sistemas basados en descripciones técnicas.
- **Skills utilizados**: skill_AssetIdentification (ver .github/skills/skill_AssetIdentification.md).
- **Entradas**: Descripciones de sistema, diagramas de flujo de datos.
- **Salidas**: Inventario de activos JSON, matriz de clasificación Markdown, evaluación de confianza.
- **Comportamiento**: Cataloga datos, componentes y credenciales; asigna clasificaciones de sensibilidad y objetivos de protección.

## 5. Agente de Salida (OutputAgent)

- **Propósito**: Generar salidas finales en formatos requeridos.
- **Skills utilizados**: Generación de texto, formateo; skill_DiagramGeneration para diagramas.
- **Tools utilizadas**: DiagramGenerator.
- **Entradas**: Estructura validada, inventario de activos.
- **Salidas**: JSON completo, resumen Markdown, lista de faltantes, diagramas Mermaid/draw.io.
- **Comportamiento**: Formatea resultados según spec.md; genera diagramas visuales.

## Integración

Los agentes operan en secuencia en un pipeline:
IngestionAgent → ParsingAgent → ValidationAgent → OutputAgent

AssetAgent puede operar independientemente o integrarse para análisis de activos en sistemas parseados.

Utilizan tools especializadas como MermaidInterpreter y DiagramGenerator para formatos específicos (ver tools/). Skills como skill_DiagramGeneration permiten generación de diagramas.

## Configuración

- Cada agente puede configurarse con modelos de IA específicos (ej: GPT-4 para parsing).
- Usan herramientas como LangChain para orquestación.
- Monitoreo de confianza y calidad en cada paso.