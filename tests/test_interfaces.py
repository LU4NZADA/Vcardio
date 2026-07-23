import pandas as pd


def test_csv_exporter():
    from exports.base import CSVExporter, BaseExporter
    e = CSVExporter()
    assert isinstance(e, BaseExporter)
    r = e.export(pd.DataFrame({"A": [1]}))
    assert isinstance(r, bytes)


def test_cache_decorators_import():
    from data.cache import cache_dataframe, cache_analysis, timed, invalidate
    assert callable(cache_dataframe)


def test_settings_immutability():
    import pytest
    from config.settings import settings
    with pytest.raises(AttributeError):
        settings.APP_NAME = "outro"