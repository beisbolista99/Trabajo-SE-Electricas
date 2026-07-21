from __future__ import annotations

from pathlib import Path

from validar_compresion import compression_report


def test_reduccion_tokens_supera_80_por_ciento(tmp_path: Path) -> None:
    original = tmp_path / "original.md"
    compacto = tmp_path / "compacto.md"
    original.write_text(("encabezado repetido " * 500) + "formula relevante A = pi * r^2", encoding="utf-8")
    compacto.write_text("formula relevante A = pi * r^2 [Fuente: pagina 1]", encoding="utf-8")
    report = compression_report(original, compacto)
    assert report["cumple_objetivo"] is True
    assert report["reduccion_tokens_porcentaje"] >= 80

