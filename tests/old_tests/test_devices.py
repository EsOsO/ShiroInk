"""
Unit tests for device specifications and device-specific presets.
"""

import unittest
from pathlib import Path
from PIL import Image

from src.image_pipeline.devices import DeviceSpecs, DeviceSpec, DisplayType
from src.image_pipeline.presets import PipelinePresets


class TestDeviceSpecs(unittest.TestCase):
    """Test device specification functionality."""

    def test_get_all_devices(self):
        """Test getting all device specifications."""
        devices = DeviceSpecs.get_all_devices()
        
        self.assertIsInstance(devices, dict)
        self.assertGreater(len(devices), 0)
        
        # Check that all expected brands are present
        device_keys = list(devices.keys())
        self.assertTrue(any(k.startswith("kindle") for k in device_keys))
        self.assertTrue(any(k.startswith("kobo") for k in device_keys))
        self.assertTrue(any(k.startswith("tolino") for k in device_keys))
        self.assertTrue(any(k.startswith("pocketbook") for k in device_keys))
        self.assertTrue(any(k.startswith("ipad") for k in device_keys))

    def test_get_device_kindle(self):
        """Test getting Kindle device specification."""
        device = DeviceSpecs.get_device("kindle_paperwhite_11")
        
        self.assertIsInstance(device, DeviceSpec)
        self.assertEqual(device.resolution, (1236, 1648))
        self.assertEqual(device.display_type, DisplayType.EINK)
        self.assertEqual(device.ppi, 300)
        self.assertIn("6.8", device.description)

    def test_get_device_kobo(self):
        """Test getting Kobo device specification."""
        device = DeviceSpecs.get_device("kobo_libra_2")
        
        self.assertIsInstance(device, DeviceSpec)
        self.assertEqual(device.resolution, (1264, 1680))
        self.assertEqual(device.display_type, DisplayType.EINK)

    def test_get_device_tolino(self):
        """Test getting Tolino device specification."""
        device = DeviceSpecs.get_device("tolino_vision_6")
        
        self.assertIsInstance(device, DeviceSpec)
        self.assertEqual(device.resolution, (1264, 1680))
        self.assertEqual(device.display_type, DisplayType.EINK)

    def test_get_device_pocketbook(self):
        """Test getting PocketBook device specification."""
        device = DeviceSpecs.get_device("pocketbook_era")
        
        self.assertIsInstance(device, DeviceSpec)
        self.assertEqual(device.resolution, (1072, 1448))
        self.assertEqual(device.display_type, DisplayType.EINK)

    def test_get_device_pocketbook_color(self):
        """Test getting PocketBook color device specification."""
        device = DeviceSpecs.get_device("pocketbook_inkpad_color_3")
        
        self.assertIsInstance(device, DeviceSpec)
        self.assertEqual(device.resolution, (1236, 1648))
        self.assertEqual(device.display_type, DisplayType.EINK)
        self.assertIn("color", device.description.lower())

    def test_get_device_ipad(self):
        """Test getting iPad device specification."""
        device = DeviceSpecs.get_device("ipad_pro_11")
        
        self.assertIsInstance(device, DeviceSpec)
        self.assertEqual(device.resolution, (1668, 2388))
        self.assertEqual(device.display_type, DisplayType.RETINA)

    def test_get_device_invalid(self):
        """Test getting invalid device raises KeyError."""
        with self.assertRaises(KeyError):
            DeviceSpecs.get_device("nonexistent_device")

    def test_list_devices(self):
        """Test listing all device keys."""
        devices = DeviceSpecs.list_devices()
        
        self.assertIsInstance(devices, list)
        self.assertGreater(len(devices), 0)
        self.assertIn("kindle_paperwhite_11", devices)
        self.assertIn("kobo_libra_2", devices)
        self.assertIn("ipad_pro_11", devices)

    def test_get_devices_by_brand_kindle(self):
        """Test getting devices by Kindle brand."""
        devices = DeviceSpecs.get_devices_by_brand("kindle")
        
        self.assertIsInstance(devices, dict)
        self.assertGreater(len(devices), 0)
        
        for key in devices.keys():
            self.assertTrue(key.startswith("kindle"))

    def test_get_devices_by_brand_kobo(self):
        """Test getting devices by Kobo brand."""
        devices = DeviceSpecs.get_devices_by_brand("kobo")
        
        self.assertIsInstance(devices, dict)
        self.assertGreater(len(devices), 0)
        
        for key in devices.keys():
            self.assertTrue(key.startswith("kobo"))

    def test_get_devices_by_brand_ipad(self):
        """Test getting devices by iPad brand."""
        devices = DeviceSpecs.get_devices_by_brand("ipad")
        
        self.assertIsInstance(devices, dict)
        self.assertGreater(len(devices), 0)
        
        for key in devices.keys():
            self.assertTrue(key.startswith("ipad"))

    def test_device_spec_repr(self):
        """Test device specification string representation."""
        device = DeviceSpecs.get_device("kindle_paperwhite_11")
        repr_str = repr(device)
        
        self.assertIn("1236x1648", repr_str)
        self.assertIn("e-ink", repr_str)


