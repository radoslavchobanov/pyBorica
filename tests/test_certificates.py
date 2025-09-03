"""Tests for the certificate service using a mock transport."""

import pytest
import httpx

from borica_qes import BoricaConfig
from borica_qes.client import BoricaClient
from borica_qes.models import AuthRequest
from borica_qes.enums import IdentifierType


def test_certificate_endpoints(mock_transport: httpx.MockTransport) -> None:
    """Ensure certificate endpoints return expected models with the mock transport."""
    cfg = BoricaConfig(
        base_url="https://example/signing-api/v2",
        rp_id="rp-123",
        client_cert="/path/cert.pem",
        client_key="/path/key.pem",
        verify=True,
    )
    client = BoricaClient(cfg)
    # Patch sync client transport
    client._t._client._transport = mock_transport  # type: ignore[attr-defined]

    # Test auth
    auth_req = AuthRequest(profileId="profile", otp="123456")
    auth_resp = client.certificates.get_client_token(auth_req)
    assert auth_resp.data.clientToken == "token-xyz"

    # Test certificate by identity (will return 404 in mock, so expect HttpError)
    with pytest.raises(Exception):
        client.certificates.get_certificate_by_identity(IdentifierType.EGN, "7901010000")