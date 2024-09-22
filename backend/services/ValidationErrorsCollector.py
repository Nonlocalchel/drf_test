from django.core.exceptions import ValidationError
from django.db import models


class ValidationErrorsCollector:
    validators: list = []
    error = ValidationError

    def collect_errors(self, validate_obj: models.Model) -> dict[str: str] | None:
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
        error = error.error_dict
        error_data = list(error.items())[0]
        return error_data

