from __future__ import annotations

from calcular_ocupacion_ductos import calcular_ocupacion


def test_ocupacion_ductos_recalcula_area_y_porcentaje() -> None:
    result = calcular_ocupacion(
        diametro_cable_mm=16.5,
        cantidad_cables=2,
        diametro_exterior_ducto_mm=110.0,
        espesor_ducto_mm=5.3,
        cantidad_ductos=1,
        porcentaje_maximo=0.33,
    )
    assert result.area_unitaria_cable_mm2 == 213.82
    assert result.area_total_cables_mm2 == 427.65
    assert result.ocupacion_porcentaje == 5.51
    assert result.estado == "CONFIRMADO"

