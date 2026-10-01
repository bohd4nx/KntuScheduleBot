import base64
import json


def jwt_expiry(token: str) -> float:
    """Поле `exp` з JWT (без перевірки підпису — лише щоб спланувати оновлення)."""
    try:
        payload = token.split(".")[1]
        return float(json.loads(base64.urlsafe_b64decode(payload + "=" * (-len(payload) % 4)))["exp"])
    except (IndexError, ValueError, KeyError):
        return 0.0
