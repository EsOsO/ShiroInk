"""
Unit tests for device specifications.

Tests cover:
- Device specification retrieval and validation
- New device fields (color_support, color_gamut, bit_depth, etc.)
- Device filtering and grouping
"""

import pytest
from src.image_pipeline.devices import DeviceSpecs, DeviceSpec, DisplayType, ColorGamut


class TestDeviceSpecRetrieval:
    """Test device specification retrieval operations."""

    def test_get_all_devices_returns_dict(self):
        """All devices should be returned as a dictionary."""
        devices = DeviceSpecs.get_all_devices()
        
        assert isinstance(devices, dict)
        assert len(devices) > 0

    def test_all_brands_present(self):
        """All major brands should have device specifications."""
        devices = DeviceSpecs.get_all_devices()
        device_keys = list(devices.keys())
        
        assert any(k.startswith("kindle") for k in device_keys)
        assert any(k.startswith("kobo") for k in device_keys)
        assert any(k.startswith("tolino") for k in device_keys)
        assert any(k.startswith("pocketbook") for k in device_keys)
        assert any(k.startswith("ipad") for k in device_keys)

    def test_list_devices_returns_list(self):
        """List devices should return a list of device keys."""
        devices = DeviceSpecs.list_devices()
        
        assert isinstance(devices, list)
        assert len(devices) > 0
        assert "kindle_paperwhite_11" in devices
        assert "kobo_libra_2" in devices
        assert "ipad_pro_11" in devices

    def test_get_device_invalid_raises_key_error(self):
        """Getting an invalid device should raise KeyError."""
        with pytest.raises(KeyError):
            DeviceSpecs.get_device("nonexistent_device")


class TestDeviceSpecFields:
    """Test that all devices have required fields populated correctly."""

    @pytest.fixture(params=DeviceSpecs.list_devices())
    def device_spec(self, request):
        """Parametrized fixture that yields each device spec."""
        return DeviceSpecs.get_device(request.param)

    def test_all_devices_have_name(self, device_spec):
        """All devices must have a name."""
        assert device_spec.name
        assert isinstance(device_spec.name, str)

    def test_all_devices_have_resolution(self, device_spec):
        """All devices must have a valid resolution."""
        assert device_spec.resolution
        assert len(device_spec.resolution) == 2
        assert device_spec.resolution[0] > 0
        assert device_spec.resolution[1] > 0

    def test_all_devices_have_display_type(self, device_spec):
        """All devices must have a display type."""
        assert device_spec.display_type
        assert isinstance(device_spec.display_type, DisplayType)

    def test_all_devices_have_ppi(self, device_spec):
        """All devices must have a valid PPI."""
        assert device_spec.ppi > 0
        assert device_spec.ppi <= 500  # Reasonable upper bound

    def test_all_devices_have_screen_size(self, device_spec):
        """All devices must have a valid screen size."""
        assert device_spec.screen_size_inches > 0
        assert device_spec.screen_size_inches <= 15  # Reasonable upper bound

    def test_all_devices_have_color_support_flag(self, device_spec):
        """All devices must have color_support defined."""
        assert isinstance(device_spec.color_support, bool)

    def test_all_devices_have_color_gamut(self, device_spec):
        """All devices must have color_gamut defined."""
        if device_spec.color_support:
            assert device_spec.color_gamut is not None
            assert isinstance(device_spec.color_gamut, ColorGamut)
        else:
            # B&W devices should have NONE or None
            assert device_spec.color_gamut in (None, ColorGamut.NONE)

    def test_all_devices_have_bit_depth(self, device_spec):
        """All devices must have a valid bit depth."""
        assert device_spec.bit_depth > 0
        assert device_spec.bit_depth in (4, 8, 12, 16, 24)  # Common bit depths

    def test_all_devices_have_max_colors(self, device_spec):
        """All devices must have max_colors defined."""
        if device_spec.color_support:
            assert device_spec.max_colors is not None
            assert device_spec.max_colors > 0
        # B&W devices may have max_colors for grayscale levels

    def test_all_devices_have_recommended_pipeline(self, device_spec):
        """All devices must have a recommended pipeline."""
        assert device_spec.recommended_pipeline
        assert isinstance(device_spec.recommended_pipeline, str)

    def test_all_devices_have_description(self, device_spec):
        """All devices must have a description."""
        assert device_spec.description
        assert isinstance(device_spec.description, str)


