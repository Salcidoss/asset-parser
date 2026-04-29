from typing import Dict, List


def generate_mermaid(inventory: Dict) -> str:
    lines = ["graph TD"]
    nodes = set()
    node_map = {}

    for nombre in inventory.get("actores", []) + inventory.get("componentes", []) + inventory.get("entidades", []):
        key = _safe_id(nombre)
        node_map[nombre] = key
        nodes.add(f"    {key}[{nombre}]")

    for flujo in inventory.get("flujos", []):
        origen = node_map.get(flujo["origen"], _safe_id(flujo["origen"]))
        destino = node_map.get(flujo["destino"], _safe_id(flujo["destino"]))
        nodes.add(f"    {origen}[{flujo['origen']}]")
        nodes.add(f"    {destino}[{flujo['destino']}]")
        lines.append(f"    {origen} --> {destino} : {flujo['tipo']}")

    lines = list(nodes) + lines
    return "\n".join(lines)


def generate_drawio_xml(inventory: Dict) -> str:
    cells = [
        '<mxCell id="0"/>',
        '<mxCell id="1" parent="0"/>'
    ]
    index = 2
    positioned = []
    for nombre in inventory.get("actores", []) + inventory.get("componentes", []) + inventory.get("entidades", []):
        cell = (
            f'<mxCell id="{index}" value="{nombre}" style="rounded=1;whiteSpace=wrap;html=1;" '
            f'vertex="1" parent="1">'
            f'<mxGeometry x="{(index-2)*160}" y="{(index-2)//4*120}" width="140" height="60" as="geometry"/>'
            '</mxCell>'
        )
        cells.append(cell)
        positioned.append((nombre, str(index)))
        index += 1

    for flujo in inventory.get("flujos", []):
        origen_id = _find_cell_id(positioned, flujo["origen"])
        destino_id = _find_cell_id(positioned, flujo["destino"])
        if origen_id and destino_id:
            cells.append(
                f'<mxCell id="{index}" style="edgeStyle=orthogonalEdgeStyle;rounded=0;" '
                f'edge="1" source="{origen_id}" target="{destino_id}" parent="1">'
                f'<mxGeometry relative="1" as="geometry"/> '
                '</mxCell>'
            )
            index += 1

    xml = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<mxfile host="app.diagrams.net">',
        '  <diagram id="diagram-1" name="Page-1">',
        '    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="850" pageHeight="1100" math="0" shadow="0">',
        '      <root>',
    ]
    xml.extend([f"        {cell}" for cell in cells])
    xml.extend([
        '      </root>',
        '    </mxGraphModel>',
        '  </diagram>',
        '</mxfile>',
    ])
    return "\n".join(xml)


def _safe_id(text: str) -> str:
    return ''.join(ch if ch.isalnum() else '_' for ch in text)


def _find_cell_id(positioned: List, label: str) -> str:
    for nombre, cell_id in positioned:
        if nombre == label:
            return cell_id
    return ""
