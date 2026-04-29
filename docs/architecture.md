# Arquitectura Técnica del Sistema de Ingesta y Parsing

## 1. Visión General

Esta arquitectura define cómo un sistema basado en IA construye piezas coherentes a partir de información técnica variada. El enfoque se basa en un pipeline de procesamiento que combina técnicas de procesamiento de lenguaje natural (NLP), reglas heurísticas y validación cruzada para extraer y conectar componentes, actores, entidades y flujos de manera consistente.

El sistema utiliza modelos de lenguaje grandes (LLMs) como núcleo para interpretar texto, detectar patrones y generar conexiones lógicas, complementado con reglas determinísticas para asegurar coherencia y trazabilidad.

## 2. Arquitectura Conceptual

```
[Entrada] → [Ingesta] → [Normalización] → [Detección de Formato] → [Extracción IA] → [Validación y Coherencia] → [Salida Estructurada]
```

### Componentes Principales:

- **Módulo de Ingesta**: Recepción y preprocesamiento inicial de datos.
- **Normalizador**: Limpieza y homogeneización de texto.
- **Detector de Formato**: Clasificación automática del tipo de documento/diagrama.
- **Extractor IA**: Uso de LLMs para identificar y extraer elementos clave.
- **Validador de Coherencia**: Aplicación de reglas para conectar piezas y detectar inconsistencias.
- **Generador de Salida**: Formateo de resultados en JSON y Markdown.
- **Tools Especializadas**: MermaidInterpreter para parsing de diagramas Mermaid; DiagramGenerator para generación de diagramas.
- **Skills**: skill_AssetIdentification para inventarios; skill_DiagramGeneration para visualización.

## 3. Flujo de Procesamiento Detallado

### 3.1 Ingesta y Preprocesamiento

1. **Recepción de Entrada**: Aceptar texto plano, archivos estructurados o diagramas textuales.
2. **Detección de Codificación**: Identificar UTF-8, ASCII, etc., y convertir si necesario.
3. **Segmentación**: Dividir el contenido en bloques lógicos (secciones, diagramas, párrafos).

### 3.2 Normalización

1. **Limpieza de Texto**: Remover caracteres especiales, normalizar espacios, corregir errores comunes.
2. **Homogeneización de Notación**: Convertir variaciones de UML/DFD a un formato estándar interno.
3. **Tokenización**: Preparar texto para análisis NLP.

### 3.3 Detección de Formato

Utilizar un clasificador basado en IA (fine-tuned LLM o modelo de clasificación) para identificar:
- UML: Buscar patrones como "class", "use case", "extends", diagramas de secuencia.
- DFD: Identificar "process", "data store", "external entity", flujos con flechas.
- Narrativo: Texto descriptivo sin notación formal.
- Mixto: Combinaciones de los anteriores.

### 3.4 Extracción de Elementos con IA

**Técnicas de IA utilizadas:**

- **Named Entity Recognition (NER)**: Identificar actores, componentes y entidades usando modelos pre-entrenados (spaCy, Hugging Face).
- **Relación Extraction**: Detectar conexiones entre elementos mediante prompts a LLMs.
- **Template Matching**: Usar prompts estructurados para extraer información específica por formato.

**Prompts clave para coherencia:**

- Para UML: "Extrae clases, relaciones de herencia y asociaciones del siguiente diagrama UML."
- Para DFD: "Identifica procesos, almacenes de datos y flujos en este diagrama DFD."
- Para narrativo: "Lista los actores, componentes y sus interacciones descritas en este texto."

**Construcción de Coherencia:**
- **Referencia Cruzada**: Verificar que cada flujo mencione elementos ya extraídos.
- **Resolución de Ambigüedades**: Usar contexto para distinguir actores de entidades (ej: "Usuario" es actor, "Cuenta de Usuario" es entidad).
- **Inferencia Lógica**: Si un componente A llama a B, inferir dependencias implícitas.

### 3.5 Validación y Coherencia

**Reglas Determinísticas:**
- Cada flujo debe tener origen y destino válidos.
- Actores no pueden ser entidades de datos.
- Componentes deben tener al menos una interacción.

**Validación IA:**
- Usar LLM para verificar consistencia narrativa: "¿Esta descripción es coherente con los elementos extraídos?"
- Detectar faltantes: "¿Qué información adicional se necesita para completar este flujo?"

**Detección de Inconsistencias:**
- Flujos sin componentes referenciados.
- Descripciones contradictorias.
- Elementos mencionados pero no definidos.

### 3.6 Generación de Salida

1. **Estructuración JSON**: Mapear elementos extraídos a la estructura definida en spec.md.
2. **Generación Markdown**: Usar LLM para crear descripciones naturales y tablas.
3. **Lista de Faltantes**: Compilar hallazgos de validación.

## 4. Técnicas de IA para Construir Coherencia

### 4.1 Procesamiento de Lenguaje Natural
- **Modelos**: GPT-4, Claude, o modelos open-source como Llama para parsing.
- **Técnicas**: Zero-shot learning para formatos no vistos, few-shot para ejemplos específicos.

### 4.2 Reglas y Heurísticas
- **Diccionarios**: Listas de términos comunes para actores (Usuario, Administrador), componentes (API, Base de Datos).
- **Patrones**: Regex para detectar flujos (ej: "A → B: mensaje").
- **Validación Lógica**: Reglas como "si existe flujo A→B, entonces A y B deben existir".

### 4.3 Aprendizaje Continuo
- **Feedback Loop**: Incorporar correcciones humanas para mejorar el modelo.
- **Fine-tuning**: Entrenar en datasets específicos de UML/DFD para mayor precisión.

## 5. Tecnologías y Herramientas

- **Lenguaje Principal**: Python 3.9+
- **Frameworks de IA**:
  - LangChain: Para orquestar LLMs y crear pipelines.
  - Hugging Face Transformers: Para NER y clasificación.
  - spaCy: Para tokenización y análisis sintáctico.
- **Procesamiento de Texto**: NLTK, regex para reglas determinísticas.
- **Validación**: Pydantic para esquemas JSON.
- **Almacenamiento**: JSON/YAML para configuraciones, SQLite para trazabilidad.
- **Despliegue**: FastAPI para APIs REST, Docker para contenedorización.

## 6. Consideraciones de Calidad y Escalabilidad

### 6.1 Calidad
- **Métricas**: Precisión >90% en extracción, recall para elementos faltantes.
- **Testing**: Datasets de UML/DFD sintéticos y reales para validación.
- **Monitoreo**: Logs de decisiones IA para debugging.

### 6.2 Escalabilidad
- **Procesamiento Paralelo**: Usar async/await para múltiples entradas.
- **Caché**: Almacenar resultados intermedios para entradas similares.
- **Optimización**: Cuantización de modelos para menor uso de memoria.

### 6.3 Seguridad
- **Validación de Entrada**: Sanitizar texto para prevenir inyección.
- **Privacidad**: No almacenar datos sensibles, procesar localmente si posible.

## 7. Integración con Especificación

Esta arquitectura implementa directamente los requisitos de `spec.md`:
- Soporte a múltiples formatos mediante clasificadores IA.
- Extracción coherente usando NER y relación extraction.
- Validación cruzada para asegurar trazabilidad.
- Salida estructurada con JSON y Markdown.
- Detección de faltantes para completar información.

El sistema es extensible: nuevos formatos se añaden fine-tuning modelos o reglas adicionales.