"""Pytest fixtures for borica-qes tests."""

import httpx
import pytest


@pytest.fixture
def mock_transport() -> httpx.MockTransport:
    """Provide a mock transport that returns canned responses for tests."""

    def handler(request: httpx.Request) -> httpx.Response:
        # Provide minimal routing for sign, status, content and auth endpoints.
        path = request.url.path
        method = request.method

        # Sign request acceptance
        if method == "POST" and path.endswith("/sign"):
            return httpx.Response(
                200,
                json={
                    "data": {"callbackId": "cb-1", "validity": "2025-12-31"},
                    "responseCode": "ACCEPTED",
                    "code": "ACCEPTED",
                    "message": "ok",
                },
            )
        # Poll status
        if method == "GET" and path.startswith("/sign/"):
            # Return completed status with signature reference
            return httpx.Response(
                200,
                json={
                    "data": {"signatures": [{"status": "SIGNED", "signature": "content-1"}]},
                    "code": "COMPLETED",
                },
            )
        # Download content
        if method == "GET" and "/sign/content/" in path:
            return httpx.Response(200, content=b"%PDF-1.4\n%...dummy pdf...")
        # Auth token exchange
        if method == "POST" and path.endswith("/auth"):
            return httpx.Response(
                200,
                json={
                    "data": {"clientToken": "token-xyz"},
                    "responseCode": "OK",
                    "code": "OK",
                    "message": "ok",
                },
            )
        # Fallback: not found
        return httpx.Response(404, json={"message": "not found"})

    return httpx.MockTransport(handler)