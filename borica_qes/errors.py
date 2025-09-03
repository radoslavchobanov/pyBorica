"""Custom exception hierarchy for the BORICA CQES wrapper.

The API wrapper raises these exceptions to distinguish between transport
errors (e.g. network failures or HTTP status codes), API semantic
errors (non-2xx JSON responses containing ``code`` and ``message``)
and generic wrapper errors.
"""


class BoricaError(Exception):
    """Base class for all BORICA CQES errors."""

    pass


class HttpError(BoricaError):
    """Raised when a non-2xx HTTP response is encountered.

    Attributes
    ----------
    status_code:
        The HTTP status code returned by the server.
    body:
        The response body (text or bytes) received from the server.
    """

    def __init__(self, status_code: int, body: str | bytes) -> None:
        super().__init__(f"HTTP {status_code}: {body!r}")
        self.status_code = status_code
        self.body = body


class ApiError(BoricaError):
    """Raised when BORICA returns an error code in a JSON response.

    Attributes
    ----------
    code:
        The error code provided by BORICA.
    message:
        Human-readable description of the error.
    """

    def __init__(self, code: str, message: str) -> None:
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message