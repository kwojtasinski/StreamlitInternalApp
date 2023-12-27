import datetime
import ipaddress
import logging
import pathlib
import random
from typing import Literal, Union

import pandas as pd

from streamlit_internal_app.component import StreamlitInternalApp

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

logger = logging.getLogger(__name__)


app = StreamlitInternalApp(
    title="Example App",
    description="This is my app",
    use_wide=True,
    render_code=True,
    use_logging=True,
)


@app.component
def add(a: int, b: int) -> int:
    """Adds two numbers together

    Args:
        a (int): The first number
        b (int): The second number

    Returns:
        int: The sum of the two numbers
    """
    return a + b


@app.component
def divide(a: float, b: float) -> float:
    """Divides two numbers.

    Args:
        a (float): The dividend.
        b (float): The divisor.

    Returns:
        float: The quotient of the division.
    """
    return a / b


@app.component
def count_words(text: str) -> int:
    """
    Count the number of words in a given text.

    Args:
        text (str): The input text.

    Returns:
        int: The number of words in the text.
    """
    return len(text.split())


@app.component
def capitalize_words(text: list[str]) -> list[str]:
    """
    Capitalizes the words in a list.

    Args:
        text (list[str]): The list of words to be capitalized.

    Returns:
        list[str]: The list of capitalized words.
    """
    return [word.capitalize() for word in text]


@app.component
def change_string(text: str, change: Literal["upper", "lower", "title"]) -> str:
    """
    Change the case of the input text based on the specified change.

    Args:
        text (str): The input text to be modified.
        change (Literal["upper", "lower", "title"]): The type of case change to apply.

    Returns:
        str: The modified text with the specified case change applied.
    """
    return getattr(text, change)()


@app.component
def count_hosts(payload: dict[str, str]) -> dict[str, int]:
    """
    Counts the number of hosts in each CIDR.

    Args:
        payload (dict[str, str]): A dictionary containing CIDR strings as values.

    Returns:
        dict[str, int]: A dictionary containing the number of hosts in each CIDR.

    Example:
        >> count_hosts({"test": "192.168.0.0/24"})
        {"test": 254}
    """
    results = {
        k: len(list(ipaddress.ip_network(v).hosts())) for k, v in payload.items()
    }
    return results


@app.component
def count_weekend_days(start_date: datetime.date, end_date: datetime.date) -> int:
    """
    Counts the number of weekend days between two given dates.

    Args:
        start_date (datetime.date): The start date.
        end_date (datetime.date): The end date.

    Returns:
        int: The number of weekend days between the start and end dates.
    """
    results = 0

    diff_in_days = (end_date - start_date).days
    logger.info(
        "There are %s day(s) difference between %s and %s",
        diff_in_days,
        start_date,
        end_date,
    )

    for day in range(diff_in_days + 1):
        if (start_date + datetime.timedelta(days=day)).weekday() in (5, 6):
            results = results + 1

    return results


@app.component
def get_datetime_diff(
    start_dt: datetime.datetime,
    end_df: datetime.datetime,
) -> dict[str, Union[int, float]]:
    """
    Calculate the difference between two datetime objects.

    Args:
        start_dt (datetime.datetime): The starting datetime object.
        end_df (datetime.datetime): The ending datetime object.

    Returns:
        dict[str, Union[int, float]]: A dictionary containing the difference between the two datetime objects.
            The dictionary has the following keys:
            - "days" (int): The number of days in the difference.
            - "seconds" (int): The number of seconds in the difference.
            - "microseconds" (int): The number of microseconds in the difference.
    """
    time_diff = end_df - start_dt
    return {k: getattr(time_diff, k) for k in ("days", "seconds", "microseconds")}


@app.component
def get_incidents_from_year(
    year: Literal["2020", "2021", "2022", "2023"],
) -> pd.DataFrame:
    """
    Retrieve incidents from a specific year.

    Parameters:
        year (str): The year of the incidents to retrieve. Must be one of "2020", "2021", "2022", or "2023".

    Returns:
        pd.DataFrame: A DataFrame containing the incidents from the specified year.
    """
    path_to_csv = pathlib.Path(__file__).parent / "incidents.csv"
    df = pd.read_csv(path_to_csv)
    return df[df["year"] == int(year)]


@app.component
def generate_random_numbers_file(size: int, path_to_save: str) -> pathlib.Path:
    """
    Generate a file with random numbers.

    Args:
        size (int): The number of random numbers to generate.
        path_to_save (str): The path to save the generated file.

    Returns:
        pathlib.Path: The path to the generated file.
    """
    values = [random.random() for _ in range(size)]
    path_to_file = pathlib.Path(path_to_save)
    path_to_file.write_text("\n".join(str(v) for v in values))
    return path_to_file


@app.component
def get_current_datetime() -> datetime.datetime:
    """
    Get the current datetime.

    Returns:
        datetime.datetime: The current datetime.
    """
    return datetime.datetime.today()


app.render()
