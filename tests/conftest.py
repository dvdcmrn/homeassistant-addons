"""Stub Home Assistant when it is not installed so unit tests can run locally."""

from __future__ import annotations

import sys
from types import ModuleType
from unittest.mock import MagicMock


def _install_homeassistant_stub() -> None:
    class HomeAssistantView:
        requires_auth = False
        url = ""
        name = ""

        def json(self, data, status_code=200):
            return {"data": data, "status_code": status_code}

    class StaticPathConfig:
        def __init__(self, url, path, cache_headers=True):
            self.url = url
            self.path = path
            self.cache_headers = cache_headers

    core = ModuleType("homeassistant.core")
    core.HomeAssistant = MagicMock
    core.ServiceCall = MagicMock

    typing_mod = ModuleType("homeassistant.helpers.typing")
    typing_mod.ConfigType = dict

    service_mod = ModuleType("homeassistant.helpers.service")
    service_mod.async_register_admin_service = MagicMock()

    cv_mod = ModuleType("homeassistant.helpers.config_validation")
    cv_mod.empty_config_schema = lambda domain: {}

    helpers = ModuleType("homeassistant.helpers")
    helpers.service = service_mod
    helpers.typing = typing_mod
    helpers.config_validation = cv_mod

    http_view = ModuleType("homeassistant.components.http.view")
    http_view.HomeAssistantView = HomeAssistantView

    http = ModuleType("homeassistant.components.http")
    http.StaticPathConfig = StaticPathConfig
    http.view = http_view

    components = ModuleType("homeassistant.components")
    components.http = http

    ha = ModuleType("homeassistant")
    ha.core = core
    ha.helpers = helpers
    ha.components = components

    sys.modules.setdefault("homeassistant", ha)
    sys.modules.setdefault("homeassistant.core", core)
    sys.modules.setdefault("homeassistant.helpers", helpers)
    sys.modules.setdefault("homeassistant.helpers.service", service_mod)
    sys.modules.setdefault("homeassistant.helpers.typing", typing_mod)
    sys.modules.setdefault("homeassistant.helpers.config_validation", cv_mod)
    sys.modules.setdefault("homeassistant.components", components)
    sys.modules.setdefault("homeassistant.components.http", http)
    sys.modules.setdefault("homeassistant.components.http.view", http_view)


def _homeassistant_available() -> bool:
    try:
        from homeassistant.components import http as ha_http
    except ImportError:
        return False
    return hasattr(ha_http, "StaticPathConfig")


if not _homeassistant_available():
    _install_homeassistant_stub()
