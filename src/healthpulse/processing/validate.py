from healthpulse.processing.clean import normalize_record

def validate_records(rows):
    valid, errors = [], []
    for index, row in enumerate(rows):
        try:
            valid.append(normalize_record(row))
        except (TypeError, ValueError, KeyError, OverflowError) as exc:
            errors.append({"row": index, "reason": str(exc)})
    return valid, errors
