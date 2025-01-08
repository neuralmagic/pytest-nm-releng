from typing import Union

import pytest


def setenv(monkeypatch: pytest.MonkeyPatch, name: str, value: Union[str, None]) -> None:
    if value is None:
        monkeypatch.delenv(name, raising=False)
    else:
        monkeypatch.setenv(name, value)
