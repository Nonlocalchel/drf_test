def collect_validators() -> list:
    from tasks.validators import validate_changes, validate_report, check_worker
    return [check_worker, validate_report, validate_changes]

