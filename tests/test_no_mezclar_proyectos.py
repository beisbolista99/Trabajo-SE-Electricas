from __future__ import annotations

from pathlib import Path

import pytest

from crear_proyecto import create_project


def test_crear_proyecto_no_sobrescribe_existente(tmp_path: Path) -> None:
    first = create_project("Proyecto Demo", "SE Demo", tmp_path)
    assert first.name == "PROYECTO_DEMO"
    with pytest.raises(FileExistsError):
        create_project("Proyecto Demo", "Otra SE", tmp_path)

