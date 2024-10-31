from django.core.exceptions import ValidationError
from django.db import models


class ValidationErrorsCollector:
    """
    Tool which provide easy interface to validate you model,
    if the field values are interrelated and require more difficult processing.
    To use this tool:
        1. Create an attribute of your class that will reference an instance of that class;
        2. Set to him attribute validators() which will contain a list of validator functions that throw exceptions;
        3. Launch method obj.collect_errors where you need it and handle them
    You can override method get_error_message if the logic of its work does not suit you
    This tool by itself helps to collect a list of errors into a dictionary by running the specified validators.
    It is more useful in conjunction with SelfValidationMixin
    """
    validators: list = []
    error = ValidationError

    def collect_errors(self, validate_obj: models.Model) -> dict[str: str] | None:
        """Collect all validate messages from validate functions which """
        errors = {}
        for validator in self.validators:
            try:
                validator(validate_obj)
            except self.error as error:
                error_data = self.get_error_message(error)
                errors[error_data[0]] = error_data[1]

        return errors

    @staticmethod
    def get_error_message(error: any) -> list:
        """Make errors data for ValidationErrorsCollector obj"""
        error = error.error_dict
        error_data = list(error.items())[0]
        return error_data

