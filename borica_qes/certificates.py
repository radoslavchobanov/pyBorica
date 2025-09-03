"""Certificate-related service for the BORICA CQES API.

This module exposes operations to obtain client tokens and to look up
Cloud QES certificates by identity or by profile identifier. The
high-level wrapper classes encapsulate the HTTP interactions and return
pydantic models for convenience.
"""

from __future__ import annotations

from typing import Optional

from .transport import Transport, AsyncTransport
from .enums import IdentifierType
from .models import (
    AuthRequest,
    AuthResponse,
    CertificateByIdentityResponse,
    CertificateByProfileResponse,
)


class CertificateService:
    """Synchronous wrapper around BORICA's certificate-related endpoints."""

    def __init__(self, transport: Transport) -> None:
        self._t = transport

    def get_client_token(self, req: AuthRequest) -> AuthResponse:
        """Exchange a profile ID and OTP for a client token via POST ``/auth``."""
        resp = self._t.request("POST", "/auth", json=req.model_dump())
        return AuthResponse.model_validate(resp.json())

    def get_certificate_by_identity(self, id_type: IdentifierType, identity_value: str) -> CertificateByIdentityResponse:
        """Fetch a certificate by identity type and value via GET ``/cert/identity/...``."""
        resp = self._t.request("GET", f"/cert/identity/{id_type.value}/{identity_value}")
        return CertificateByIdentityResponse.model_validate(resp.json())

    def get_certificate_by_profile_id(self, profile_id: str) -> CertificateByProfileResponse:
        """Fetch a certificate by profile ID via GET ``/cert/{profileId}``."""
        resp = self._t.request("GET", f"/cert/{profile_id}")
        return CertificateByProfileResponse.model_validate(resp.json())


class AsyncCertificateService:
    """Asynchronous variant of :class:`CertificateService`."""

    def __init__(self, transport: AsyncTransport) -> None:
        self._t = transport

    async def get_client_token(self, req: AuthRequest) -> AuthResponse:
        resp = await self._t.request("POST", "/auth", json=req.model_dump())
        return AuthResponse.model_validate(resp.json())

    async def get_certificate_by_identity(self, id_type: IdentifierType, identity_value: str) -> CertificateByIdentityResponse:
        resp = await self._t.request("GET", f"/cert/identity/{id_type.value}/{identity_value}")
        return CertificateByIdentityResponse.model_validate(resp.json())

    async def get_certificate_by_profile_id(self, profile_id: str) -> CertificateByProfileResponse:
        resp = await self._t.request("GET", f"/cert/{profile_id}")
        return CertificateByProfileResponse.model_validate(resp.json())