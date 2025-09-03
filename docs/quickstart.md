# Quickstart

This guide walks you through a minimal setup for signing a document with BORICA’s CQES API using **borica-qes**.

## 1. Install the package

```bash
pip install borica-qes
```

## 2. Prepare credentials

To call the API you need:

1. A **Relying Party ID** assigned by BORICA.
2. A client **certificate** and **private key** (PEM format). BORICA issues these for mutual TLS.
3. (Optional) A **CA bundle** for TLS verification, if the system trust store does not include BORICA’s CA.

## 3. Construct a request

Below is an asynchronous example. For synchronous use, import `BoricaClient` instead of `AsyncBoricaClient` and remove `async/await`.

```python
from base64 import b64encode
from borica_qes import BoricaConfig, AsyncBoricaClient, ContentFormat, HashAlgorithm
from borica_qes.models import SignContent, SignRequest

cfg = BoricaConfig(
    base_url="https://cqes-rpuat.b-trust.bg/signing-api/v2",
    rp_id="YOUR_RP_ID",
    client_cert="/path/to/client.crt",
    client_key="/path/to/client.key",
    verify=True,  # or path to a CA bundle
)

async def sign_document():
    # Load your PDF as bytes
    with open("example.pdf", "rb") as f:
        data_bytes = f.read()
    content = SignContent(
        confirmText="Please sign example.pdf",
        contentFormat=ContentFormat.BINARY_BASE64,
        data=b64encode(data_bytes).decode(),
        fileName="example.pdf",
        hashAlgorithm=HashAlgorithm.SHA256,
        toBeArchived=True,
    )
    request = SignRequest(contents=[content], relyingPartyCallbackId="tx-001")
    async with AsyncBoricaClient(cfg) as client:
        # Identify the user via personalId, profileId+OTP, clientToken, or certId
        accepted = await client.signing.send_sign_request(request, personal_id="7901011234")
        final = await client.signing.poll_until_signed(callback_id=accepted.data.callbackId)
        content_id = final.data.signatures[0].signature
        pdf_bytes = await client.signing.download_signed_content(content_id)
    with open("example.signed.pdf", "wb") as f:
        f.write(pdf_bytes)

```

See [How‑tos](howtos/mtls.md) for details on identity modes and mTLS configuration.