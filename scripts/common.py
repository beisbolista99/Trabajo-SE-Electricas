from __future__ import annotations

import csv
import math
import re
import shutil
import unicodedata
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

try:
    import yaml
except ModuleNotFoundError:
    yaml = None  # type: ignore[assignment]

PENDING = "PENDIENTE DE VALIDAR"
CONFIDENCE_LEVELS = {"CONFIRMADO", "RECALCULADO", "INFERIDO", "PENDIENTE", "INCONSISTENTE"}
REPO_ROOT = Path(__file__).resolve().parents[1]
PROJECTS_DIR = REPO_ROOT / "projects"
TEMPLATE_PROJECT_DIR = PROJECTS_DIR / "_TEMPLATE_PROYECTO"

DOCUMENT_RECORD_HEADERS = [
    "Proyecto",
    "Subestacion",
    "Codigo documental",
    "Titulo",
    "Revision o edicion",
    "Fecha",
    "Disciplina",
    "Tipo de documento",
    "Estado documental",
    "Paginas o laminas",
    "Fuente",
    "Nivel de confianza",
    "Archivo",
    "Advertencias",
]


def safe_slug(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value.strip())
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^A-Za-z0-9]+", "_", ascii_text).strip("_").upper()
    return slug or "PENDIENTE_DE_VALIDAR"


def timestamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as file:
        if yaml is not None:
            data = yaml.safe_load(file) or {}
        else:
            data = {}
            for raw_line in file:
                line = raw_line.strip()
                if not line or line.startswith("#") or ":" not in line:
                    continue
                key, value = line.split(":", 1)
                data[key.strip()] = value.strip().strip('"')
    if not isinstance(data, dict):
        raise ValueError(f"YAML no valido: {path}")
    return data


def write_yaml(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        if yaml is not None:
            yaml.safe_dump(data, file, allow_unicode=False, sort_keys=False)
            return
        for key, value in data.items():
            file.write(f'{key}: "{value}"\n')


def backup_file(path: Path) -> Path | None:
    if not path.exists():
        return None
    backup = path.with_name(f"{path.name}.{timestamp()}.bak")
    shutil.copy2(path, backup)
    return backup


def ensure_project_dir(project: Path) -> Path:
    project = project.resolve()
    if not project.exists():
        raise FileNotFoundError(f"No existe el proyecto: {project}")
    ficha = project / "ficha_proyecto.yaml"
    if not ficha.exists():
        raise FileNotFoundError(f"No existe ficha_proyecto.yaml en: {project}")
    return project


def ensure_inside(base: Path, candidate: Path) -> None:
    base_resolved = base.resolve()
    candidate_resolved = candidate.resolve()
    try:
        candidate_resolved.relative_to(base_resolved)
    except ValueError as exc:
        raise ValueError(f"Ruta fuera del ambito permitido: {candidate}") from exc


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str, overwrite: bool = True) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not overwrite:
        raise FileExistsError(f"El archivo ya existe: {path}")
    path.write_text(content, encoding="utf-8")


def estimate_tokens(text: str) -> int:
    try:
        import tiktoken

        encoding = tiktoken.get_encoding("cl100k_base")
        return len(encoding.encode(text))
    except Exception:
        return max(1, math.ceil(len(text) / 4))


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def write_csv_dicts(path: Path, rows: Iterable[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def area_circulo(diametro_mm: float) -> float:
    if diametro_mm <= 0:
        raise ValueError("El diametro debe ser mayor que cero.")
    return math.pi * (diametro_mm / 2) ** 2


def infer_document_type(path: Path) -> str:
    lower = str(path).lower()
    if "plan" in lower:
        return "plano"
    if "memoria" in lower or "calculo" in lower:
        return "memoria_calculo"
    if "hctg" in lower:
        return "hctg"
    if "catalog" in lower:
        return "catalogo"
    if "comentario" in lower:
        return "comentario_cliente"
    if "especific" in lower:
        return "especificacion_tecnica"
    return "otro"


def project_name_from_ficha(project_dir: Path) -> str:
    ficha = load_yaml(project_dir / "ficha_proyecto.yaml")
    return str(ficha.get("proyecto") or project_dir.name)


def compact_status(declared: float, recalculated: float, tolerance: float = 0.01) -> str:
    return "CONFIRMADO" if abs(declared - recalculated) <= tolerance else "INCONSISTENTE"
