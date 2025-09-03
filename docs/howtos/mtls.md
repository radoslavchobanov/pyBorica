# Mutual TLS Setup

All calls to the BORICA Signing API require **mutual TLS (mTLS)**. This means your client must present a certificate and private key when connecting to the API, and must also validate BORICA’s server certificate.

## Client certificate & key

BORICA issues a client certificate and key for each relying party. These are typically delivered as separate `.crt` and `.key` files or as a `.pfx` bundle that you can extract.

Provide them to `BoricaConfig` via `client_cert` and `client_key`:

```python
cfg = BoricaConfig(
    base_url="...",
    rp_id="...",
    client_cert="/absolute/path/to/client.crt",
    client_key="/absolute/path/to/client.key",
    verify="/absolute/path/to/ca-bundle.pem",  # optional
)
```

## CA bundle

Set `verify` to one of:

- `True` (default): use system trust store to verify BORICA’s certificate chain.
- `False`: **not recommended**, disables verification.
- A path to a CA bundle file containing BORICA’s intermediate/root certificates. Use this if the system store doesn’t trust BORICA.

For more information on Python TLS settings, see the [`httpx` docs](https://www.python-httpx.org/advanced/#ssl).