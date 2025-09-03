# Remote Identification & OTC Signing

BORICA offers an optional **Remote Identification** flow. It allows you to verify a natural person’s identity online (via video) and then sign documents using a one‑time certificate (OTC).

The high‑level steps are:

1. **Start a web session**: `start_web_session()` returns a `webSessionId` and `resultId`.
2. **Create a registration**: call `create_registration()` with URLs for success and cancel pages. You receive a `sessionId`.
3. **Redirect the customer**: direct the user to `https://id[b|u]at.borica.bg/session/{sessionId}` where they complete video KYC.
4. **Handle callback**: BORICA calls your `requestCallbackUrl` with `clientIdentificator` and `signSessionId` once identification succeeds.
5. **Start OTC signing**: use `start_otc_sign()` with `identificator` and `signSessionId` to show the document to the user and capture their one‑time signature.
6. **Fetch result**: poll `get_web_result(..., process_state="SIGN_SESSION", session_id=signSessionId)` until `signDocuments` appears.

See the `examples/remote_ident_otc.py` script for an end‑to‑end sample.

For more details, consult BORICA’s Remote Identification specification.