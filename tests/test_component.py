from dataclasses import dataclass

import pytest

from streamlit_internal_app.component import ComponentForm
from streamlit_internal_app.exceptions import (
    ComponentFormWithDataclassHasMoreThanOneFieldError,
    ComponentFormWithUnsupportedAnnotationError,
)


def test_component_form_with_unsupported_type_should_raise_exception():
    def faulty_function(data: bytes):
        ...

    with pytest.raises(ComponentFormWithUnsupportedAnnotationError):
        ComponentForm(faulty_function).render()


def test_component_form_with_dataclass_and_other_fields_should_raise_exception():
    @dataclass
    class DataClass:
        a: int

    def faulty_function(data: DataClass, other: int):
        ...

    with pytest.raises(ComponentFormWithDataclassHasMoreThanOneFieldError):
        ComponentForm(faulty_function).render()
