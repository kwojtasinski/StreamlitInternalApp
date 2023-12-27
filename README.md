# StreamlitInternalApp

## Overview  

This is a Python package to turn functions into internal apps powered by Streamlit. It creates forms based on the function's annotation and allows you to run the function with the form's values. Note that this is early-stage project with limited functionality.  

## Description

This package provides `StreamlitInternalApp` class that you can use to create internal apps. It provides `component` method decorator that turns any Python function into `ComponentForm` class. It is responsible for rendering form with this function arguments as input fields and return type as output. It doesn't infer the runtime types, but rely completely on the `typing` annotations. The function's docstring is used as a form's description. Once the form is submitted, the function is called with the form's values and the result is displayed in the output section.

`StreamlitInternalApp` is composed of multiple `ComponentForm` instances. It is responsible for rendering the sidebar with the list of available forms and the main section with the selected form. It also provides a way to add custom components to the sidebar.

## Installation

```bash
pip install streamlit-internal-app
```

This package requires Python 3.11+ and Streamlit 1.29+.

## Usage

StreamlitInternalApp is opinionated and designed to be as simple as possible. Custom validation on the UI side is not supported. It is expected that the function will validate the input and raise an exception if the input is invalid. The exception will be displayed in the output section.

Here is a simple example:

```python
from streamlit_internal_app import StreamlitInternalApp

app = StreamlitInternalApp(title="Example app", description="This is an example app.")

@app.component
def add(a: int, b: int) -> int:
    """Adds two numbers."""
    return a + b

app.render()
```

That's all you need to do to create an internal app. You can the application by executing `python -m streamlit run path/to/script.py`.

Here is a table of supported types:

| Annotation | Input field(s) | Output field | Input widget docs | Output widget docs |
| --- | --- | --- | --- | --- |
| `int` | `st.number_input(argument_name, step=1)` | `st.write(result)` | <https://docs.streamlit.io/library/api-reference/widgets/st.number_input> |     <https://docs.streamlit.io/library/api-reference/write-magic/st.write> |
| `float` | `st.number_input(argument_name, step=0.01)` | `st.write(result)` | <https://docs.streamlit.io/library/api-reference/widgets/st.number_input> | <https://docs.streamlit.io/library/api-reference/write-magic/st.write> |
| `str` | `st.text_input(argument_name)` | `st.write(result)` | <https://docs.streamlit.io/library/api-reference/widgets/st.text_input> | <https://docs.streamlit.io/library/api-reference/write-magic/st.write> |
| `bool` | `st.checkbox(argument_name)` | `st.write(result)` | <https://docs.streamlit.io/library/api-reference/widgets/st.checkbox> | <https://docs.streamlit.io/library/api-reference/write-magic/st.write> |
| `datetime.date` | `st.date_input(argument_name)` | `st.write(result)` | <https://docs.streamlit.io/library/api-reference/widgets/st.date_input> | <https://docs.streamlit.io/library/api-reference/write-magic/st.write> |
| `datetime.datetime` | `st.date_input(label=f"{argument_name}_date")` and `st.time_input(label=f"{argument_name}_time", step=60)` combined | `st.write(result)` | <https://docs.streamlit.io/library/api-reference/widgets/st.date_input> <https://docs.streamlit.io/library/api-reference/widgets/st.time_input> | <https://docs.streamlit.io/library/api-reference/write-magic/st.write> |
| `pathlib.Path` | ❌ | `st.download_button(label="Download")` | ❌ | <https://docs.streamlit.io/library/api-reference/widgets/st.download_button> |
| `typing.Literal` | `st.selectbox(argument_name, literal_values)` | `st.write(result)` | <https://docs.streamlit.io/library/api-reference/widgets/st.selectbox> | <https://docs.streamlit.io/library/api-reference/write-magic/st.write> |
| `list` | `st.text_area(argument_name)` that will be parsed into JSON object (for `list[str]`) and `st.multiselect(argument_name, literal_values)` for `list[Literal[str1,str2,...]]`. Only these two are supported. | `st.json(result)` | <https://docs.streamlit.io/library/api-reference/widgets/st.text_area> <https://docs.streamlit.io/library/api-reference/widgets/st.multiselect> | <https://docs.streamlit.io/library/api-reference/data/st.json> |
| `dict` | `st.text_area(argument_name)` that will be parsed into JSON object. Only `dict` annotation is supported. | `st.json(result)` | <https://docs.streamlit.io/library/api-reference/widgets/st.text_area> | <https://docs.streamlit.io/library/api-reference/data/st.json> |
| `pandas.DataFrame` | ❌ | `st.dataframe(result)` | ❌ | <https://docs.streamlit.io/library/api-reference/data/st.dataframe> |

If your annotation is not in the list, the output will be rendered with `st.write` by default.

Here is a short demo of how the example app looks like:
![example app](docs/static/output.gif)

Refer to `/tests/static/example_app.py` for a full example.
If you have poetry installed you can run the example app with `scripts/run_sample_app.sh`, or you can do it with development Docker image.

Refer to `scripts/` directory on how to run unit tests, formatting and linting.

### Logging support

There is a built-in support for logging. You can pass `use_logging=True` into `StreamlitInternalApp` constructor to enable it. It will add custom logging handler that outputs the logs into the output section. "Count weekend days" in `/tests/static/example_app.py` is an example.
