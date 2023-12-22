import datetime
import json

from streamlit.testing.v1 import AppTest


def test_app_renders_add_as_expected(example_app: AppTest):
    assert len(example_app.number_input) == 2
    example_app.number_input[0].set_value(1).run()
    example_app.number_input[1].set_value(5).run()
    example_app.button[0].click().run()
    text = [x.value for x in example_app.markdown]
    assert text == [
        "## Source code of add",
        "# Add",
        "## Results",
        "`6`",
        "This is my app",
    ]


def test_app_renders_divide_as_expected(example_app: AppTest):
    example_app.sidebar.radio[0].set_value("Divide").run()
    assert len(example_app.number_input) == 2
    example_app.number_input[0].set_value(2.0).run()
    example_app.number_input[1].set_value(4.0).run()
    example_app.button[0].click().run()
    text = [x.value for x in example_app.markdown]
    assert text == [
        "## Source code of divide",
        "# Divide",
        "## Results",
        "`0.5`",
        "This is my app",
    ]


def test_app_renders_capitalize_words_as_expected(example_app: AppTest):
    example_app.sidebar.radio[0].set_value("Capitalize words").run()
    assert len(example_app.text_area) == 1
    example_app.text_area[0].set_value('["hello", "world"]').run()
    example_app.button[0].click().run()
    result = json.loads(example_app.json[0].value)
    expected_result = ["Hello", "World"]
    assert result == expected_result


def test_app_renders_count_words_as_expected(example_app: AppTest):
    example_app.sidebar.radio[0].set_value("Count words").run()
    assert len(example_app.text_input) == 1
    example_app.text_input[0].set_value("Hello world").run()
    example_app.button[0].click().run()
    text = [x.value for x in example_app.markdown]
    assert text == [
        "## Source code of count_words",
        "# Count words",
        "## Results",
        "`2`",
        "This is my app",
    ]


def test_app_renders_change_string_as_expected(example_app: AppTest):
    example_app.sidebar.radio[0].set_value("Change string").run()
    assert len(example_app.text_input) == 1
    assert len(example_app.selectbox) == 1
    example_app.text_input[0].set_value("text").run()
    example_app.selectbox[0].select("upper").run()
    example_app.button[0].click().run()
    text = [x.value for x in example_app.markdown]
    assert text == [
        "## Source code of change_string",
        "# Change string",
        "## Results",
        "TEXT",
        "This is my app",
    ]


def test_app_renders_count_hosts_as_expected(example_app: AppTest):
    example_app.sidebar.radio[0].set_value("Count hosts").run()
    assert len(example_app.text_area) == 1
    example_app.text_area[0].set_value('{"test": "192.168.0.0/24"}').run()
    example_app.button[0].click().run()
    result = json.loads(example_app.json[0].value)
    expected_result = {"test": 254}
    assert result == expected_result


def test_example_app_renders_get_weekend_days_as_expected(example_app: AppTest):
    example_app.sidebar.radio[0].set_value("Count weekend days").run()
    assert len(example_app.date_input) == 2
    example_app.date_input[0].set_value(
        datetime.datetime(year=2023, month=1, day=1),
    ).run()
    example_app.date_input[1].set_value(
        datetime.datetime(year=2023, month=1, day=7),
    ).run()
    example_app.button[0].click().run()
    text = [x.value for x in example_app.markdown]
    assert text == [
        "## Source code of count_weekend_days",
        "# Count weekend days",
        "## Results",
        "`2`",
        "This is my app",
    ]


def test_app_renders_get_datetime_diff_as_expected(example_app: AppTest):
    example_app.sidebar.radio[0].set_value("Get datetime diff").run()
    assert len(example_app.date_input) == 2
    assert len(example_app.time_input) == 2
    example_app.date_input[0].set_value(
        datetime.datetime(year=2023, month=1, day=1),
    ).run()
    example_app.time_input[0].set_value(datetime.time(hour=0, minute=0, second=0)).run()
    example_app.date_input[1].set_value(
        datetime.datetime(year=2023, month=1, day=7),
    ).run()
    example_app.time_input[1].set_value(
        datetime.time(hour=12, minute=0, second=0),
    ).run()
    example_app.button[0].click().run()
    result = json.loads(example_app.json[0].value)
    expected_result = {"days": 6, "seconds": 43200, "microseconds": 0}
    assert result == expected_result
