"""Typed request and response models for the BORICA CQES API.

Pydantic BaseModels are used to enforce type correctness and to provide
helpful error messages when constructing payloads. All fields map
directly to the JSON structures defined in BORICA's specification.

Refer to the official documentation for detailed semantics of each
field. This module merely reflects the shape of the data; business
logic lives in :mod:`borica_qes.signing`, :mod:`borica_qes.certificates` and
other modules.
"""

from __future__ import annotations

from typing import Optional, List, Any, Dict
from pydantic import BaseModel

from .enums import (
    ContentFormat,
    HashAlgorithm,
    SignatureType,
    Payer,
    SignStatus,
)


# -----------------------------------------------------------------------------
# Signing payloads
# -----------------------------------------------------------------------------


class SignaturePosition(BaseModel):
    """Coordinates for visual signature placement in a PDF.

    ``imageWidth`` and ``imageHeight`` define the size of the signature area.
    ``imageXAxis`` and ``imageYAxis`` define the upper-left origin of the
    signature area relative to the page origin. ``pageNumber`` is 1-based.
    """

    imageHeight: int
    imageWidth: int
    imageXAxis: int
    imageYAxis: int
    pageNumber: int


class SignContent(BaseModel):
    """Represents a single content item to be signed.

    The ``data`` field must be base64 encoded when using
    :class:`ContentFormat.BINARY_BASE64` or :class:`ContentFormat.DIGEST`.
    When ``contentFormat`` is ``TEXT``, ``data`` contains the raw string.
    """

    confirmText: str
    contentFormat: ContentFormat
    data: str
    fileName: str
    hashAlgorithm: HashAlgorithm = HashAlgorithm.SHA256
    padesVisualSignature: bool = False
    signaturePosition: Optional[SignaturePosition] = None
    signatureType: SignatureType = SignatureType.XADES_BASELINE_LTA_ENVELOPING
    toBeArchived: bool = False


class SignRequest(BaseModel):
    """Body for the POST ``/sign`` endpoint.

    You must provide exactly one identity method (see ``rpToClientAuthorization``
    header) via the corresponding keyword arguments in
    :meth:`~borica_qes.signing.SigningService.send_sign_request`.
    """

    contents: List[SignContent]
    relyingPartyCallbackId: Optional[str | int] = None
    callbackURL: Optional[str] = None
    payer: Payer = Payer.RELYING_PARTY
    isLogin: bool = False


class SignatureItem(BaseModel):
    """Result item for a signed content.

    The ``status`` indicates progress and the ``signature`` contains a
    reference to the signed document when completed.
    """

    status: SignStatus
    signature: Optional[str] = None
    signatureType: Optional[str] = None


class SignAcceptedData(BaseModel):
    """Data returned upon initial acceptance of a sign request."""

    callbackId: str
    validity: str


class SignAcceptedResponse(BaseModel):
    """Response from POST ``/sign`` when the request is accepted."""

    data: SignAcceptedData
    responseCode: str
    code: str
    message: str


class SignStatusData(BaseModel):
    """Data returned when polling for sign status."""

    cert: Optional[str] = None
    signatures: List[SignatureItem]


class SignStatusResponse(BaseModel):
    """Response from GET ``/sign/{callbackId}`` or ``/sign/rpcallbackid/{rpCallbackId}``.

    If the signing is still in progress, the ``code`` field will typically
    contain ``IN_PROGRESS`` and ``data`` may be null or contain partial
    information. When completed, ``code`` is ``COMPLETED`` and the
    ``signatures`` list holds references to the signed content(s).
    """

    data: Optional[SignStatusData] = None
    responseCode: Optional[str] = None
    code: Optional[str] = None
    message: Optional[str] = None


class QrInnerRequest(BaseModel):
    """Internal container for QR signing requests."""

    content: SignContent
    relyingPartyCallbackId: Optional[str | int] = None
    callbackURL: Optional[str] = None
    payer: Payer = Payer.RELYING_PARTY
    isLogin: bool = False


class QrRequest(BaseModel):
    """Body for POST ``/signviaqr``.

    The ``qrHeight`` and ``qrWidth`` fields allow controlling the size of
    the returned QR image. If omitted, default sizes will be used.
    """

    qrHeight: Optional[int] = None
    qrWidth: Optional[int] = None
    request: QrInnerRequest


class QrAcceptedData(BaseModel):
    """Data returned from ``/signviaqr`` when the request is accepted."""

    callbackId: str
    qrImage: Optional[str] = ""
    qrPlain: Optional[str] = ""
    validity: str


class QrAcceptedResponse(BaseModel):
    """Response from POST ``/signviaqr`` upon acceptance."""

    data: QrAcceptedData
    responseCode: str
    code: str
    message: str


# -----------------------------------------------------------------------------
# Auth & Certificates
# -----------------------------------------------------------------------------


class AuthRequest(BaseModel):
    """Body for POST ``/auth``.

    ``profileId`` must correspond to the user's BORICA profile and ``otp``
    must be the one-time password sent to the user. The API returns a
    ``clientToken`` which can be used for subsequent signing requests.
    """

    profileId: str
    otp: str | int


class AuthResponseData(BaseModel):
    clientToken: str


class AuthResponse(BaseModel):
    data: AuthResponseData
    responseCode: str
    code: str
    message: str


class CertificateByIdentityData(BaseModel):
    encodedCert: str
    certReqId: int
    devices: List[str]


class CertificateByIdentityResponse(BaseModel):
    data: CertificateByIdentityData
    responseCode: str
    code: str
    message: str


class CertificateByProfileData(BaseModel):
    encodedCert: str


class CertificateByProfileResponse(BaseModel):
    data: CertificateByProfileData
    responseCode: str
    code: str
    message: str
