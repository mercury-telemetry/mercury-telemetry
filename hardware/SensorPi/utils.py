from datetime import datetime, timezone


def date_str_with_current_timezone():
    return datetime.now(timezone.utc).astimezone().isoformat()
