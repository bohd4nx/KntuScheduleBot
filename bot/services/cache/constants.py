KEY_PREFIX = "kntu"

# Розклад лежить довше, ніж «свіжий» (24 год): застарілий кеш рятує, коли портал недоступний.
SCHEDULE_STORAGE_TTL_SECONDS = 7 * 24 * 60 * 60

REDIS_TIMEOUT_SECONDS = 5.0
