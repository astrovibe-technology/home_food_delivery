from datetime import time

SLOT_TIME_MAP = {
    "early_morning": (time(3, 0), time(7, 0)),
    "breakfast":     (time(7, 0), time(11, 0)),
    "brunch":        (time(11, 0), time(13, 0)),
    "lunch":         (time(13, 0), time(16, 0)),
    "snacks":        (time(16, 0), time(19, 0)),
    "dinner":        (time(19, 0), time(23, 0)),
    "midnight":      (time(23, 0), time(3, 0)),
}




