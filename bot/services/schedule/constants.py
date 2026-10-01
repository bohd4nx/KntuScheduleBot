BASE_URL = "https://portal.kntu.kr.ua/api"

ACCESS_COOKIE = "staffportal_access"
REFRESH_COOKIE = "staffportal_refresh"

# Кеш відповідей порталу — на добу (ключ — понеділок тижня).
CACHE_TTL_SECONDS = 24 * 60 * 60

# Access-токен живе 30 хв — оновлюємо трохи раніше, щоб не влучити в протухлий.
ACCESS_EXPIRY_MARGIN_SECONDS = 60

# Якщо `exp` не вдалося прочитати — вважаємо токен чинним стільки секунд.
ACCESS_FALLBACK_TTL_SECONDS = 15 * 60

# Refresh «ковзний» (30 днів від останнього оновлення): фоновий цикл не дає йому протухнути.
KEEPALIVE_INTERVAL_SECONDS = 12 * 60 * 60

MAX_ATTEMPTS = 3

# Портал відповідає за ~1 с; зависання краще швидко повторити, ніж чекати довго.
REQUEST_TIMEOUT_SECONDS = 8.0
CONNECT_TIMEOUT_SECONDS = 5.0

# Тимчасові збої, які варто повторити: 429 та помилки шлюзу.
# Пауза обмежена, щоб запит користувача не висів хвилинами.
RETRYABLE_STATUS_CODES = frozenset({429, 500, 502, 503, 504})
MAX_RETRY_WAIT_SECONDS = 8.0

PORTAL_MAX_CONNECTIONS = 5
