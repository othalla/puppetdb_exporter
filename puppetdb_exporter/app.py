import hug


@hug.get('/metrics')
def metrics() -> str:
    return ""
