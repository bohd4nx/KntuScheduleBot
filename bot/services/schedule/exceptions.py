class PortalError(Exception):
    """Невдалий виклик порталу (або відповідь, яку неможливо використати).

    `status_code` = None, якщо HTTP-відповіді не було: збій з'єднання, таймаут або битий payload.
    """

    def __init__(self, message: str, *, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code

    @property
    def is_auth_error(self) -> bool:
        """Портал відхилив облікові дані — потрібен новий PORTAL_REFRESH_TOKEN."""
        return self.status_code in (400, 401, 403)
