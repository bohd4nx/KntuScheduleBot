from typing import Any

from curl_cffi.requests import Response


def backoff(attempt: int, *, max_wait: float) -> float:
    """Експоненційна пауза між спробами: 1, 2, 4… с, але не більше `max_wait`."""
    return min(2.0 ** (attempt - 1), max_wait)


def retry_delay(response: Response, attempt: int, *, max_wait: float) -> float:
    """Пауза перед повтором: числовий Retry-After, якщо є, інакше `backoff`."""
    retry_after = response.headers.get("Retry-After")
    if retry_after and str(retry_after).isdigit():
        return min(float(retry_after), max_wait)
    return backoff(attempt, max_wait=max_wait)


def read_json(response: Response) -> Any:
    """Тіло відповіді як JSON; `ValueError`, якщо воно не JSON."""
    return response.json()  # type: ignore[no-untyped-call]
