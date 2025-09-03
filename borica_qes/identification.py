"""Remote identification and OTC signing service for BORICA.

This module implements helper methods for BORICA's remote identification
process, which allows performing electronic identification of a natural
person via a video or mobile session and subsequently issuing a one-time
certificate for signing. The API endpoints are documented in BORICA's
Remote Identification guide. These wrappers return raw JSON dictionaries
for flexibility.
"""

from __future__ import annotations

from typing import Optional, Dict, Any

from .transport import Transport, AsyncTransport
from .enums import Language


class IdentificationService:
    """Synchronous remote identification and OTC signing endpoints."""

    def __init__(self, transport: Transport) -> None:
        self._t = transport

    def start_web_session(self, request_callback_url: str, identification_reason: str) -> Dict[str, Any]:
        """Initiate a web identification session.

        Returns a dict containing ``webSessionId`` and ``resultId`` among other fields.
        """
        body = {
            "requestCallbackUrl": request_callback_url,
            "identificationReason": identification_reason,
        }
        resp = self._t.request("POST", "/identification/web/websession/start", json=body)
        return resp.json()

    def create_registration(
        self,
        web_session_id: str,
        *,
        success_url: str,
        cancel_url: str,
        user_language: Language = Language.BG,
        verify_email: bool = True,
        verify_phone: bool = True,
        device_fingerprint: Optional[Dict[str, Any]] = None,
        external_ref: Optional[str] = None,
        show_gtc_gdp: bool = True,
        show_main_info: bool = True,
    ) -> Dict[str, Any]:
        """Create a registration session for an OTC identification.

        Returns a dict containing ``sessionId`` and other metadata.
        """
        body: Dict[str, Any] = {
            "cancelUrl": cancel_url,
            "deviceFingerprint": device_fingerprint or {},
            "externalRef": external_ref or "",
            "successUrl": success_url,
            "userLanguage": user_language.value,
            "verifyEmailAddress": verify_email,
            "verifyPhoneNumber": verify_phone,
            "showGtcGdp": show_gtc_gdp,
            "showMainInfo": show_main_info,
        }
        resp = self._t.request(
            "POST",
            f"/identification/web/sessions/by-otc-request/{web_session_id}",
            json=body,
        )
        return resp.json()

    def get_web_result(
        self,
        result_id: int | str,
        process_state: str,
        session_id: str,
        *,
        only_metadata: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Fetch the result of a web identification or signing session."""
        path = f"/identification/web/{result_id}/result/{process_state}/{session_id}"
        if only_metadata is not None:
            path += f"/{str(only_metadata).lower()}"
        resp = self._t.request("GET", path)
        return resp.json()

    def start_otc_sign(
        self,
        identificator: str,
        sign_session_id: str,
        documents_for_sign: list[Dict[str, Any]],
        *,
        send_by_email: bool = True,
        success_url: str,
        cancel_url: str,
    ) -> Dict[str, Any]:
        """Begin an OTC signing session for previously identified client."""
        body = {
            "identificator": identificator,
            "signSessionId": sign_session_id,
            "documentsForSign": documents_for_sign,
            "sendSignedDocumentsByEmail": send_by_email,
            "successUrl": success_url,
            "cancelUrl": cancel_url,
        }
        resp = self._t.request("POST", "/identification/web/signsession/start", json=body)
        return resp.json()


class AsyncIdentificationService:
    """Asynchronous variant of :class:`IdentificationService`."""

    def __init__(self, transport: AsyncTransport) -> None:
        self._t = transport

    async def start_web_session(self, request_callback_url: str, identification_reason: str) -> Dict[str, Any]:
        body = {
            "requestCallbackUrl": request_callback_url,
            "identificationReason": identification_reason,
        }
        resp = await self._t.request("POST", "/identification/web/websession/start", json=body)
        return resp.json()

    async def create_registration(
        self,
        web_session_id: str,
        *,
        success_url: str,
        cancel_url: str,
        user_language: Language = Language.BG,
        verify_email: bool = True,
        verify_phone: bool = True,
        device_fingerprint: Optional[Dict[str, Any]] = None,
        external_ref: Optional[str] = None,
        show_gtc_gdp: bool = True,
        show_main_info: bool = True,
    ) -> Dict[str, Any]:
        body: Dict[str, Any] = {
            "cancelUrl": cancel_url,
            "deviceFingerprint": device_fingerprint or {},
            "externalRef": external_ref or "",
            "successUrl": success_url,
            "userLanguage": user_language.value,
            "verifyEmailAddress": verify_email,
            "verifyPhoneNumber": verify_phone,
            "showGtcGdp": show_gtc_gdp,
            "showMainInfo": show_main_info,
        }
        resp = await self._t.request(
            "POST",
            f"/identification/web/sessions/by-otc-request/{web_session_id}",
            json=body,
        )
        return resp.json()

    async def get_web_result(
        self,
        result_id: int | str,
        process_state: str,
        session_id: str,
        *,
        only_metadata: Optional[bool] = None,
    ) -> Dict[str, Any]:
        path = f"/identification/web/{result_id}/result/{process_state}/{session_id}"
        if only_metadata is not None:
            path += f"/{str(only_metadata).lower()}"
        resp = await self._t.request("GET", path)
        return resp.json()

    async def start_otc_sign(
        self,
        identificator: str,
        sign_session_id: str,
        documents_for_sign: list[Dict[str, Any]],
        *,
        send_by_email: bool = True,
        success_url: str,
        cancel_url: str,
    ) -> Dict[str, Any]:
        body = {
            "identificator": identificator,
            "signSessionId": sign_session_id,
            "documentsForSign": documents_for_sign,
            "sendSignedDocumentsByEmail": send_by_email,
            "successUrl": success_url,
            "cancelUrl": cancel_url,
        }
        resp = await self._t.request("POST", "/identification/web/signsession/start", json=body)
        return resp.json()