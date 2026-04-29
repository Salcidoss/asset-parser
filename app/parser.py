import re
from typing import Dict, List


def _extract_nodes_from_mermaid(text: str) -> Dict[str, str]:
    nodes = {}
    label_pattern = re.compile(r"([A-Za-z0-9_]+)\s*\[([^\]]+)\]")
    for match in label_pattern.finditer(text):
        node_id, label = match.groups()
        nodes[node_id] = label.strip()
    return nodes


def _extract_edges_from_mermaid(text: str) -> List[Dict[str, str]]:
    edges = []
    edge_pattern = re.compile(r"([A-Za-z0-9_]+)\s*--?>+\s*([A-Za-z0-9_]+)(?:\s*:\s*(.*))?")
    for match in edge_pattern.finditer(text):
        origen, destino, label = match.groups()
        edges.append({
            "origen": origen,
            "destino": destino,
            "tipo": (label or "flujo").strip(),
        })
    return edges


def parse_mermaid(content: str) -> Dict[str, List[Dict[str, str]]]:
    nodes = _extract_nodes_from_mermaid(content)
    edges = _extract_edges_from_mermaid(content)

    activos = []
    actores = []
    entidades = []
    for label in nodes.values():
        clean = label.strip()
        if any(term in clean.lower() for term in ["usuario", "cliente", "sistema"]):
            actores.append(clean)
        elif any(term in clean.lower() for term in ["base de datos", "tabla", "almacén", "store"]):
            entidades.append(clean)
        else:
            activos.append(clean)

    flujos = [
        {
            "origen": nodes.get(edge["origen"], edge["origen"]),
            "destino": nodes.get(edge["destino"], edge["destino"]),
            "tipo": edge["tipo"],
        }
        for edge in edges
    ]

    return {
        "componentes": activos,
        "actores": actores,
        "entidades": entidades,
        "flujos": flujos,
        "data_assets": [],
        "component_assets": [],
        "credential_assets": [],
        "faltantes_inconsistencias": [],
    }


def parse_text(content: str) -> Dict[str, List[Dict[str, str]]]:
    lines = [line.strip() for line in content.splitlines() if line.strip()]
    componentes = []
    actores = []
    entidades = []
    flujos = []

    for line in lines:
        if line.lower().startswith("actor:"):
            actores.append(line.split(":", 1)[1].strip())
        elif line.lower().startswith("componente:"):
            componentes.append(line.split(":", 1)[1].strip())
        elif line.lower().startswith("entidad:"):
            entidades.append(line.split(":", 1)[1].strip())
        elif "->" in line or "-->" in line:
            parts = re.split(r"--?>+", line)
            origen = parts[0].strip()
            destino = parts[1].strip() if len(parts) > 1 else ""
            tipo = "flujo"
            if ":" in destino:
                destino, tipo = [token.strip() for token in destino.split(":", 1)]
            flujos.append({"origen": origen, "destino": destino, "tipo": tipo})

    return {
        "componentes": componentes,
        "actores": actores,
        "entidades": entidades,
        "flujos": flujos,
        "data_assets": [],
        "component_assets": [],
        "credential_assets": [],
        "faltantes_inconsistencias": [],
    }
