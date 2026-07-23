"""
Pacote de configuracao.
"""

from config.settings import settings, AppSettings

from config.app import (
    MESES_PT, COMORB_COLS,
    BINS_IDADE, LABELS_IDADE,
)
from config.plotly import PLOTLY_THEME, chart_layout
from config.colors import (
    DIAG_COLORS, CORES_COMORBIDADES,
    COR_PRIMARIA, COR_SECUNDARIA, COR_ALERTA, COR_INFO,
    COR_FUNDO, COR_SUPERFICIE, COR_TEXTO, COR_TEXTO_MUTED,
)
from config.paths import (
    BASE_DIR, DATA_DIR, ASSETS_DIR, DOCS_DIR, LOG_DIR,
    EXPORT_DIR, TEST_DIR, EXAMPLES_DIR,
    path_dados, path_asset, path_log, path_export,
)