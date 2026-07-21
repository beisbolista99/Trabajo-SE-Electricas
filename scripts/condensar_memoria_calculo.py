from __future__ import annotations

import argparse
import re
from pathlib import Path

from common import PENDING, read_text, write_text
from generar_indice_tecnico import HIGH_KEYWORDS, split_pages


def _important_lines(page_text: str) -> list[str]:
    lines = [line.strip() for line in page_text.splitlines() if line.strip()]
    selected = []
    for line in lines:
        lower = line.lower()
        if any(keyword in lower for keyword in HIGH_KEYWORDS) or "=" in line or "%" in line:
            selected.append(line)
    return selected[:20]


def compact_calculation_memory(text_path: Path, output: Path, title: str = PENDING) -> Path:
    pages = split_pages(read_text(text_path))
    lines = [
        "# Documento compacto",
        "",
        "## 1. Identificacion documental",
        "",
        f"- Titulo: {title}",
        f"- Codigo documental: {PENDING}",
        f"- Revision: {PENDING}",
        f"- Fecha: {PENDING}",
        f"- Estado: PENDIENTE",
        "",
        "## 2. Objetivo y alcance",
        "",
        f"{PENDING}. [Fuente: paginas originales]",
        "",
        "## 3. Criterios de diseno",
        "",
    ]

    criteria_found = False
    technical_rows: list[str] = []
    formulas: list[str] = []
    references: list[str] = []

    for page_number, page_text in pages:
        for line in _important_lines(page_text):
            source = f"[Fuente: pagina {page_number}]"
            if "=" in line:
                formulas.append(f"- `{line}` {source}")
            if re.search(r"tabla|diametro|area|ducto|camara|caja|ocupacion|porcentaje", line, re.IGNORECASE):
                technical_rows.append(f"- {line} {source}")
            if re.search(r"criterio|norma|alcance|objetivo", line, re.IGNORECASE):
                lines.append(f"- {line} {source}")
                criteria_found = True
        references.append(f"- Pagina {page_number}: consultada en texto extraido.")

    if not criteria_found:
        lines.append(f"- {PENDING}. [Fuente: paginas originales]")

    lines.extend(
        [
            "",
            "## 4. Normativa aplicable",
            "",
            f"{PENDING}. [Fuente: paginas originales]",
            "",
            "## 5. Equipos considerados",
            "",
            f"{PENDING}. [Fuente: paginas originales]",
            "",
            "## 6. Topologia de canalizaciones",
            "",
            f"{PENDING}. [Fuente: paginas originales]",
            "",
            "## 7. Tablas tecnicas compactadas",
            "",
        ]
    )
    lines.extend(technical_rows or [f"- {PENDING}. [Fuente: paginas originales]"])
    lines.extend(
        [
            "",
            "DECLARADO: PENDIENTE DE VALIDAR.",
            "",
            "RECALCULADO: PENDIENTE DE VALIDAR.",
            "",
            "DIFERENCIA: PENDIENTE DE VALIDAR.",
            "",
            "ESTADO: PENDIENTE.",
            "",
            "## 8. Formulas utilizadas",
            "",
        ]
    )
    lines.extend(formulas or [f"- {PENDING}. [Fuente: paginas originales]"])
    lines.extend(
        [
            "",
            "## 9. Valores de entrada",
            "",
            f"{PENDING}. [Fuente: paginas originales]",
            "",
            "## 10. Resultados principales",
            "",
            f"{PENDING}. [Fuente: paginas originales]",
            "",
            "## 11. Observaciones e inconsistencias",
            "",
            "No usar este compacto como fuente automatica si se detectan datos heredados. Estado: PENDIENTE.",
            "",
            "## 12. Referencias a paginas originales",
            "",
        ]
    )
    lines.extend(references)
    write_text(output, "\n".join(lines) + "\n")
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description="Condensar texto extraido de una memoria de calculo.")
    parser.add_argument("--text", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--title", default=PENDING)
    args = parser.parse_args()
    print(compact_calculation_memory(args.text, args.output, args.title))


if __name__ == "__main__":
    main()

