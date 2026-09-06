import pytest

from sih26155.core.schema.enums import Vendor
from sih26155.ingestion.detection.vendor_detector import (
    VendorDetectionError,
    detect_vendor,
)


def test_detect_cisco():
    config = """
    hostname EDGE-01
    !
    ip ssh version 2
    ip http server
    !
    line vty 0 4
     transport input ssh
    !
    """

    result = detect_vendor(config)

    assert result.vendor == Vendor.CISCO
    assert result.confidence > 0
    assert len(result.matched_signatures) > 0


def test_detect_juniper():
    config = """
    set system host-name EDGE-JUNOS
    set system services ssh protocol-version v2
    set system services telnet
    set interfaces ge-0/0/0 unit 0 family inet
    """

    result = detect_vendor(config)

    assert result.vendor == Vendor.JUNIPER
    assert result.confidence > 0
    assert len(result.matched_signatures) > 0


def test_detect_palo_alto():
    config = """
    <config>
      <devices>
        <entry name="localhost.localdomain">
          <deviceconfig>
          </deviceconfig>
        </entry>
      </devices>
    </config>
    """

    result = detect_vendor(config)

    assert result.vendor == Vendor.PALO_ALTO
    assert result.confidence > 0
    assert len(result.matched_signatures) > 0


def test_detect_unknown():
    config = """
    this is not a recognized network configuration
    random configuration syntax
    """

    result = detect_vendor(config)

    assert result.vendor == Vendor.UNKNOWN
    assert result.confidence == 0.0
    assert result.matched_signatures == ()


def test_empty_configuration():
    with pytest.raises(VendorDetectionError):
        detect_vendor("")


def test_whitespace_only_configuration():
    with pytest.raises(VendorDetectionError):
        detect_vendor("   ")


def test_non_string_configuration():
    with pytest.raises(VendorDetectionError):
        detect_vendor(None)