from pathlib import Path

import pandas as pd
import pytest
from streamlit.testing.v1 import AppTest


@pytest.fixture(scope="session")
def example_app_file():
    return Path(__file__).parent / "static" / "example_app.py"


@pytest.fixture()
def incidents_df() -> pd.DataFrame:
    return pd.read_csv(Path(__file__).parent / "static" / "incidents.csv")


@pytest.fixture()
def example_app(example_app_file):
    app = AppTest.from_file(example_app_file.as_posix())
    app.run()
    return app
