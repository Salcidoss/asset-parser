# GitHub Copilot Instructions

## Propósito

Este repositorio contiene una aplicación que ingesta documentación técnica, identifica activos, actores, componentes y relaciones, y genera diagramas compatibles con Mermaid y draw.io.

## Uso Esperado de Copilot

Copilot debe ayudar a:
- Extender la lógica de ingestión para nuevos formatos de entrada.
- Mejorar el parseo de texto y diagramas mediante heurísticas y prompts.
- Añadir validaciones adicionales y pruebas unitarias.
- Generar documentación y actualizar los archivos `README.md`, `docs/` y `agents/`.

## Archivos clave

- `main.py`: punto de entrada CLI.
- `app/`: implementación de ingestión, parseo y generación.
- `tests/`: pruebas unitarias.
- `docs/spec.md`: especificación del proyecto.
- `docs/architecture.md`: arquitectura técnica.
- `.github/skills/`: skills específicas para el proyecto.
- `tools/`: definición de herramientas especializadas.

## Recomendaciones para Copilot

- Mantener la consistencia con la estructura actual del pipeline.
- Usar `pytest` para validar nuevos cambios.
- Asegurarse de que los nuevos módulos respeten el modelo de salida JSON con `resumen_markdown`, `faltantes_inconsistencias` y `diagrama_mermaid`.
- Documentar nuevas features en `README.md` y `docs/`.