class TestDevicePresets(unittest.TestCase):
    """Test device-specific pipeline presets."""

    def test_kobo_preset(self):
        """Test Kobo preset pipeline."""
        pipeline = PipelinePresets.kobo()
        steps = pipeline.get_steps()
        
        self.assertEqual(len(pipeline), 3)
        self.assertIn("Contrast", steps)
        self.assertIn("Sharpen", steps)
        self.assertIn("Quantize", steps)

    def test_tolino_preset(self):
        """Test Tolino preset pipeline."""
        pipeline = PipelinePresets.tolino()
        steps = pipeline.get_steps()
        
        self.assertEqual(len(pipeline), 3)
        self.assertIn("Contrast", steps)
        self.assertIn("Sharpen", steps)
        self.assertIn("Quantize", steps)

    def test_pocketbook_preset(self):
        """Test PocketBook preset pipeline."""
        pipeline = PipelinePresets.pocketbook()
        steps = pipeline.get_steps()
        
        self.assertEqual(len(pipeline), 3)
        self.assertIn("Contrast", steps)
        self.assertIn("Sharpen", steps)
        self.assertIn("Quantize", steps)

    def test_pocketbook_color_preset(self):
        """Test PocketBook color preset pipeline."""
        pipeline = PipelinePresets.pocketbook_color()
        steps = pipeline.get_steps()
        
        self.assertEqual(len(pipeline), 2)
        self.assertIn("Contrast", steps)
        self.assertIn("Sharpen", steps)
        self.assertNotIn("Quantize", steps)  # Color preserving

    def test_ipad_preset(self):
        """Test iPad preset pipeline."""
        pipeline = PipelinePresets.ipad()
        steps = pipeline.get_steps()
        
        self.assertEqual(len(pipeline), 2)
        self.assertIn("Contrast", steps)
        self.assertIn("Sharpen", steps)
        self.assertNotIn("Quantize", steps)  # Full color

    def test_eink_preset(self):
        """Test generic e-ink preset pipeline."""
        pipeline = PipelinePresets.eink()
        steps = pipeline.get_steps()
        
        self.assertEqual(len(pipeline), 3)
        self.assertIn("Contrast", steps)
        self.assertIn("Sharpen", steps)
        self.assertIn("Quantize", steps)

    def test_get_preset_by_name_device_specific(self):
        """Test getting device-specific preset by name."""
        pipeline = PipelinePresets.get_preset("kobo")
        self.assertEqual(len(pipeline), 3)
        
        pipeline = PipelinePresets.get_preset("ipad")
        self.assertEqual(len(pipeline), 2)

    def test_list_presets_includes_devices(self):
        """Test that preset list includes device-specific presets."""
        presets = PipelinePresets.list_presets()
        
        # Generic presets
        self.assertIn("kindle", presets)
        self.assertIn("tablet", presets)
        
        # Device-specific presets
        self.assertIn("kobo", presets)
        self.assertIn("tolino", presets)
        self.assertIn("pocketbook", presets)
        self.assertIn("pocketbook_color", presets)
        self.assertIn("ipad", presets)
        self.assertIn("eink", presets)

    def test_device_presets_process_image(self):
        """Test that device presets can process images."""
        test_image = Image.new("RGB", (100, 100), color="white")
        
        presets_to_test = [
            "kobo", "tolino", "pocketbook", 
            "pocketbook_color", "ipad", "eink"
        ]
        
        for preset_name in presets_to_test:
            with self.subTest(preset=preset_name):
                pipeline = PipelinePresets.get_preset(preset_name)
                result = pipeline.process(test_image)
                
                self.assertIsInstance(result, Image.Image)
                self.assertEqual(result.size, test_image.size)


class TestDisplayTypes(unittest.TestCase):
    """Test display type enumeration."""

    def test_display_types_exist(self):
        """Test that all display types are defined."""
        self.assertEqual(DisplayType.EINK.value, "e-ink")
        self.assertEqual(DisplayType.LCD.value, "lcd")
        self.assertEqual(DisplayType.OLED.value, "oled")
        self.assertEqual(DisplayType.RETINA.value, "retina")

    def test_device_display_types(self):
        """Test that devices have correct display types."""
        # E-ink devices
        kindle = DeviceSpecs.get_device("kindle_paperwhite_11")
        self.assertEqual(kindle.display_type, DisplayType.EINK)
        
        kobo = DeviceSpecs.get_device("kobo_libra_2")
        self.assertEqual(kobo.display_type, DisplayType.EINK)
        
        # Retina devices
        ipad = DeviceSpecs.get_device("ipad_pro_11")
        self.assertEqual(ipad.display_type, DisplayType.RETINA)


if __name__ == "__main__":
    unittest.main()
