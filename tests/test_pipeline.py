import json
from pathlib import Path

from app.pipeline import run_pipeline


def test_pipeline_parses_text_input(tmp_path):
    input_file = tmp_path / "spec.txt"
    input_file.write_text(
        "actor: Usuario\ncomponente: Portal Web\ncomponente: API de Autenticación\nUsuario --> Portal Web: solicitud\nPortal Web --> API de Autenticación: autenticación",
        encoding="utf-8",
    )
    output_dir = tmp_path / "output"
    result = run_pipeline(input_file, output_dir, diagram_format="mermaid")

    assert "componentes" in result["json_data"]
    assert "Portal Web" in result["json_data"]["componentes"]
    assert "Usuario" in result["json_data"]["actores"]
    assert "diagrama" in result
    assert "graph TD" in result["diagrama"]
    assert result["resumen_md"].startswith("# Resumen de alto nivel")
    assert result["faltantes_md"].startswith("# Información Faltante")


def test_pipeline_parses_mermaid_input(tmp_path):
    input_file = tmp_path / "diagram.mmd"
    input_file.write_text(
        "graph TD\n    A[Usuario] --> B[Portal Web]\n    B --> C[Base de Datos]",
        encoding="utf-8",
    )
    output_dir = tmp_path / "output"
    result = run_pipeline(input_file, output_dir, diagram_format="mermaid")

    assert "Base de Datos" in result["json_data"]["entidades"] or "Base de Datos" in result["json_data"]["componentes"]
    assert len(result["json_data"]["flujos"]) == 2
    assert result["resumen_md"].startswith("# Resumen de alto nivel")
