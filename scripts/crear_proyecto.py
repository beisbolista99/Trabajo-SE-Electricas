from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from common import PENDING, PROJECTS_DIR, TEMPLATE_PROJECT_DIR, safe_slug, write_yaml


def create_project(nombre: str, subestacion: str | None = None, base_dir: Path = PROJECTS_DIR) -> Path:
    slug = safe_slug(nombre)
    target = base_dir / slug
    if target.exists():
        raise FileExistsError(f"El proyecto ya existe y no se sobrescribira: {target}")
    if not TEMPLATE_PROJECT_DIR.exists():
        raise FileNotFoundError(f"No existe el template: {TEMPLATE_PROJECT_DIR}")

    ignore = shutil.ignore_patterns("__pycache__", "*.bak", "~$*.xlsx")
    shutil.copytree(TEMPLATE_PROJECT_DIR, target, ignore=ignore)

    ficha = {
        "proyecto": slug,
        "subestacion": subestacion or PENDING,
        "cliente": PENDING,
        "ubicacion": PENDING,
        "tension_at": PENDING,
        "tension_mt": PENDING,
        "responsable_revision": PENDING,
        "fecha_creacion": PENDING,
        "estado": "PENDIENTE",
        "regla_no_mezclar": "No reutilizar datos de otra subestacion sin autorizacion expresa.",
    }
    write_yaml(target / "ficha_proyecto.yaml", ficha)
    return target


def main() -> None:
    parser = argparse.ArgumentParser(description="Crear una nueva carpeta de proyecto.")
    parser.add_argument("--nombre", required=True, help="Nombre del proyecto o subestacion.")
    parser.add_argument("--subestacion", help="Nombre de la subestacion.")
    parser.add_argument("--base-dir", type=Path, default=PROJECTS_DIR)
    args = parser.parse_args()

    path = create_project(args.nombre, args.subestacion, args.base_dir)
    print(path)


if __name__ == "__main__":
    main()

