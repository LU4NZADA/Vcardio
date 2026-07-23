"""
Caminhos via pathlib.Path.
"""

from pathlib import Path

BASE_DIR: Path = Path(__file__).resolve().parent.parent
DATA_DIR: Path = BASE_DIR / "data"
ASSETS_DIR: Path = BASE_DIR / "assets"
DOCS_DIR: Path = BASE_DIR / "docs"
LOG_DIR: Path = BASE_DIR / "logs"
EXPORT_DIR: Path = BASE_DIR / "exports"
TEST_DIR: Path = BASE_DIR / "tests"
EXAMPLES_DIR: Path = BASE_DIR / "examples"


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def path_dados(nome: str) -> Path:
    return DATA_DIR / nome


def path_asset(nome: str) -> Path:
    return ASSETS_DIR / nome


def path_log(nome: str = "app.log") -> Path:
    ensure_dir(LOG_DIR)
    return LOG_DIR / nome


def path_export(nome: str) -> Path:
    ensure_dir(EXPORT_DIR)
    return EXPORT_DIR / nome