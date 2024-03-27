class ComponentFormWithUnsupportedAnnotationError(Exception):
    """
    Exception raised when an unsupported annotation is encountered in ComponentForm.

    Attributes:
        annotation (type): The unsupported annotation that caused the error.
    """

    def __init__(self, annotation: type) -> None:
        """
        Initializes a new instance of the ComponentFormWithUnsupportedAnnotationError class.

        Args:
            annotation (type): The unsupported annotation that caused the error.
        """
        super().__init__(
            f"Annotation {annotation} is not supported by ComponentForm.",
        )


class ComponentFormWithDataclassHasMoreThanOneFieldError(Exception):
    """
    Exception raised when a ComponentForm has both dataclass and other fields at the same time.
    """

    def __init__(self) -> None:
        super().__init__(
            "ComponentForm cannot have dataclass and other fields at the same time.",
        )
