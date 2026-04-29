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

    json_path = output_dir / "result.json"
    json_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")

    summary_path = output_dir / "summary.md"
    summary_md = result.get("resumen_markdown", "")
    summary_path.write_text(summary_md, encoding="utf-8")

    diagram_path = output_dir / ("diagram.mmd" if args.format == "mermaid" else "diagram.xml")
    diagram_path.write_text(result.get("diagrama", ""), encoding="utf-8")

    print(f"Outputs written to {output_dir.resolve()}")


if __name__ == "__main__":
    main()
