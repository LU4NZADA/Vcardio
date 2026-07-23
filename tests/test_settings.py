def test_settings_campos():
    from config.settings import settings
    assert isinstance(settings.APP_NAME, str)
    assert isinstance(settings.VERSION, str)
    assert isinstance(settings.ANO, int)


def test_settings_semver():
    from config.settings import settings
    partes = settings.VERSION.split(".")
    assert len(partes) == 3
    for p in partes:
        assert p.isdigit()


def test_settings_limiares():
    from config.settings import settings
    assert settings.LIMIAR_ARRITMIA > 0
    assert settings.LIMIAR_HIPERTENSAO > 0


def test_metadata_consistencia():
    from metadata import VERSAO, AUTOR_PRINCIPAL
    from config.settings import settings
    assert VERSAO == settings.VERSION
    assert AUTOR_PRINCIPAL == settings.AUTOR