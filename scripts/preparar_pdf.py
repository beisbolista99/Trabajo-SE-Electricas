from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from common import ensure_project_dir, safe_slug, write_text, write_yaml
from extraer_metadatos_pdf import extract_pdf_metadata


def prepare_pdf(pdf: Path, project: Path, codigo: str) -> Path:
    project = ensure_project_dir(project)
    if not pdf.exists():
        raise FileNotFoundError(pdf)
    if pdf.suffix.lower() != ".pdf":
        raise ValueError("El archivo de entrada debe ser PDF.")

    code = safe_slug(codigo)
    out_dir = project / "02_extracciones" / "documentos_compactos" / code
    out_dir.mkdir(parents=True, exist_ok=True)
    original_copy = out_dir / "original.pdf"
    if original_copy.exists():
        raise FileExistsError(f"No se sobrescribe original existente: {original_copy}")

    shutil.copy2(pdf, original_copy)
    metadata = extract_pdf_metadata(original_copy)
    metadata["codigo_documento"] = code
    metadata["archivo_original"] = "original.pdf"
    write_yaml(out_dir / "metadata.yaml", metadata)
    write_text(out_dir / "referencias_cruzadas.md", "# Referencias cruzadas\n\nPENDIENTE DE VALIDAR.\n")
    write_text(out_dir / "inconsistencias_detectadas.md", "# Inconsistencias detectadas\n\nPENDIENTE DE VALIDAR.\n")
    return out_dir


def main() -> None:
    parser = argparse.ArgumentParser(description="Copiar PDF a zona de extraccion sin modificar original.")
    parser.add_argument("--pdf", type=Path, required=True)
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--codigo", required=True)
    args = parser.parse_args()
    print(prepare_pdf(args.pdf, args.project, args.codigo))


if __name__ == "__main__":
    main()

