import importlib

import pytest
from fastapi.testclient import TestClient

import src.app as app_module


@pytest.fixture(autouse=True)
def reload_app_module():
    """Reload the app module before each test to reset in-memory state."""
    importlib.reload(app_module)
    yield
    importlib.reload(app_module)


@pytest.fixture
def client():
    return TestClient(app_module.app)
