from __future__ import annotations

import argparse
import re
from pathlib import Path

from common import read_text, write_text

HIGH_KEYWORDS = [
    "tabla",
    "formula",
    "resultado",
    "conclusion",
    "diametro",
    "area",
    "ducto",
    "camara",
    "caja",
    "porcentaje",
    "ocupacion",
    "inconsistencia",
]
MEDIUM_KEYWORDS = ["alcance", "antecedente", "norma", "criterio", "objetivo"]


def split_pages(text: str) -> list[tuple[int, str]]:
    matches = list(re.finditer(r"^# Pagina\s+(\d+)\s*$", text, flags=re.MULTILINE | re.IGNORECASE))
    if not matches:
        return [(1, text)]
    pages: list[tuple[int, str]] = []
    for idx, match in enumerate(matches):
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        pages.append((int(match.group(1)), text[start:end].strip()))
    return pages


def classify_page(page_text: str) -> str:
    lower = page_text.lower()
    if any(keyword in lower for keyword in HIGH_KEYWORDS):
        return "ALTA"
    if any(keyword in lower for keyword in MEDIUM_KEYWORDS):
        return "MEDIA"
    return "BAJA"


def generate_index(text_path: Path, output: Path) -> Path:
    pages = split_pages(read_text(text_path))
    lines = ["# Indice tecnico", ""]
    for page_number, page_text in pages:
        priority = classify_page(page_text)
        preview = " ".join(page_text.split())[:180] or "Pagina sin texto extraible"
        lines.append(f"## Pagina {page_number}")
        lines.append(f"- Prioridad: {priority}")
        lines.append(f"- Resumen: {preview}")
        lines.append(f"- Fuente: pagina {page_number}")
        lines.append("")
    write_text(output, "\n".join(lines))
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description="Generar indice tecnico desde texto por pagina.")
    parser.add_argument("--text", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(generate_index(args.text, args.output))


if __name__ == "__main__":
    main()

