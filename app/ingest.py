from pathlib import Path
from typing import Dict


SUPPORTED_EXTENSIONS = {"txt", "md", "json", "yaml", "yml", "mmd"}


def load_file(path: Path) -> Dict[str, str]:
    if path.is_dir():
        raise ValueError("Expected a file path, not a directory.")

    suffix = path.suffix.lower().strip(".")
    if suffix not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file extension: {suffix}")

    content = path.read_text(encoding="utf-8")
    file_type = "mermaid" if content.strip().startswith(("graph", "sequenceDiagram")) else "text"
    return {"content": content, "type": file_type, "path": str(path)}
