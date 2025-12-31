"""
Unit tests for configurable image processing pipeline.
"""

import unittest
from pathlib import Path
from PIL import Image

from src.image_pipeline.pipeline import ImagePipeline, ProcessingStep
from src.image_pipeline.presets import PipelinePresets
from src.image_pipeline.contrast import ContrastStep
from src.image_pipeline.sharpen import SharpenStep
from src.image_pipeline.quantize import QuantizeStep


class TestProcessingSteps(unittest.TestCase):
    """Test individual processing steps."""

    def setUp(self):
        """Create a test image."""
        self.test_image = Image.new("RGB", (100, 100), color="white")

    def test_contrast_step(self):
        """Test contrast adjustment step."""
        step = ContrastStep(factor=1.5)
        result = step.process(self.test_image)
        
        self.assertIsInstance(result, Image.Image)
        self.assertEqual(result.size, self.test_image.size)
        self.assertEqual(step.get_name(), "Contrast")

    def test_sharpen_step(self):
        """Test sharpening step."""
        step = SharpenStep(factor=1.2)
        result = step.process(self.test_image)
        
        self.assertIsInstance(result, Image.Image)
        self.assertEqual(result.size, self.test_image.size)
        self.assertEqual(step.get_name(), "Sharpen")

    def test_quantize_step(self):
        """Test quantization step."""
        step = QuantizeStep()
        result = step.process(self.test_image)
        
        self.assertIsInstance(result, Image.Image)
        self.assertEqual(result.size, self.test_image.size)
        self.assertEqual(step.get_name(), "Quantize")


class TestImagePipeline(unittest.TestCase):
    """Test pipeline functionality."""

    def setUp(self):
        """Create a test image."""
        self.test_image = Image.new("RGB", (100, 100), color="white")

    def test_empty_pipeline(self):
        """Test empty pipeline returns unchanged image."""
        pipeline = ImagePipeline()
        result = pipeline.process(self.test_image)
        
        self.assertEqual(len(pipeline), 0)
        self.assertIsInstance(result, Image.Image)

    def test_pipeline_with_steps(self):
        """Test pipeline with multiple steps."""
        pipeline = ImagePipeline()
        pipeline.add_step(ContrastStep(factor=1.5))
        pipeline.add_step(SharpenStep(factor=1.2))
        
        self.assertEqual(len(pipeline), 2)
        self.assertEqual(pipeline.get_steps(), ["Contrast", "Sharpen"])
        
        result = pipeline.process(self.test_image)
        self.assertIsInstance(result, Image.Image)

    def test_pipeline_chaining(self):
        """Test method chaining."""
        pipeline = (ImagePipeline()
                   .add_step(ContrastStep(factor=1.5))
                   .add_step(SharpenStep(factor=1.2)))
        
        self.assertEqual(len(pipeline), 2)

    def test_pipeline_modification(self):
        """Test adding and removing steps."""
        pipeline = ImagePipeline()
        pipeline.add_step(ContrastStep())
        pipeline.add_step(SharpenStep())
        pipeline.add_step(QuantizeStep())
        
        self.assertEqual(len(pipeline), 3)
        
        pipeline.remove_step("Sharpen")
        self.assertEqual(len(pipeline), 2)
        self.assertEqual(pipeline.get_steps(), ["Contrast", "Quantize"])
        
        pipeline.clear()
        self.assertEqual(len(pipeline), 0)


class TestPipelinePresets(unittest.TestCase):
    """Test predefined pipeline presets."""

    def test_kindle_preset(self):
        """Test Kindle preset pipeline."""
        pipeline = PipelinePresets.kindle()
        steps = pipeline.get_steps()
        
        self.assertEqual(len(pipeline), 3)
        self.assertIn("Contrast", steps)
        self.assertIn("Sharpen", steps)
        self.assertIn("Quantize", steps)

    def test_tablet_preset(self):
        """Test tablet preset pipeline."""
        pipeline = PipelinePresets.tablet()
        steps = pipeline.get_steps()
        
        self.assertEqual(len(pipeline), 2)
        self.assertIn("Contrast", steps)
        self.assertIn("Sharpen", steps)
        self.assertNotIn("Quantize", steps)

    def test_print_preset(self):
        """Test print preset pipeline."""
        pipeline = PipelinePresets.print()
        steps = pipeline.get_steps()
        
        self.assertEqual(len(pipeline), 1)
        self.assertIn("Sharpen", steps)

    def test_minimal_preset(self):
        """Test minimal preset pipeline."""
        pipeline = PipelinePresets.minimal()
        
        self.assertEqual(len(pipeline), 0)

    def test_custom_preset(self):
        """Test custom preset with parameters."""
        pipeline = PipelinePresets.custom(
            contrast=1.8,
            sharpen=1.5,
            quantize=True
        )
        
        self.assertEqual(len(pipeline), 3)
        self.assertEqual(pipeline.get_steps(), ["Contrast", "Sharpen", "Quantize"])

    def test_custom_preset_partial(self):
        """Test custom preset with partial parameters."""
        pipeline = PipelinePresets.custom(contrast=1.5)
        
        self.assertEqual(len(pipeline), 1)
        self.assertEqual(pipeline.get_steps(), ["Contrast"])

    def test_get_preset_by_name(self):
        """Test getting preset by name."""
        pipeline = PipelinePresets.get_preset("kindle")
        
        self.assertEqual(len(pipeline), 3)

    def test_get_preset_invalid_name(self):
        """Test getting preset with invalid name raises error."""
        with self.assertRaises(ValueError):
            PipelinePresets.get_preset("invalid_preset")

    def test_list_presets(self):
        """Test listing available presets."""
        presets = PipelinePresets.list_presets()
        
        self.assertIn("kindle", presets)
        self.assertIn("tablet", presets)
        self.assertIn("print", presets)
        self.assertIn("high_quality", presets)
        self.assertIn("minimal", presets)


if __name__ == "__main__":
    unittest.main()
