from __future__ import annotations

import argparse
from pathlib import Path

from common import write_text


def extract_text_by_page(pdf: Path) -> list[str]:
    if not pdf.exists():
        raise FileNotFoundError(pdf)
    if pdf.suffix.lower() != ".pdf":
        raise ValueError("El archivo debe ser PDF.")

    try:
        import fitz

        with fitz.open(pdf) as doc:
            return [page.get_text("text").strip() for page in doc]
    except Exception:
        from pypdf import PdfReader

        reader = PdfReader(str(pdf))
        return [(page.extract_text() or "").strip() for page in reader.pages]


def write_text_by_page(pdf: Path, output: Path) -> Path:
    pages = extract_text_by_page(pdf)
    chunks = []
    for index, text in enumerate(pages, start=1):
        body = text if text else "PENDIENTE DE VALIDAR: pagina sin texto extraible."
        chunks.append(f"# Pagina {index}\n\n{body}\n")
    write_text(output, "\n".join(chunks))
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description="Extraer texto de PDF por pagina.")
    parser.add_argument("--pdf", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(write_text_by_page(args.pdf, args.output))


if __name__ == "__main__":
    main()

