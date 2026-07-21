from __future__ import annotations

import argparse
from pathlib import Path

from common import PENDING, load_yaml, write_text


def generate_report(project: Path, output: Path) -> Path:
    ficha = load_yaml(project / "ficha_proyecto.yaml")
    lines = [
        "# Informe de revision tecnica",
        "",
        "## 1. Identificacion",
        "",
        f"- Proyecto: {ficha.get('proyecto', PENDING)}",
        f"- Subestacion: {ficha.get('subestacion', PENDING)}",
        "- Documento revisado: PENDIENTE DE VALIDAR",
        "- Codigo: PENDIENTE DE VALIDAR",
        "- Revision: PENDIENTE DE VALIDAR",
        "",
        "## 2. Conclusiones",
        "",
        "PENDIENTE DE VALIDAR.",
        "",
        "## 3. Observaciones",
        "",
        "| ID | Fuente | Observacion | Estado |",
        "| --- | --- | --- | --- |",
        "| OBS-001 | PENDIENTE DE VALIDAR | PENDIENTE DE VALIDAR | PENDIENTE |",
        "",
    ]
    write_text(output, "\n".join(lines))
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description="Generar informe de revision Markdown.")
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(generate_report(args.project, args.output))


if __name__ == "__main__":
    main()

