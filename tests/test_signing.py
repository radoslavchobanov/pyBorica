"""Tests for the signing service using a mock transport."""

import asyncio
import pytest
import httpx

from borica_qes import BoricaConfig
from borica_qes.client import AsyncBoricaClient
from borica_qes.models import SignContent, SignRequest
from borica_qes.enums import ContentFormat, HashAlgorithm


@pytest.mark.asyncio
async def test_signing_flow(mock_transport: httpx.MockTransport) -> None:
    """Verify that a basic signing flow succeeds using the mock transport."""
    cfg = BoricaConfig(
        base_url="https://example/signing-api/v2",
        rp_id="rp-123",
        client_cert="/path/cert.pem",
        client_key="/path/key.pem",
        verify=True,
    )
    async with AsyncBoricaClient(cfg) as client:
        # Patch the underlying httpx AsyncClient transport to use the mock
        client._t._client._transport = mock_transport  # type: ignore[attr-defined]

        content = SignContent(
            confirmText="Sign this document",
            contentFormat=ContentFormat.TEXT,
            data="Hello world",
            fileName="hello.txt",
            hashAlgorithm=HashAlgorithm.SHA256,
        )
        req = SignRequest(contents=[content])

        # Use a token identity method for simplicity
        accepted = await client.signing.send_sign_request(req, client_token="token-xyz")
        assert accepted.data.callbackId == "cb-1"

        # Poll until completed
        status = await client.signing.poll_until_signed(callback_id="cb-1")
        assert status.code == "COMPLETED"
        sig_ref = status.data.signatures[0].signature  # type: ignore[union-attr]
        assert sig_ref == "content-1"

        # Download the content
        data = await client.signing.download_signed_content(sig_ref)
        assert data.startswith(b"%PDF")