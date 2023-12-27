import datetime
import inspect
import json
import logging
import pathlib
from functools import wraps
from typing import Any, Callable, Literal, Optional, get_args, get_origin

import streamlit as st
from pandas import DataFrame


class StreamlitHandler(logging.Handler):
    def emit(self, record: logging.LogRecord):
        msg = self.format(record)
        if record.levelno == logging.ERROR:
            st.error(msg, icon="🚨")
        if record.levelno == logging.WARNING:
            st.warning(msg, icon="⚠️")
        if record.levelno == logging.INFO:
            st.info(msg, icon="ℹ️")
        if record.levelno == logging.DEBUG:
            st.info(msg, icon="🐛")


class ComponentForm:
    """
    A class that represents a form for running a component.

    Args:
        function (Callable): The component function to be executed.

    Attributes:
        component (Callable): The component function to be executed.
        name (str): The formatted name of the component.
    """

    def __init__(self, function: Callable):
        """
        Initialize a new instance of the class.

        Args:
            function (Callable): The function to be assigned as the component.

        Returns:
            None
        """
        self.component = function
        self.name = function.__name__.replace("__", "_").replace("_", " ").capitalize()

    def run(self, params: dict[str, Any]):
        """
        Runs the component function with the provided parameters.

        Args:
            params (dict[str, Any]): The parameters to be passed to the component function.

        Returns:
            Any: The result of running the component function.
        """
        return self.component(**params)

    @staticmethod
    def _render_result(result: Any, return_type: Any) -> None:
        """
        Renders the result of the component function based on its return type.

        Args:
            result (Any): The result of running the component function.
            return_type (Any): The return type of the component function.
        """

        if return_type == pathlib.Path:
            st.download_button(
                label="Download",
                data=result.read_text(),
                file_name=result.as_posix(),
            )
            return

        if return_type == DataFrame:
            st.dataframe(data=result)
            return

        if return_type == pathlib.Path:
            st.download_button(
                label="Download",
                data=result.read_text(),
                file_name=result.as_posix(),
            )
            return

        if get_origin(return_type) == dict:
            st.json(result)
            return

        if get_origin(return_type) == list:
            st.json(result)
            return

        try:
            st.write(result)
        except Exception as e:
            st.exception(e)

    @staticmethod
    def _render_element(name: str, annotation: Any) -> Any:
        """
        Renders the input element based on the annotation type.

        Args:
            name (str): The name of the input element.
            annotation (Any): The annotation type of the input element.

        Returns:
            Any: The rendered input element.

        Raises:
            ValueError: If the annotation type is not supported.
        """
        if annotation == str:
            return st.text_input(name, placeholder=name)

        if annotation == int:
            return st.number_input(name, step=1, placeholder=name)

        if annotation == float:
            return st.number_input(name, step=0.01, placeholder=name)

        if annotation == bool:
            return st.checkbox(name)

        if get_origin(annotation) == Literal:
            return st.selectbox(name, get_args(annotation), placeholder=name)

        if annotation == datetime.date:
            return st.date_input(name)

        if annotation == datetime.datetime:
            date = st.date_input(
                label=f"{name}_date",
                help=f"Define day for {name} field",
            )
            time = st.time_input(
                label=f"{name}_time",
                step=60,
                help=f"Define time for {name} field.",
            )
            return datetime.datetime.combine(date=date, time=time)

        if get_origin(annotation) == dict:
            value = st.text_area(
                name,
                placeholder=name,
                help=f"Define JSON definition of {name} field (type dict), that will be parsed.",
            )
            return {} if value == "" else json.loads(value)

        if get_origin(annotation) == list:
            if get_args(annotation)[0] == str:
                value = st.text_area(
                    name,
                    placeholder=name,
                    help=f"Define JSON definition of {name} field (type list), that will be parsed.",
                )
                return [] if value == "" else json.loads(value)

            if get_origin(get_args(annotation)[0]) == Literal:
                return st.multiselect(
                    name,
                    get_args(get_args(annotation)[0]),
                    placeholder=name,
                )
        raise ValueError(f"Unsupported type {annotation}")

    def render(self):
        """
        Renders the component form.

        Displays the component name, docstring (if available), and input elements for the component's parameters.
        """
        annotations = self.component.__annotations__
        return_type = annotations.pop("return", None)

        st.write(f"# {self.name}")

        if self.component.__doc__:
            st.text(self.component.__doc__)

        results = {}

        with st.form(self.component.__name__):
            for name, annotation in annotations.items():
                results[name] = self._render_element(name, annotation)
            submit = st.form_submit_button("Run")

        if submit:
            with st.spinner("Running..."):
                st.write("## Results")
                try:
                    result = self.run(results)
                    self._render_result(result, return_type)
                except Exception as e:
                    st.exception(e)

    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__}(name="{self.name}", component={self.component})'
        )


class StreamlitInternalApp:
    def __init__(  # noqa: PLR0913
        self,
        title: str,
        description: Optional[str] = None,
        use_wide: bool = False,
        render_code: bool = False,
        use_logging: bool = False,
    ):
        """
        Initialize a new instance of the StreamlitInternalApp class.

        Args:
            title (str): The title of the app.
            description (str, optional): The description of the app. Defaults to None.
            use_wide (bool): Whether to use a wide layout for the app. Defaults to False.
            render_code (bool): Whether to render the code in the app. Defaults to False.
            use_logging (bool): Whether to enable logging integration. Defaults to False.
        """
        self.title = title
        self.description = description
        self.use_wide = use_wide
        self.render_code = render_code
        self.components = {}
        if use_logging is True:
            self.setup_logging()

    def component(self, function: Callable) -> Any:
        """
        Register a component in the app. This is a decorator that wraps the component function.

        Args:
            function (Callable): The component to be registered.

        Returns:
            Any - The result of the component function.

        Example:
            >>> def my_component():
            ...     pass
            >>> app.component(my_component)
        """
        component = ComponentForm(function)
        self.components[component.name] = component

        @wraps(function)
        def wrapper(*args, **kwargs):
            return function(*args, **kwargs)

        return wrapper

    def render(self):
        """
        Renders the app by displaying the title, description (if available),
        and allowing the user to choose a component from the sidebar.
        """
        st.set_page_config(
            page_title=self.title,
            layout="wide" if self.use_wide else "centered",
        )
        st.sidebar.title(self.title)

        if self.description is not None:
            st.sidebar.write(f"{self.description}")

        component = st.sidebar.radio("Choose app", list(self.components.keys()))

        if self.render_code is True:
            st.write(
                f"## Source code of {self.components[component].component.__name__}",
            )
            st.code(
                inspect.getsource(self.components[component].component),
                language="python",
                line_numbers=True,
            )
        self.components[component].render()

    def __repr__(self) -> str:
        """
        Returns a string representation of the Component object.

        The string representation includes the class name, title, description (if available),
        and a list of component names.

        Returns:
            str: The string representation of the Component object.
        """
        components = [component.name for component in self.components.values()]
        return (
            f'{self.__class__.__name__}(title="{self.title}", components={components})'
            if self.description is None
            else f'{self.__class__.__name__}(title="{self.title}", description="{self.description}", components={components})'
        )

    def setup_logging(self) -> None:
        """
        Setup logging to streamlit.

        This method adds a StreamlitHandler to the root logger if it doesn't already exist.
        The StreamlitHandler allows log messages to be displayed in the Streamlit app.
        """
        logger = logging.getLogger()

        if "StreamlitHandler" not in str(logger.handlers):
            logger.addHandler(StreamlitHandler())


__all__ = ["StreamlitInternalApp", "ComponentForm"]
