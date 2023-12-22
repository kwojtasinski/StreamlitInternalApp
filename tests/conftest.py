from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest


@pytest.fixture(scope="session")
def example_app_file():
    return Path(__file__).parent / "static" / "example_app.py"


@pytest.fixture()
def example_app(example_app_file):
    app = AppTest.from_file(example_app_file.as_posix())
    app.run()
    return app
