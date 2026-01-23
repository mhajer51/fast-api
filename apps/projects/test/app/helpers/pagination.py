DEFAULT_LIMIT = 50
MAX_LIMIT = 100


def clamp_limit(limit: int, default: int = DEFAULT_LIMIT, maximum: int = MAX_LIMIT) -> int:
    if limit <= 0:
        return default
    return min(limit, maximum)
