"""borica-qes package root.

Re-export primary classes and enums for convenience. Use __all__ to make
autocomplete friendly and to signal the public API surface. Internal
modules should not be imported directly by consumers.
"""

from .client import BoricaClient, AsyncBoricaClient
from .config import BoricaConfig
from .enums import (
    ContentFormat,
    SignatureType,
    HashAlgorithm,
    Payer,
    IdentifierType,
    ReportType,
    Language,
    SignStatus,
)
from .errors import BoricaError, HttpError, ApiError
from .models import (
    SignContent,
    SignRequest,
    QrRequest,
    AuthRequest,
    SignAcceptedResponse,
    SignStatusResponse,
    QrAcceptedResponse,
)

__all__ = [
    "BoricaClient",
    "AsyncBoricaClient",
    "BoricaConfig",
    "ContentFormat",
    "SignatureType",
    "HashAlgorithm",
    "Payer",
    "IdentifierType",
    "ReportType",
    "Language",
    "SignStatus",
    "BoricaError",
    "HttpError",
    "ApiError",
    "SignContent",
    "SignRequest",
    "QrRequest",
    "AuthRequest",
    "SignAcceptedResponse",
    "SignStatusResponse",
    "QrAcceptedResponse",
]