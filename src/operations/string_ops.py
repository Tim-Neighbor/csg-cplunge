def is_numeric(string, allow_empty_string=True):

    if string == '':
        return allow_empty_string

    try:
        float(string)
    except Exception:
        return False

    return True
