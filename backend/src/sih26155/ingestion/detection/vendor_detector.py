from dataclasses import dataclass

from sih26155.core.schema.enums import Vendor


@dataclass(frozen=True)
class VendorDetectionResult:
    """
    Result of deterministic vendor detection.

    The detector identifies the most likely vendor from configuration
    signatures. It does not parse or interpret security semantics.
    """

    vendor: Vendor
    confidence: float
    matched_signatures: tuple[str, ...] = ()


class VendorDetectionError(Exception):
    """Raised when vendor detection cannot be performed."""


# Strong, vendor-specific configuration signatures.
#
# These are intentionally conservative. A false positive is worse than
# returning UNKNOWN because UNKNOWN configurations can later be handled
# by the AI-assisted semantic mapping layer.
VENDOR_SIGNATURES: dict[Vendor, tuple[str, ...]] = {
    Vendor.CISCO: (
        "version ",
        "hostname ",
        "ip ssh ",
        "line vty ",
        "enable secret ",
        "service timestamps ",
        "logging ",
    ),
    Vendor.JUNIPER: (
        "set system ",
        "set interfaces ",
        "set security ",
        "set protocols ",
        "set routing-options ",
    ),
    Vendor.PALO_ALTO: (
        "<config>",
        "<devices>",
        "<entry name=",
        "<deviceconfig>",
        "<vsys>",
        "<security>",
    ),
}


def detect_vendor(config: str) -> VendorDetectionResult:
    """
    Detect the vendor associated with a network configuration.

    Detection is deterministic and signature-based.

    Args:
        config:
            Raw network device configuration text.

    Returns:
        VendorDetectionResult containing the detected vendor,
        confidence, and signatures that matched.

    Raises:
        VendorDetectionError:
            If the configuration is not a string or is empty.
    """

    if not isinstance(config, str):
        raise VendorDetectionError(
            "Configuration must be provided as a string."
        )

    normalized = config.strip().lower()

    if not normalized:
        raise VendorDetectionError(
            "Configuration cannot be empty."
        )

    scores: dict[Vendor, int] = {}

    for vendor, signatures in VENDOR_SIGNATURES.items():
        matches = sum(
            1
            for signature in signatures
            if signature.lower() in normalized
        )

        if matches:
            scores[vendor] = matches

    if not scores:
        return VendorDetectionResult(
            vendor=Vendor.UNKNOWN,
            confidence=0.0,
            matched_signatures=(),
        )

    # Select the vendor with the strongest number of matching signatures.
    detected_vendor = max(scores, key=scores.get)
    matched_signatures = tuple(
        signature
        for signature in VENDOR_SIGNATURES[detected_vendor]
        if signature.lower() in normalized
    )

    total_signatures = len(VENDOR_SIGNATURES[detected_vendor])
    confidence = min(
        len(matched_signatures) / total_signatures,
        1.0,
    )

    return VendorDetectionResult(
        vendor=detected_vendor,
        confidence=confidence,
        matched_signatures=matched_signatures,
    )