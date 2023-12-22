import datetime
import inspect
import json
import logging
from typing import Any, Callable, Literal, Optional, get_args, get_origin

import streamlit as st


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
        if return_type == str:
            st.write(result)

        if return_type == int:
            st.write(result)

        if return_type == float:
            st.write(result)

        if return_type == bool:
            st.write(result)

        if return_type == datetime.datetime:
            st.write(result)

        if return_type == datetime.date:
            st.write(result)

        if get_origin(return_type) == dict:
            st.json(result)

        if get_origin(return_type) == list:
            st.json(result)

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
            return st.text_input(name)

        if annotation == int:
            return st.number_input(name, step=1)

        if annotation == float:
            return st.number_input(name, step=0.01)

        if annotation == bool:
            return st.checkbox(name)

        if get_origin(annotation) == Literal:
            return st.selectbox(name, get_args(annotation))

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
                help=f"Define JSON definition of {name} field (type dict), that will be parsed.",
            )
            return {} if value == "" else json.loads(value)

        if get_origin(annotation) == list:
            if get_args(annotation)[0] == str:
                value = st.text_area(
                    name,
                    help=f"Define JSON definition of {name} field (type list), that will be parsed.",
                )
                return [] if value == "" else json.loads(value)

            if get_origin(get_args(annotation)[0]) == Literal:
                return st.multiselect(
                    name,
                    get_args(get_args(annotation)[0]),
                    help=f"Define JSON definition of {name} field (type list), that will be parsed.",
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

    def component(self, function: Callable) -> None:
        """
        Register a component in the app.

        Args:
            function (Callable): The component to be registered.

        Returns:
            None
        """
        function = ComponentForm(function)
        self.components[function.name] = function

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
        components = [component.name for component in self.components.values()]
        return (
            f'{self.__class__.__name__}(title="{self.title}", components={components})'
            if self.description is None
            else f'{self.__class__.__name__}(title="{self.title}", description="{self.description}", components={components})'
        )

    def setup_logging(self) -> None:
        """
        Setup logging to streamlit.
        """
        logger = logging.getLogger()

        if "StreamlitHandler" not in str(logger.handlers):
            logger.addHandler(StreamlitHandler())
