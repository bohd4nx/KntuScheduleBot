from datetime import time
from typing import Final

DIGEST_TIME: Final = time(6, 0)
# Спимо шматками: «київська» доба може мати 23/25 годин, тож залишок щоразу рахуємо заново.
MAX_SLEEP_SECONDS: Final = 10 * 60
SATURDAY: Final = 5
