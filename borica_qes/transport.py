"""HTTP transport layer for the BORICA CQES wrapper.

This module defines thin wrappers around ``httpx.Client`` and
``httpx.AsyncClient`` configured for the BORICA API. These wrappers
handle mutual TLS, default headers and timeouts. They raise
:class:`~borica_qes.errors.HttpError` for non-success status codes.

Consumers should not use this module directly but rather interact via
the higher level services in :mod:`borica_qes.signing`,
:mod:`borica_qes.certificates` and :mod:`borica_qes.identification`.
"""

from __future__ import annotations

from typing import Optional, Any

import httpx

from .config import BoricaConfig
from .errors import HttpError


class Transport:
    """Synchronous HTTP transport with mutual TLS and default headers."""

    def __init__(self, cfg: BoricaConfig) -> None:
        # Save config for debugging/logging but do not expose sensitive info
        self._cfg = cfg
        # Configure client with base URL, client certificate, TLS verify, timeouts and
        # default headers. httpx merges per-request headers with these defaults.
        self._client = httpx.Client(
            base_url=cfg.base_url.rstrip("/"),
            cert=cfg.cert_tuple(),
            verify=cfg.verify,
            timeout=cfg.timeout_s,
            headers={
                "accept": "application/json",
                "Accept-language": cfg.default_language,
                "relyingPartyID": cfg.rp_id,
            },
        )

    def close(self) -> None:
        """Close the underlying HTTP client and release resources."""
        self._client.close()

    def request(
        self,
        method: str,
        path: str,
        *,
        headers: Optional[dict[str, str]] = None,
        json: Optional[dict[str, Any]] = None,
        stream: bool = False,
    ) -> httpx.Response:
        """Perform an HTTP request and return the response.

        Parameters
        ----------
        method:
            HTTP method (e.g. ``"GET"``, ``"POST"``).
        path:
            The path relative to ``base_url`` (should start with ``/``).
        headers:
            Optional additional headers to include in the request.
        json:
            Optional JSON body to send; typically a ``dict``.
        stream:
            If true, do not attempt to parse the response as JSON and return
            the raw response. For binary downloads.

        Raises
        ------
        HttpError
            If the response status code is >= 400.
        """
        resp = self._client.request(method, path, headers=headers, json=json)
        if resp.status_code >= 400:
            # For error responses, do not swallow details; propagate body for debugging
            raise HttpError(resp.status_code, resp.text)
        return resp


class AsyncTransport:
    """Asynchronous HTTP transport with mutual TLS and default headers."""

    def __init__(self, cfg: BoricaConfig) -> None:
        self._cfg = cfg
        self._client = httpx.AsyncClient(
            base_url=cfg.base_url.rstrip("/"),
            cert=cfg.cert_tuple(),
            verify=cfg.verify,
            timeout=cfg.timeout_s,
            headers={
                "accept": "application/json",
                "Accept-language": cfg.default_language,
                "relyingPartyID": cfg.rp_id,
            },
        )

    async def aclose(self) -> None:
        """Close the underlying asynchronous client."""
        await self._client.aclose()

    async def request(
        self,
        method: str,
        path: str,
        *,
        headers: Optional[dict[str, str]] = None,
        json: Optional[dict[str, Any]] = None,
        stream: bool = False,
    ) -> httpx.Response:
        """Perform an asynchronous HTTP request.

        Raises :class:`HttpError` for error status codes. When ``stream`` is
        ``True``, the raw response is returned so callers must handle reading
        the body (e.g. ``await resp.aread()``).
        """
        resp = await self._client.request(method, path, headers=headers, json=json)
        if resp.status_code >= 400:
            # Use bytes for error bodies to avoid decoding issues
            content = await resp.aread()
            raise HttpError(resp.status_code, content.decode(errors="replace"))
        return resp