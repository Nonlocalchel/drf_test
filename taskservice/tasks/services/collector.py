from django.core.exceptions import ValidationError


def collect_all_validators() -> list:
    from tasks.services.validators import validate_changes, validate_report, check_worker
    return [check_worker, validate_report, validate_changes]


def collect_all_errors(validators: list, validate_obj: object) -> dict[str: str] | None:
    errors = {}
    for validator in validators:
        try:
            validator(validate_obj)
        except ValidationError as validation_error:
            error = validation_error.error_dict
            error_data = list(error.items())[0]
            errors[error_data[0]] = error_data[1]

    return errors
