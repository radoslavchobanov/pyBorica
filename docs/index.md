# borica-qes Documentation

Welcome to the documentation for **borica-qes**, a Python wrapper around BORICA’s Cloud Qualified Electronic Signature (CQES) API.

Use the navigation to the left to explore guides and reference material. If you're new to the library, start with the [Quickstart](quickstart.md).

## Overview

borica-qes simplifies integrating BORICA’s Signing API in your Python applications. It manages TLS configuration, headers, request/response models, and provides helper methods to handle polling and content download.

- **Sign documents**: submit requests, poll until signed, and download signed content.
- **QR flow**: initiate signing via QR code.
- **Authentication**: exchange profileId and OTP for a client token via `/auth`.
- **Certificate lookup**: check if a user holds a Cloud QES by identity or profile ID.
- **Remote Identification** (optional): perform web/mobile identification and one‑time certificate signing.

See also [Quickstart](quickstart.md) for a working example and [How‑tos](howtos/mtls.md) for detailed guides on specific topics.