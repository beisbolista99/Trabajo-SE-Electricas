from __future__ import annotations

import argparse
from pathlib import Path

from common import estimate_tokens, read_text, write_yaml


def compression_report(original: Path, compacto: Path, objetivo_minimo: float = 80.0) -> dict[str, object]:
    original_tokens = estimate_tokens(read_text(original))
    compact_tokens = estimate_tokens(read_text(compacto))
    reduction = 0.0 if original_tokens == 0 else (1 - compact_tokens / original_tokens) * 100
    return {
        "archivo_original": str(original),
        "documento_compacto": str(compacto),
        "paginas_totales": "PENDIENTE DE VALIDAR",
        "paginas_prioridad_alta": "PENDIENTE DE VALIDAR",
        "paginas_prioridad_media": "PENDIENTE DE VALIDAR",
        "paginas_prioridad_baja": "PENDIENTE DE VALIDAR",
        "tokens_originales_estimados": original_tokens,
        "tokens_documento_compacto": compact_tokens,
        "reduccion_tokens_porcentaje": round(reduction, 2),
        "objetivo_minimo_porcentaje": objetivo_minimo,
        "cumple_objetivo": reduction >= objetivo_minimo,
        "tablas_extraidas": "PENDIENTE DE VALIDAR",
        "formulas_detectadas": "PENDIENTE DE VALIDAR",
        "referencias_cruzadas_detectadas": "PENDIENTE DE VALIDAR",
        "paginas_requieren_revision_visual": [],
        "advertencias": [],
    }


def validate_compression(original: Path, compacto: Path, output: Path) -> Path:
    write_yaml(output, compression_report(original, compacto))
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description="Validar reduccion de tokens entre texto original y compacto.")
    parser.add_argument("--original", type=Path, required=True)
    parser.add_argument("--compacto", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(validate_compression(args.original, args.compacto, args.output))


if __name__ == "__main__":
    main()

