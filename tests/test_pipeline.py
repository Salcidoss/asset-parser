import json
from pathlib import Path

from app.pipeline import run_pipeline


def test_pipeline_parses_text_input(tmp_path):
    input_file = tmp_path / "spec.txt"
    input_file.write_text(
        "actor: Usuario\ncomponente: Portal Web\ncomponente: API de Autenticación\nUsuario --> Portal Web: solicitud\nPortal Web --> API de Autenticación: autenticación\",
        encoding="utf-8",
    )
    output_dir = tmp_path / "output"
    result = run_pipeline(input_file, output_dir, diagram_format="mermaid")

    assert "componentes" in result
    assert "Portal Web" in result["componentes"]
    assert "Usuario" in result["actores"]
    assert "diagrama" in result
    assert "graph TD" in result["diagrama"]


def test_pipeline_parses_mermaid_input(tmp_path):
    input_file = tmp_path / "diagram.mmd"
    input_file.write_text(
        "graph TD\n    A[Usuario] --> B[Portal Web] --> C[Base de Datos]",
        encoding="utf-8",
    )
    output_dir = tmp_path / "output"
    result = run_pipeline(input_file, output_dir, diagram_format="mermaid")

    assert "Base de Datos" in result["entidades"] or "Base de Datos" in result["componentes"]
    assert any(f["tipo"] == "flujo" for f in result["flujos"])
    assert result["resumen_markdown"].startswith("# Resumen de alto nivel")
