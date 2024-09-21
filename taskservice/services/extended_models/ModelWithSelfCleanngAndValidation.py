from django.core.exceptions import ValidationError

from services.ValidationErrorsCollector import ValidationErrorsCollector
from services.extended_models.ModelWithSelfCleaning import ModelWithSelfCleaning


class ModelWithSelfValidation(ModelWithSelfCleaning):
    error_collector: ValidationErrorsCollector = ValidationErrorsCollector
    validators: list = []

    def clean(self):
        error_collector = self.error_collector()
        error_collector.validators = self.validators
        errors = error_collector.collect_errors(self)
        if errors:
            raise ValidationError(errors)

        return super().clean()