class TestSpecificDevices:
    """Test specific device configurations."""

    def test_kindle_paperwhite_11_spec(self):
        """Test Kindle Paperwhite 11th Gen specifications."""
        device = DeviceSpecs.get_device("kindle_paperwhite_11")
        
        assert device.resolution == (1236, 1648)
        assert device.display_type == DisplayType.EINK
        assert device.ppi == 300
        assert device.screen_size_inches == 6.8
        assert device.color_support is False
        assert device.bit_depth == 4
        assert device.max_colors == 16
        assert device.recommended_pipeline == "kindle"

    def test_pocketbook_inkpad_color_3_spec(self):
        """Test PocketBook InkPad Color 3 specifications."""
        device = DeviceSpecs.get_device("pocketbook_inkpad_color_3")
        
        assert device.resolution == (1236, 1648)
        assert device.display_type == DisplayType.EINK
        assert device.color_support is True
        assert device.color_gamut == ColorGamut.SRGB
        assert device.bit_depth == 12
        assert device.max_colors == 4096
        assert device.recommended_pipeline == "pocketbook_color"

    def test_ipad_pro_11_spec(self):
        """Test iPad Pro 11\" specifications."""
        device = DeviceSpecs.get_device("ipad_pro_11")
        
        assert device.resolution == (1668, 2388)
        assert device.display_type == DisplayType.RETINA
        assert device.screen_size_inches == 11.0
        assert device.color_support is True
        assert device.color_gamut == ColorGamut.DCI_P3
        assert device.bit_depth == 24
        assert device.max_colors == 16777216
        assert device.recommended_pipeline == "ipad"


class TestDeviceFiltering:
    """Test device filtering and grouping operations."""

    def test_get_devices_by_brand_kindle(self):
        """Filter devices by Kindle brand."""
        devices = DeviceSpecs.get_devices_by_brand("kindle")
        
        assert isinstance(devices, dict)
        assert len(devices) > 0
        
        for key in devices.keys():
            assert key.startswith("kindle")

    def test_get_devices_by_brand_kobo(self):
        """Filter devices by Kobo brand."""
        devices = DeviceSpecs.get_devices_by_brand("kobo")
        
        assert isinstance(devices, dict)
        assert len(devices) > 0
        
        for key in devices.keys():
            assert key.startswith("kobo")

    def test_get_devices_by_brand_ipad(self):
        """Filter devices by iPad brand."""
        devices = DeviceSpecs.get_devices_by_brand("ipad")
        
        assert isinstance(devices, dict)
        assert len(devices) > 0
        
        for key in devices.keys():
            assert key.startswith("ipad")


class TestDisplayType:
    """Test display type enumeration."""

    def test_display_type_values(self):
        """Verify display type enum values."""
        assert DisplayType.EINK.value == "e-ink"
        assert DisplayType.LCD.value == "lcd"
        assert DisplayType.OLED.value == "oled"
        assert DisplayType.RETINA.value == "retina"

    def test_eink_devices_have_correct_type(self):
        """E-ink devices should have EINK display type."""
        kindle = DeviceSpecs.get_device("kindle_paperwhite_11")
        kobo = DeviceSpecs.get_device("kobo_libra_2")
        tolino = DeviceSpecs.get_device("tolino_vision_6")
        
        assert kindle.display_type == DisplayType.EINK
        assert kobo.display_type == DisplayType.EINK
        assert tolino.display_type == DisplayType.EINK

    def test_retina_devices_have_correct_type(self):
        """iPad devices should have RETINA display type."""
        ipad = DeviceSpecs.get_device("ipad_pro_11")
        
        assert ipad.display_type == DisplayType.RETINA


class TestColorGamut:
    """Test color gamut enumeration."""

    def test_color_gamut_values(self):
        """Verify color gamut enum values."""
        assert ColorGamut.NONE.value is None
        assert ColorGamut.SRGB.value == "sRGB"
        assert ColorGamut.DCI_P3.value == "DCI-P3"
        assert ColorGamut.ADOBE_RGB.value == "Adobe RGB"

    def test_bw_devices_have_no_gamut(self):
        """B&W devices should have no color gamut."""
        kindle = DeviceSpecs.get_device("kindle_paperwhite_11")
        kobo = DeviceSpecs.get_device("kobo_libra_2")
        
        assert kindle.color_gamut in (None, ColorGamut.NONE)
        assert kobo.color_gamut in (None, ColorGamut.NONE)

    def test_color_devices_have_valid_gamut(self):
        """Color devices should have a valid color gamut."""
        pocketbook_color = DeviceSpecs.get_device("pocketbook_inkpad_color_3")
        ipad_pro = DeviceSpecs.get_device("ipad_pro_11")
        
        assert pocketbook_color.color_gamut == ColorGamut.SRGB
        assert ipad_pro.color_gamut == ColorGamut.DCI_P3


class TestDeviceRepresentation:
    """Test device string representation."""

    def test_device_spec_repr(self):
        """Device repr should contain key information."""
        device = DeviceSpecs.get_device("kindle_paperwhite_11")
        repr_str = repr(device)
        
        assert "1236x1648" in repr_str
        assert "e-ink" in repr_str
