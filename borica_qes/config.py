"""Configuration for the BORICA CQES API.

This module defines the :class:`BoricaConfig` dataclass which stores the
connection details required to call BORICA's Cloud Qualified Electronic
Signature (CQES) API. The configuration encapsulates the base API URL,
relying party identifier, client certificate and key paths used for
mutual TLS authentication, TLS verification options, a default language
for API responses, and a default timeout for requests.

The :class:`BoricaConfig` type is intentionally minimal; most users
should construct it directly from environment variables or explicit
arguments. The ``verify`` attribute uses httpx's ``VerifyTypes`` to
ensure compatibility with httpx's underlying TLS options.
"""

from dataclasses import dataclass
from httpx._types import VerifyTypes


@dataclass(frozen=True)
class BoricaConfig:
    """Container for BORICA CQES API configuration.

    Parameters
    ----------
    base_url:
        The base URL of the BORICA Signing API. This should include the
        versioned path, e.g. ``https://cqes-rpuat.b-trust.bg/signing-api/v2``.
    rp_id:
        The relying party identifier assigned by BORICA.
    client_cert:
        Path to the PEM encoded client certificate used for mutual TLS.
    client_key:
        Path to the PEM encoded private key matching ``client_cert``.
    verify:
        TLS verification settings accepted by httpx. May be ``True`` (use
        system CA bundle), ``False`` (disable verification) or a path to
        a custom CA bundle.
    default_language:
        Language code for the ``Accept-language`` header (``"bg"`` or
        ``"en"``). Defaults to English.
    timeout_s:
        Default request timeout in seconds.
    """

    base_url: str
    rp_id: str
    client_cert: str
    client_key: str
    verify: VerifyTypes = True
    default_language: str = "en"
    timeout_s: float = 30.0

    def cert_tuple(self) -> tuple[str, str]:
        """Return the certificate and key as a tuple for httpx."""
        return (self.client_cert, self.client_key)