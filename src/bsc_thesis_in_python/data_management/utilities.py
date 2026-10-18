def validate_input(value, expected_type, varname):
    """Validates that inputs passed to a function fit their expected type.

    :param value: Argument to be checked.
    :param expected_type: Expected argument type (e.g., pd.DataFrame)
    :param varname: Variable name passed in the error message.
    """
    if not isinstance(value, expected_type):
        _raise_type_error(varname, expected_type, value)


def _raise_type_error(varname, expected, actual):
    """Formats and raises a TypeError for the validate_input function."""
    actual_name = type(actual).__name__
    errortext = f"{varname} expected {expected}, not {actual_name}"
    raise TypeError(errortext)
