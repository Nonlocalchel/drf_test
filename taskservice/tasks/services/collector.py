def collect_all_validators() -> list:
    from tasks.services.validators import validate_changes, validate_report, check_worker
    return [validate_changes, check_worker, validate_report]


def collect_all_errors(validators: list, validate_obj: object) -> dict[str: str] | None:
    errors = {}
    for validator in validators:
        error = validator(validate_obj)
        if error:
            error_data = list(error.items())[0]
            errors[error_data[0]] = error_data[1]

    return errors
