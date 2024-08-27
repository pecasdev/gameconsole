import time

def now() -> int:
    if hasattr(time, "ticks_ms"):
        return int(time.ticks_ms())  # type: ignore
    else:
        return int(time.time() * 1000)