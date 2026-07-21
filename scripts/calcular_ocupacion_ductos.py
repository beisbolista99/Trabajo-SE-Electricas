from __future__ import annotations

import argparse
import math
from dataclasses import dataclass

from common import area_circulo


@dataclass(frozen=True)
class OccupancyResult:
    area_unitaria_cable_mm2: float
    area_total_cables_mm2: float
    diametro_interior_ducto_mm: float
    area_util_ducto_mm2: float
    ocupacion: float
    ocupacion_porcentaje: float
    ductos_requeridos: int
    estado: str


def calcular_area_cable(diametro_exterior_mm: float) -> float:
    return area_circulo(diametro_exterior_mm)


def calcular_area_util_ducto(diametro_exterior_mm: float, espesor_mm: float) -> tuple[float, float]:
    if espesor_mm < 0:
        raise ValueError("El espesor no puede ser negativo.")
    diametro_interior = diametro_exterior_mm - 2 * espesor_mm
    if diametro_interior <= 0:
        raise ValueError("El diametro interior calculado debe ser mayor que cero.")
    return diametro_interior, area_circulo(diametro_interior)


def calcular_ocupacion(
    diametro_cable_mm: float,
    cantidad_cables: int,
    diametro_exterior_ducto_mm: float,
    espesor_ducto_mm: float,
    cantidad_ductos: int,
    porcentaje_maximo: float = 0.33,
) -> OccupancyResult:
    if cantidad_cables <= 0 or cantidad_ductos <= 0:
        raise ValueError("Las cantidades deben ser mayores que cero.")
    if not 0 < porcentaje_maximo <= 1:
        raise ValueError("El porcentaje maximo debe estar entre 0 y 1.")

    area_unitaria = calcular_area_cable(diametro_cable_mm)
    area_total = area_unitaria * cantidad_cables
    diametro_interior, area_ducto = calcular_area_util_ducto(diametro_exterior_ducto_mm, espesor_ducto_mm)
    ocupacion = area_total / (cantidad_ductos * area_ducto)
    ductos_requeridos = math.ceil(area_total / (area_ducto * porcentaje_maximo))
    estado = "CONFIRMADO" if ocupacion <= porcentaje_maximo else "INCONSISTENTE"
    return OccupancyResult(
        area_unitaria_cable_mm2=round(area_unitaria, 2),
        area_total_cables_mm2=round(area_total, 2),
        diametro_interior_ducto_mm=round(diametro_interior, 2),
        area_util_ducto_mm2=round(area_ducto, 2),
        ocupacion=round(ocupacion, 6),
        ocupacion_porcentaje=round(ocupacion * 100, 2),
        ductos_requeridos=ductos_requeridos,
        estado=estado,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Calcular ocupacion de ductos.")
    parser.add_argument("--diametro-cable-mm", type=float, required=True)
    parser.add_argument("--cantidad-cables", type=int, required=True)
    parser.add_argument("--diametro-exterior-ducto-mm", type=float, required=True)
    parser.add_argument("--espesor-ducto-mm", type=float, required=True)
    parser.add_argument("--cantidad-ductos", type=int, required=True)
    parser.add_argument("--porcentaje-maximo", type=float, default=0.33)
    args = parser.parse_args()
    result = calcular_ocupacion(
        args.diametro_cable_mm,
        args.cantidad_cables,
        args.diametro_exterior_ducto_mm,
        args.espesor_ducto_mm,
        args.cantidad_ductos,
        args.porcentaje_maximo,
    )
    for key, value in result.__dict__.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()

