"""
Interfaces (Protocolos) para exportadores.
"""

from typing import Protocol, runtime_checkable
import pandas as pd


@runtime_checkable
class BaseExporter(Protocol):
    def export(self, **kwargs) -> bytes | None: ...


class CSVExporter:
    def export(self, df: pd.DataFrame, **kwargs) -> bytes:
        return df.to_csv(index=False).encode("utf-8")


class ExcelExporter:
    def export(self, sheets: dict, **kwargs) -> bytes:
        from io import BytesIO
        buf = BytesIO()
        with pd.ExcelWriter(buf, engine="openpyxl") as w:
            for nome, df in sheets.items():
                df.to_excel(w, index=False, sheet_name=nome)
        return buf.getvalue()