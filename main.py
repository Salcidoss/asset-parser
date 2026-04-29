import argparse
import json
from pathlib import Path
from app.pipeline import run_pipeline


def parse_args():
    parser = argparse.ArgumentParser(
        description="Ingest documentation, identify assets, and generate diagrams."
    )
    parser.add_argument("--input", "-i", required=True, help="Input file or directory with documentation")
    parser.add_argument("--output", "-o", default="output", help="Output directory")
    parser.add_argument("--format", "-f", choices=["mermaid", "drawio"], default="mermaid", help="Diagram format")
    return parser.parse_args()


def main():
    args = parse_args()
    input_path = Path(args.input)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    result = run_pipeline(input_path, output_dir, diagram_format=args.format)

    # output.json
    json_path = output_dir / "output.json"
    json_path.write_text(json.dumps(result["json_data"], indent=2, ensure_ascii=False), encoding="utf-8")

    # resumen.md
    summary_path = output_dir / "resumen.md"
    summary_path.write_text(result["resumen_md"], encoding="utf-8")

    # diagrama.mermaid o .xml
    diagram_ext = "mermaid" if args.format == "mermaid" else "xml"
    diagram_path = output_dir / f"diagrama.{diagram_ext}"
    diagram_path.write_text(result["diagrama"], encoding="utf-8")

    # faltantes.md
    faltantes_path = output_dir / "faltantes.md"
    faltantes_path.write_text(result["faltantes_md"], encoding="utf-8")

    print(f"Outputs written to {output_dir.resolve()}")


if __name__ == "__main__":
    main()
