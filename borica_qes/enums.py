"""Enumerations used throughout the BORICA CQES wrapper.

These enums wrap the various string constants defined by BORICA's API.
Using enums prevents magic strings from leaking into consumer code and
enables type checkers and IDEs to catch invalid values early. The enums
inherit from ``str`` so they can be passed directly in JSON payloads.
"""

from __future__ import annotations

from enum import Enum


class ContentFormat(str, Enum):
    """Possible content formats for signing requests."""

    DIGEST = "DIGEST"
    BINARY_BASE64 = "BINARY_BASE64"
    TEXT = "TEXT"


class SignatureType(str, Enum):
    """Supported signature type identifiers."""

    SIGNATURE = "SIGNATURE"
    XADES_BASELINE_LTA_ENVELOPING = "XADES_BASELINE_LTA_ENVELOPING"


class HashAlgorithm(str, Enum):
    """Hash algorithms supported by BORICA for digest calculations."""

    SHA256 = "SHA256"
    SHA512 = "SHA512"


class Payer(str, Enum):
    """Indicates who pays for the signing operation."""

    CLIENT = "CLIENT"
    RELYING_PARTY = "RELYING_PARTY"


class ReportType(str, Enum):
    """Types of QLTPS evidence reports."""

    SIMPLE = "SIMPLE"
    DETAILED = "DETAILED"


class IdentifierType(str, Enum):
    """Identity types for certificate queries."""

    EGN = "EGN"
    LNC = "LNC"
    EMAIL = "EMAIL"
    PHONE = "PHONE"


class Language(str, Enum):
    """Languages accepted by the API for prompts and messages."""

    BG = "bg"
    EN = "en"


class SignStatus(str, Enum):
    """Possible states of a signature item during polling."""

    IN_PROGRESS = "IN_PROGRESS"
    SIGNED = "SIGNED"