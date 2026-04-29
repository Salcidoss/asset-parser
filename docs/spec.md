# Especificación de Ingesta y Parsing de Información Técnica

## 1. Objetivo

Definir los requisitos para un sistema capaz de ingerir, normalizar y parsear información técnica variada: diagramas, descripciones, especificaciones, UML, DFD y texto libre. El sistema debe extraer componentes, flujos de datos, actores y entidades con claridad y consistencia.

## 2. Alcance

El sistema debe soportar:
- Diagramas en formatos textuales o semiestructurados (UML, DFD, BPMN, etc.).
- Descripciones narrativas de sistemas, procesos, servicios e interacciones.
- Especificaciones funcionales y no funcionales.
- Modelos y diagramas definidos en notaciones comunes.

No incluye:
- Renderizado gráfico de diagramas.
- Traducción automática de idiomas.
- Ejecución de modelos.

## 3. Fuentes de entrada

El sistema debe aceptar:
- Texto plano con especificaciones y descripciones.
- Archivos estructurados en formatos comunes (JSON, YAML, XML, Markdown).
- Contenido exportado de herramientas de modelado (PlantUML, Mermaid, etc.).
- Diagramas en texto con notaciones DFD/UML.
- Código Mermaid para diagramas de flujo, secuencia y arquitectura.

## 4. Proceso general

### 4.1 Ingesta

1. Recepción de contenido desde distintas fuentes.
2. Detección del tipo de documento o diagrama.
3. Validación mínima del formato.

### 4.2 Normalización

1. Limpieza de texto (remover ruido, caracteres especiales innecesarios, espacios extra).
2. Homogeneización de notación para facilitar el parseo.
3. Identificación de bloques lógicos: diagramas, secciones, listas, descripciones.

### 4.3 Identificación del formato

Detectar si la entrada corresponde a:
- UML (casos de uso, clases, secuencia, componentes, estados).
- DFD (procesos, flujos, almacenes de datos, terminadores).
- Diagrama de componentes o arquitectura.
- Descripción narrativa.
- Especificación mixta.

### 4.4 Extracción de elementos

Para cada formato, extraer:
- Componentes / módulos / sistemas.
- Entidades de datos y objetos de negocio.
- Actores / usuarios / roles.
- Flujos de datos / interacciones / dependencias.
- Interfaces, entradas y salidas.

## 5. Estructura de salida esperada

El resultado debe ser un modelo intermedio uniforme con las siguientes categorías:

- `componentes`: lista de bloques funcionales o módulos.
- `actores`: usuarios, sistemas externos o roles que interactúan.
- `entidades`: objetos de datos, recursos o repositorios.
- `flujos`: conexiones entre componentes, actores y entidades.
- `servicios`: operaciones clave, interfaces o casos de uso.
- `contexto`: notas adicionales sobre supuestos, restricciones o dependencias.
- `resumen_markdown`: un bloque de Markdown que incluya al menos una descripción de alto nivel más tablas de componentes y de interoperabilidad.
- `faltantes_inconsistencias`: un apartado con información que falta, que parece inconsistente, o sobre la que se debería solicitar más información.
- `diagrama_mermaid`: código Mermaid generado para visualizar la arquitectura identificada.

Ejemplo de salida:

```json
{
  "componentes": ["Portal Web", "API de Autenticación", "Base de Datos"],
  "actores": ["Usuario", "Administrador", "Sistema de Pago"],
  "entidades": ["Cuenta", "Transacción", "Producto"],
  "flujos": [
    {"origen": "Usuario", "destino": "Portal Web", "tipo": "solicitud"},
    {"origen": "API de Autenticación", "destino": "Base de Datos", "tipo": "consulta"}
  ],
  "resumen_markdown": "# Resumen de alto nivel\n\nEste sistema incluye actores y componentes clave y describe sus relaciones de interoperabilidad.\n\n## Actores y Componentes\n| Tipo | Nombre | Descripción |\n|---|---|---|\n| Actor | Usuario | Cliente que interactúa con el portal web |\n| Componente | API de Autenticación | Servicio que valida credenciales |\n| Componente | Base de Datos | Almacena la información de cuentas y transacciones |\n\n## Interoperabilidad\n| Origen | Destino | Tipo |\n|---|---|---|\n| Usuario | Portal Web | Solicitud |\n| Portal Web | API de Autenticación | Llamada de autenticación |\n| API de Autenticación | Base de Datos | Consulta |",
  "faltantes_inconsistencias": [
    "No se especifica el mecanismo de validación de la sesión.",
    "El flujo entre API de Autenticación y Sistema de Pago no está documentado.",
    "Falta definir si la base de datos es relacional o no relacional."
  ],
  "diagrama_mermaid": "graph TD\\n  Usuario --> PortalWeb\\n  PortalWeb --> APIAutenticacion\\n  APIAutenticacion --> BaseDatos"
}
```

## 6. Requisitos funcionales

1. Soportar varios formatos de notación: UML, DFD y texto narrativo.
2. Detectar automáticamente el tipo de documentación.
3. Parsear y mapear componentes, flujos, actores y entidades.
4. Generar una representación estructurada y uniforme.
5. Admitir entradas mixtas (diagramas embebidos en texto descriptivo).
6. Mantener trazabilidad entre la entrada original y los elementos extraídos.
7. Generar siempre un resumen de alto nivel en Markdown con:
   - Una descripción general clara del sistema.
   - Una tabla de actores y componentes descritos por tipo.
   - Una tabla que represente la interoperabilidad entre actores y componentes.

## 7. Requisitos no funcionales

- Precisión: el parser debe minimizar falsos positivos y omitir ruído.
- Robustez: debe tolerar variaciones en estilo y formato.
- Extensibilidad: fácil de adaptar a nuevas notaciones técnicas.
- Rendimiento: procesar documentos de tamaño medio en un tiempo razonable.
- Claridad: la salida debe ser comprensible y utilizable en análisis posteriores.

## 8. Validación

El sistema debe validar:
- Que cada flujo referencie componentes, actores o entidades existentes.
- Que los actores no sean confundidos con entidades de datos.
- Que los componentes principales se identifiquen incluso en descripciones implícitas.
- Que las entidades de datos se extraigan de nombres de objetos, almacenes y mensajes.

## 9. Casos de uso

- Documentar la arquitectura de un sistema a partir de esquemas UML.
- Extraer procesos y responsabilidades desde un DFD.
- Identificar dominios y actores en una especificación narrativa.
- Preparar un modelo de análisis para diseño de software.

## 10. Criterios de éxito

- El sistema identifica correctamente al menos el 90% de componentes y flujos en ejemplos de UML y DFD.
- Las entidades y actores extraídos son coherentes con la descripción del dominio.
- La salida estructurada permite realizar análisis de arquitectura o generación de artefactos.
