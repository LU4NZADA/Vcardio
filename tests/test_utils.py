def test_fmt_br():
    from utils.formatters import fmt_br
    assert fmt_br(1234) == "1.234"
    assert fmt_br(0) == "0"


def test_fmt_pct():
    from utils.formatters import fmt_pct
    assert fmt_pct(12.345) == "12.3%"


def test_truncar():
    from utils.text import truncar
    assert truncar("Texto muito longo aqui", 15).endswith("...")
    assert truncar("Curto", 50) == "Curto"


def test_as_int():
    from utils.types import as_int
    assert as_int("42") == 42
    assert as_int(None) == 0


def test_safe_div():
    from utils.types import safe_div
    assert safe_div(10, 2) == 5.0
    assert safe_div(10, 0) == 0.0


def test_clamp():
    from utils.types import clamp
    assert clamp(5, 0, 10) == 5
    assert clamp(-1, 0, 10) == 0