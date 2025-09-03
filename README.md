# borica-qes

Python wrapper for **BORICA B‑Trust Cloud Qualified Electronic Signature (CQES)** API.

This library hides the complexities of the BORICA Signing API — mutual TLS, mandatory headers, identity modes — and exposes a clean, typed interface for Python developers. It supports both synchronous and asynchronous usage, and optionally includes the Remote Identification + OTC signing flow.

## Features

- ✅ Mutual TLS & header setup handled for you
- ✅ Strongly typed models (Pydantic v2)
- ✅ Sync **and** async clients
- ✅ Core flows: submit → poll → download, QR signing, token auth, certificate lookup
- ✅ Optional Remote Identification & OTC signing support

Requires a BORICA **Relying Party ID** and client **TLS certificate + key** issued by BORICA.

## Installation

```bash
pip install borica-qes
# or including development extras
pip install "borica-qes[dev]"
```

## Quickstart

```python
from base64 import b64encode
from borica_qes import BoricaConfig, AsyncBoricaClient, ContentFormat, HashAlgorithm
from borica_qes.models import SignContent, SignRequest

cfg = BoricaConfig(
    base_url="https://cqes-rpuat.b-trust.bg/signing-api/v2",
    rp_id="YOUR_RP_ID",
    client_cert="/path/to/cert.pem",
    client_key="/path/to/key.pem",
    verify=True,
)

async def run():
    content = SignContent(
        confirmText="Please sign",
        contentFormat=ContentFormat.BINARY_BASE64,
        data=b64encode(b"...pdf bytes...").decode(),
        fileName="demo.pdf",
        hashAlgorithm=HashAlgorithm.SHA256,
        toBeArchived=True,
    )
    req = SignRequest(contents=[content], relyingPartyCallbackId="demo-1")
    async with AsyncBoricaClient(cfg) as client:
        accepted = await client.signing.send_sign_request(req, client_token="TOKEN_OR_PROFILE_OTP_OR_PERSONAL_ID")
        status = await client.signing.poll_until_signed(callback_id=accepted.data.callbackId)
        content_id = status.data.signatures[0].signature
        pdf_bytes = await client.signing.download_signed_content(content_id)
        open("demo.signed.pdf", "wb").write(pdf_bytes)

```

See `examples/` for runnable scripts and the full documentation at https://your-org.github.io/borica-qes.

## License

Apache-2.0. See `LICENSE` for details.