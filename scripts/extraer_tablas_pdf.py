from __future__ import annotations

import argparse
from pathlib import Path

from common import write_text


def extract_tables(pdf: Path, output: Path) -> Path:
    if not pdf.exists():
        raise FileNotFoundError(pdf)
    if pdf.suffix.lower() != ".pdf":
        raise ValueError("El archivo debe ser PDF.")

    lines = ["# Tablas extraidas", ""]
    try:
        import pdfplumber

        with pdfplumber.open(str(pdf)) as doc:
            for page_number, page in enumerate(doc.pages, start=1):
                tables = page.extract_tables() or []
                for table_index, table in enumerate(tables, start=1):
                    lines.append(f"## Pagina {page_number} - Tabla {table_index}")
                    for row in table:
                        safe_row = [str(cell or "").replace("\n", " ").strip() for cell in row]
                        lines.append("| " + " | ".join(safe_row) + " |")
                    lines.append("")
        if len(lines) == 2:
            lines.append("PENDIENTE DE VALIDAR: no se detectaron tablas extraibles automaticamente.")
    except Exception as exc:
        lines.append(f"PENDIENTE DE VALIDAR: no fue posible extraer tablas automaticamente. Detalle: {exc}")

    write_text(output, "\n".join(lines) + "\n")
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description="Extraer tablas de PDF a Markdown.")
    parser.add_argument("--pdf", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(extract_tables(args.pdf, args.output))


if __name__ == "__main__":
    main()

