from __future__ import annotations

from calcular_ocupacion_ductos import calcular_area_cable


def test_area_cable_usa_diametro_exterior() -> None:
    assert round(calcular_area_cable(16.5), 2) == 213.82

