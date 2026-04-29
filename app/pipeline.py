import json
from pathlib import Path
from typing import Dict, List

from app.ingest import load_file
from app.parser import parse_mermaid, parse_text
from app.diagram import generate_mermaid, generate_drawio_xml


def _normalize_list(items: List[str]) -> List[str]:
    return sorted({item.strip() for item in items if item and item.strip()})


def _detect_faltantes(inventory: Dict) -> str:
    faltantes = ["# Información Faltante e Inconsistencias", ""]
    # Lógica básica: si no hay flujos, faltan; si entidades no conectadas, etc.
    if not inventory.get("flujos"):
        faltantes.append("## Faltantes")
        faltantes.append("- No se detectaron flujos de datos. Especificar interacciones entre componentes.")
    if not inventory.get("entidades"):
        faltantes.append("- Falta definición de entidades de datos.")
    # Inconsistencias: componentes mencionados en flujos pero no listados
    mencionados = set()
    for flujo in inventory.get("flujos", []):
        mencionados.add(flujo["origen"])
        mencionados.add(flujo["destino"])
    todos = set(inventory.get("componentes", []) + inventory.get("actores", []) + inventory.get("entidades", []))
    no_listados = mencionados - todos
    if no_listados:
        faltantes.append("## Inconsistencias")
        faltantes.append(f"- Elementos mencionados en flujos pero no catalogados: {', '.join(no_listados)}")
    return "\n".join(faltantes)


def _build_summary(inventory: Dict) -> str:
    header = ["# Resumen de alto nivel", "", "Este sistema incluye actores y componentes clave y describe sus relaciones de interoperabilidad.", ""]
    table = ["## Actores y Componentes", "| Tipo | Nombre | Descripción |", "|---|---|---|"]
    for actor in inventory.get("actores", []):
        table.append(f"| Actor | {actor} | Actor o sistema externo |")
    for component in inventory.get("componentes", []):
        table.append(f"| Componente | {component} | Componente de la solución |")
    table.append("")
    interoperability = ["## Interoperabilidad", "| Origen | Destino | Tipo |", "|---|---|---|"]
    for flujo in inventory.get("flujos", []):
        interoperability.append(f"| {flujo['origen']} | {flujo['destino']} | {flujo['tipo']} |")
    return "\n".join(header + table + ["\n"] + interoperability)


def run_pipeline(input_path: Path, output_dir: Path, diagram_format: str = "mermaid") -> Dict:
    source = load_file(input_path)
    content = source["content"]
    parser = parse_mermaid if source["type"] == "mermaid" else parse_text
    inventory = parser(content)

    inventory["componentes"] = _normalize_list(inventory.get("componentes", []))
    inventory["actores"] = _normalize_list(inventory.get("actores", []))
    inventory["entidades"] = _normalize_list(inventory.get("entidades", []))

    inventory["resumen_markdown"] = _build_summary(inventory)
    if diagram_format == "mermaid":
        inventory["diagrama"] = generate_mermaid(inventory)
    else:
        inventory["diagrama"] = generate_drawio_xml(inventory)

    inventory["dataAssets"] = []
    inventory["componentAssets"] = []
    inventory["credentialAssets"] = []

    if diagram_format == "mermaid":
        inventory["diagrama_mermaid"] = inventory["diagrama"]

    # Generar faltantes
    faltantes = _detect_faltantes(inventory)

    # Datos JSON limpios
    json_data = {
        "componentes": inventory["componentes"],
        "actores": inventory["actores"],
        "entidades": inventory["entidades"],
        "flujos": inventory["flujos"],
        "servicios": inventory.get("servicios", []),
        "contexto": inventory.get("contexto", [])
    }

    return {
        "json_data": json_data,
        "resumen_md": inventory["resumen_markdown"],
        "diagrama": inventory["diagrama"],
        "faltantes_md": faltantes
    }
