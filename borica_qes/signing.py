"""High-level signing service for the BORICA CQES API.

This module defines both synchronous and asynchronous service classes for
submitting and tracking signing requests. It also includes the helper
``_auth_header`` which constructs the mandatory ``rpToClientAuthorization``
header from various identity inputs. Callers should provide exactly one
identity field per request.

Refer to the official specification for details on the semantics of
each endpoint; this wrapper simply models the request/response
workflow.
"""

from __future__ import annotations

from typing import Optional, Dict, Any
from typing_extensions import TypedDict, Unpack

from .transport import Transport, AsyncTransport
from .models import (
    SignRequest,
    SignAcceptedResponse,
    SignStatusResponse,
    QrRequest,
    QrAcceptedResponse,
)
from .errors import ApiError
from .utils import poll


def _auth_header(
    *,
    personal_id: Optional[str] = None,
    profile_id_with_otp: Optional[tuple[str, str | int]] = None,
    client_token: Optional[str] = None,
    cert_id: Optional[str | int] = None,
) -> Dict[str, str]:
    """Build the ``rpToClientAuthorization`` header value.

    Exactly one of the keyword arguments must be supplied. These correspond to
    the identification methods accepted by BORICA. See the specification for
    details.
    """
    count = sum(x is not None for x in (personal_id, profile_id_with_otp, client_token, cert_id))
    if count != 1:
        raise ValueError(
            "Specify exactly one of: personal_id, profile_id_with_otp, client_token, cert_id."
        )
    if personal_id is not None:
        return {"rpToClientAuthorization": f"personalId:{personal_id}"}
    if profile_id_with_otp is not None:
        pid, otp = profile_id_with_otp
        return {"rpToClientAuthorization": f"profileId:{pid}:{otp}"}
    if client_token is not None:
        return {"rpToClientAuthorization": f"clientToken:{client_token}"}
    if cert_id is not None:
        return {"rpToClientAuthorization": f"certId:{cert_id}"}
    return {}


class IdentityKwargs(TypedDict, total=False):
    """TypedDict for identity keyword arguments used by send_sign_request.

    At most one of the keys should be provided when calling
    ``send_sign_request``. The :func:`_auth_header` helper enforces that
    exactly one is supplied at runtime.
    """

    personal_id: str
    profile_id_with_otp: tuple[str, str | int]
    client_token: str
    cert_id: str | int


class SigningService:
    """Synchronous signing API wrapper."""

    def __init__(self, transport: Transport) -> None:
        self._t = transport

    def send_sign_request(
        self,
        req: SignRequest,
        *,
        personal_id: Optional[str] = None,
        profile_id_with_otp: Optional[tuple[str, str | int]] = None,
        client_token: Optional[str] = None,
        cert_id: Optional[str | int] = None,
    ) -> SignAcceptedResponse:
        """Submit a signing request via POST ``/sign``.

        One of the identity parameters must be supplied. The return object
        contains a ``callbackId`` which should be used to poll for completion.
        """
        headers = _auth_header(
            personal_id=personal_id,
            profile_id_with_otp=profile_id_with_otp,
            client_token=client_token,
            cert_id=cert_id,
        )
        resp = self._t.request("POST", "/sign", headers=headers, json=req.model_dump())
        data = resp.json()
        return SignAcceptedResponse.model_validate(data)

    def get_sign_result(self, callback_id: str) -> SignStatusResponse:
        """Retrieve signing status by callback identifier."""
        resp = self._t.request("GET", f"/sign/{callback_id}")
        return SignStatusResponse.model_validate(resp.json())

    def get_sign_result_by_rp_callback_id(self, rp_callback_id: str) -> SignStatusResponse:
        """Retrieve signing status by relying party callback identifier."""
        resp = self._t.request("GET", f"/sign/rpcallbackid/{rp_callback_id}")
        return SignStatusResponse.model_validate(resp.json())

    def poll_until_signed(
        self,
        *,
        callback_id: Optional[str] = None,
        rp_callback_id: Optional[str] = None,
        interval_s: float = 2.0,
        timeout_s: float = 180.0,
    ) -> SignStatusResponse:
        """Poll the sign status endpoint until the operation completes.

        Either ``callback_id`` or ``rp_callback_id`` must be provided.
        Returns a :class:`SignStatusResponse` with the final state.
        """
        if callback_id is None and rp_callback_id is None:
            raise ValueError("Provide callback_id or rp_callback_id.")

        def step():
            if callback_id is not None:
                res = self.get_sign_result(callback_id)
            else:
                assert rp_callback_id is not None  # for type checker
                res = self.get_sign_result_by_rp_callback_id(rp_callback_id)
            # Completed state signalled by code=="COMPLETED"
            if res.code == "COMPLETED":
                return "done", res.model_dump()
            return "in_progress", res.model_dump()

        final = poll(step, interval_s=interval_s, timeout_s=timeout_s)
        return SignStatusResponse.model_validate(final)

    def download_signed_content(self, content_id: str) -> bytes:
        """Download the signed document by content identifier.

        The return value contains the raw bytes of the signed PDF/XML/etc. The
        caller is responsible for persisting the data. The API returns
        content for up to ten years when ``toBeArchived`` is true; otherwise
        seven days.
        """
        resp = self._t.request("GET", f"/sign/content/{content_id}", stream=True)
        return resp.content

    def send_sign_request_via_qr(self, req: QrRequest) -> QrAcceptedResponse:
        """Initiate a QR signing flow via POST ``/signviaqr``."""
        resp = self._t.request("POST", "/signviaqr", json=req.model_dump())
        return QrAcceptedResponse.model_validate(resp.json())


