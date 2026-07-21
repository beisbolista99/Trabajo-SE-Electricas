from __future__ import annotations

from pathlib import Path

from condensar_memoria_calculo import compact_calculation_memory


def test_documento_compacto_conserva_fuentes(tmp_path: Path) -> None:
    source = tmp_path / "texto.md"
    source.write_text("# Pagina 1\n\nFormula A = pi * r^2\n", encoding="utf-8")
    output = tmp_path / "compacto.md"
    compact_calculation_memory(source, output, "Demo")
    text = output.read_text(encoding="utf-8")
    assert "[Fuente: pagina 1]" in text
    assert "## 12. Referencias a paginas originales" in text

