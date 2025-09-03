"""Top-level facade for interacting with the BORICA CQES API.

The :class:`BoricaClient` and :class:`AsyncBoricaClient` classes expose
high-level services for signing, certificate retrieval and remote
identification via convenient attributes. They also manage the lifetime
of the underlying HTTP clients, supporting context manager semantics to
ensure resources are released.

Typical usage::

    from borica_qes import BoricaConfig, BoricaClient

    cfg = BoricaConfig(...)
    with BoricaClient(cfg) as client:
        accepted = client.signing.send_sign_request(req, client_token="...")
        status = client.signing.poll_until_signed(callback_id=accepted.data.callbackId)
        content_id = status.data.signatures[0].signature
        signed_bytes = client.signing.download_signed_content(content_id)

For asynchronous applications, use :class:`AsyncBoricaClient` and ``async with``.
"""

from __future__ import annotations

from types import TracebackType
from typing import Optional, Type

from .config import BoricaConfig
from .transport import Transport, AsyncTransport
from .signing import SigningService, AsyncSigningService
from .certificates import CertificateService, AsyncCertificateService
from .identification import IdentificationService, AsyncIdentificationService


class BoricaClient:
    """High-level synchronous CQES API client.

    This facade bundles the various domain services and manages a shared
    underlying :class:`Transport` instance. Use as a context manager to ensure
    the HTTP client is closed automatically.
    """

    def __init__(self, cfg: BoricaConfig) -> None:
        self._t = Transport(cfg)
        self.signing = SigningService(self._t)
        self.certificates = CertificateService(self._t)
        self.identification = IdentificationService(self._t)

    def close(self) -> None:
        """Close the underlying HTTP transport."""
        self._t.close()

    # Synchronous context manager methods
    def __enter__(self) -> "BoricaClient":
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        tb: Optional[TracebackType],
    ) -> None:
        self.close()


class AsyncBoricaClient:
    """High-level asynchronous CQES API client."""

    def __init__(self, cfg: BoricaConfig) -> None:
        self._t = AsyncTransport(cfg)
        self.signing = AsyncSigningService(self._t)
        self.certificates = AsyncCertificateService(self._t)
        self.identification = AsyncIdentificationService(self._t)

    async def aclose(self) -> None:
        """Close the underlying asynchronous HTTP transport."""
        await self._t.aclose()

    # Asynchronous context manager methods
    async def __aenter__(self) -> "AsyncBoricaClient":
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        tb: Optional[TracebackType],
    ) -> None:
        await self.aclose()