class AsyncSigningService:
    """Asynchronous signing API wrapper."""

    def __init__(self, transport: AsyncTransport) -> None:
        self._t = transport

    async def send_sign_request(
        self,
        req: SignRequest,
        **identity: Unpack[IdentityKwargs],
    ) -> SignAcceptedResponse:
        """Asynchronously submit a signing request.

        Identity parameters must be passed via keyword arguments matching
        :class:`IdentityKwargs` (e.g. ``client_token="..."``).
        """
        headers = _auth_header(**identity)  # type: ignore[arg-type]
        resp = await self._t.request("POST", "/sign", headers=headers, json=req.model_dump())
        return SignAcceptedResponse.model_validate(resp.json())

    async def get_sign_result(self, callback_id: str) -> SignStatusResponse:
        resp = await self._t.request("GET", f"/sign/{callback_id}")
        return SignStatusResponse.model_validate(resp.json())

    async def get_sign_result_by_rp_callback_id(self, rp_callback_id: str) -> SignStatusResponse:
        resp = await self._t.request("GET", f"/sign/rpcallbackid/{rp_callback_id}")
        return SignStatusResponse.model_validate(resp.json())

    async def poll_until_signed(
        self,
        *,
        callback_id: Optional[str] = None,
        rp_callback_id: Optional[str] = None,
        interval_s: float = 2.0,
        timeout_s: float = 180.0,
    ) -> SignStatusResponse:
        """Asynchronously poll for completion of a signing operation."""
        if callback_id is None and rp_callback_id is None:
            raise ValueError("Provide callback_id or rp_callback_id.")

        async def step() -> tuple[str, dict[str, Any]]:
            if callback_id is not None:
                res = await self.get_sign_result(callback_id)
            else:
                assert rp_callback_id is not None
                res = await self.get_sign_result_by_rp_callback_id(rp_callback_id)
            if res.code == "COMPLETED":
                return "done", res.model_dump()
            return "in_progress", res.model_dump()

        # manual async polling loop as utils.poll is synchronous
        import asyncio
        deadline = asyncio.get_event_loop().time() + timeout_s
        while True:
            state, payload = await step()
            if state == "done":
                return SignStatusResponse.model_validate(payload)
            if asyncio.get_event_loop().time() >= deadline:
                raise TimeoutError("Polling timed out.")
            await asyncio.sleep(interval_s)

    async def download_signed_content(self, content_id: str) -> bytes:
        resp = await self._t.request("GET", f"/sign/content/{content_id}", stream=True)
        return await resp.aread()

    async def send_sign_request_via_qr(self, req: QrRequest) -> QrAcceptedResponse:
        resp = await self._t.request("POST", "/signviaqr", json=req.model_dump())
        return QrAcceptedResponse.model_validate(resp.json())