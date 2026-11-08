from curl_cffi.requests import Response


def backoff(attempt: int, *, max_wait: float) -> float:
    return min(2.0 ** (attempt - 1), max_wait)


def retry_delay(response: Response, attempt: int, *, max_wait: float) -> float:
    """Пауза перед повтором: числовий Retry-After, якщо є, інакше `backoff`."""
    retry_after = response.headers.get("Retry-After")
    if retry_after and str(retry_after).isdigit():
        return min(float(retry_after), max_wait)
    return backoff(attempt, max_wait=max_wait)
