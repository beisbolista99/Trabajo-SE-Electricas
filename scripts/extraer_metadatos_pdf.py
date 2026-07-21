from __future__ import annotations

import argparse
from pathlib import Path

from common import PENDING, write_yaml


def extract_pdf_metadata(pdf: Path) -> dict[str, object]:
    if not pdf.exists():
        raise FileNotFoundError(pdf)
    if pdf.suffix.lower() != ".pdf":
        raise ValueError("El archivo debe ser PDF.")

    metadata: dict[str, object] = {
        "proyecto": PENDING,
        "subestacion": PENDING,
        "codigo_documento": PENDING,
        "titulo": pdf.stem,
        "revision": PENDING,
        "fecha": PENDING,
        "tipo_documento": PENDING,
        "disciplina": PENDING,
        "estado_documental": PENDING,
        "cantidad_paginas": PENDING,
        "archivo_original": str(pdf),
        "tokens_originales_estimados": PENDING,
        "tokens_documento_compacto": PENDING,
        "reduccion_tokens_porcentaje": PENDING,
        "nivel_confianza": "PENDIENTE",
    }

    try:
        import fitz

        with fitz.open(pdf) as doc:
            metadata["cantidad_paginas"] = doc.page_count
            pdf_meta = doc.metadata or {}
            title = pdf_meta.get("title")
            if title:
                metadata["titulo"] = title
            metadata["pdf_metadata"] = {k: v for k, v in pdf_meta.items() if v}
    except Exception as exc:
        metadata["advertencias"] = [f"No fue posible extraer metadata completa: {exc}"]

    return metadata


def main() -> None:
    parser = argparse.ArgumentParser(description="Extraer metadata basica de PDF.")
    parser.add_argument("--pdf", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    metadata = extract_pdf_metadata(args.pdf)
    if args.output:
        write_yaml(args.output, metadata)
        print(args.output)
    else:
        for key, value in metadata.items():
            print(f"{key}: {value}")


if __name__ == "__main__":
    main()

