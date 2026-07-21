from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

from common import read_csv_dicts


@dataclass(frozen=True)
class SumValidation:
    declarado: float
    recalculado: float
    diferencia: float
    estado: str


def validate_sum(rows: list[dict[str, str]], value_column: str, declared_total: float, tolerance: float = 0.01) -> SumValidation:
    total = 0.0
    for row in rows:
        value = str(row.get(value_column, "")).strip().replace(",", ".")
        if not value:
            continue
        total += float(value)
    difference = declared_total - total
    state = "CONFIRMADO" if abs(difference) <= tolerance else "INCONSISTENTE"
    return SumValidation(
        declarado=round(declared_total, 4),
        recalculado=round(total, 4),
        diferencia=round(difference, 4),
        estado=state,
    )


def validate_sum_csv(csv_path: Path, value_column: str, declared_total: float, tolerance: float = 0.01) -> SumValidation:
    return validate_sum(read_csv_dicts(csv_path), value_column, declared_total, tolerance)


def main() -> None:
    parser = argparse.ArgumentParser(description="Validar subtotal declarado contra filas visibles en CSV.")
    parser.add_argument("--csv", type=Path, required=True)
    parser.add_argument("--columna", required=True)
    parser.add_argument("--total-declarado", type=float, required=True)
    parser.add_argument("--tolerancia", type=float, default=0.01)
    args = parser.parse_args()
    result = validate_sum_csv(args.csv, args.columna, args.total_declarado, args.tolerancia)
    for key, value in result.__dict__.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()

