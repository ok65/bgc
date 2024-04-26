


def escape(raw_string) -> str:
    raw_string = "" if raw_string is None else raw_string
    return raw_string.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\t', '\\t').replace('\r', '\\r').replace("'", "\\'")

