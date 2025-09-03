# Identity Modes

When submitting a sign request to `/sign`, you must specify how BORICA should identify and authenticate the customer. This is done via the `rpToClientAuthorization` header. Exactly **one** of the following modes must be used:

| Mode | Header value example | Use case |
| --- | --- | --- |
| **Personal ID** | `personalId:7901011234` | Provide a Bulgarian EGN or LNC. BORICA triggers an OTP to the customer’s phone. |
| **Profile ID + OTP** | `profileId:032-552574:523112` | Customer enters OTP from the B‑Trust Mobile app. |
| **Client token** | `clientToken:TPC7416DC60...` | Exchange `profileId`+`otp` via `/auth` once; reuse the token for subsequent signing. |
| **Certificate ID** | `certId:1234` | Use when you know the certId from B‑Trust Mobile. |

In the Python API, you pass one of these via keyword arguments:

```python
accepted = client.signing.send_sign_request(
    req,
    personal_id="7901011234"  # or profile_id_with_otp=("032-552574", "523112"),
    # or client_token="TPC7416DC60...", or cert_id=1234
)
```

If you specify more than one identity mode, a `ValueError` is raised. See the `signing._auth_header` helper in the source code for details.