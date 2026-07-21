from __future__ import annotations

from validar_sumatorias import validate_sum


def test_validar_sumatoria_detecta_consistencia() -> None:
    rows = [{"area": "10.5"}, {"area": "4.5"}, {"area": ""}]
    result = validate_sum(rows, "area", 15.0)
    assert result.recalculado == 15.0
    assert result.estado == "CONFIRMADO"


def test_validar_sumatoria_detecta_inconsistencia() -> None:
    rows = [{"area": "10.5"}, {"area": "4.5"}]
    result = validate_sum(rows, "area", 16.0)
    assert result.diferencia == 1.0
    assert result.estado == "INCONSISTENTE"

