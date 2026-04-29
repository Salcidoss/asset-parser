from app.diagram import generate_mermaid, generate_drawio_xml


def test_generate_mermaid_contains_nodes_and_edges():
    inventory = {
        "actores": ["Usuario"],
        "componentes": ["API"],
        "entidades": ["Base de Datos"],
        "flujos": [{"origen": "Usuario", "destino": "API", "tipo": "solicitud"}],
    }
    mermaid = generate_mermaid(inventory)
    assert "graph TD" in mermaid
    assert "Usuario" in mermaid
    assert "API" in mermaid
    assert "-->" in mermaid


def test_generate_drawio_xml_outputs_xml():
    inventory = {
        "actores": ["Usuario"],
        "componentes": ["API"],
        "entidades": ["Base de Datos"],
        "flujos": [{"origen": "Usuario", "destino": "API", "tipo": "solicitud"}],
    }
    xml = generate_drawio_xml(inventory)
    assert xml.strip().startswith("<?xml")
    assert "mxGraphModel" in xml
    assert "Usuario" in xml
