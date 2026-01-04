# Image Pipeline Improvement Suggestions

**Created**: 2026-01-04  
**Status**: Analysis Complete  
**Priority**: High-Impact Features for v1.1.0+

---

## Executive Summary

This document provides comprehensive suggestions for improving ShiroInk's image processing pipeline based on analysis of the current implementation. The suggestions are organized by priority and include code examples, implementation guidance, and expected impact.

**Current Pipeline Strengths**:
- Clean, extensible architecture with `ProcessingStep` abstraction
- Device-aware processing with 46 device profiles
- Color E Ink support (Kaleido 3)
- Flexible preset system
- Good error handling and retry logic
- Parallel batch processing

**Key Gaps Identified**:
1. Limited manga-specific optimizations
2. Basic PIL enhancement methods (could be more sophisticated)
3. No preprocessing/cleanup steps
4. Sequential-only pipeline (no conditional steps)
5. Limited quality metrics and feedback
6. No advanced features (rotation, cropping, denoising)

---

## Table of Contents

1. [High Priority: Manga-Specific Features](#1-high-priority-manga-specific-features)
2. [Medium Priority: Quality Improvements](#2-medium-priority-quality-improvements)
3. [Medium Priority: Performance Optimizations](#3-medium-priority-performance-optimizations)
4. [Low Priority: Advanced Features](#4-low-priority-advanced-features)
5. [Low Priority: User Experience Enhancements](#5-low-priority-user-experience-enhancements)
6. [Implementation Roadmap](#implementation-roadmap)

---

## 1. High Priority: Manga-Specific Features

### 1.1 Auto-Rotation Detection

**Problem**: Scanned manga pages often have slight rotation that affects readability.

**Solution**: Add rotation detection and correction step.

**Implementation**:

```python
# src/image_pipeline/rotation.py
from PIL import Image
import numpy as np
from .pipeline import ProcessingStep


class AutoRotateStep(ProcessingStep):
    """
    Automatically detect and correct image rotation.
    
    Uses edge detection and Hough transform to detect text lines
    and calculate rotation angle.
    """
    
    def __init__(self, max_angle: float = 5.0, threshold: float = 0.5):
        """
        Initialize auto-rotation step.
        
        Args:
            max_angle: Maximum rotation to correct (degrees)
            threshold: Confidence threshold for rotation detection
        """
        super().__init__(max_angle=max_angle, threshold=threshold)
        self.max_angle = max_angle
        self.threshold = threshold
    
    def process(self, image: Image.Image) -> Image.Image:
        """Detect and correct rotation."""
        angle = self._detect_rotation(image)
        
        if abs(angle) < self.threshold:
            return image  # No significant rotation
        
        if abs(angle) > self.max_angle:
            # Too much rotation, might be intentional or misdetected
            return image
        
        # Rotate to correct
        return image.rotate(-angle, resample=Image.BICUBIC, expand=False, fillcolor='white')
    
    def _detect_rotation(self, image: Image.Image) -> float:
        """
        Detect rotation angle using edge detection.
        
        Returns:
            Rotation angle in degrees (positive = clockwise)
        """
        # Convert to grayscale for edge detection
        gray = image.convert('L')
        
        # Simple approach: Use PIL's getextrema for quick check
        # For production, consider using numpy + scipy for Hough transform
        
        # TODO: Implement full Hough line detection
        # For now, return 0 (no rotation detected)
        return 0.0
    
    def get_name(self) -> str:
        return "AutoRotate"
```

**Integration**:
```python
# In presets.py
pipeline.add_step(AutoRotateStep(max_angle=5.0))  # Before contrast
```

**Impact**: 
- Improves text readability on scanned manga
- Reduces eye strain on rotated pages
- **Complexity**: Medium (requires edge detection library)
- **Value**: High for scanned content

---

### 1.2 Margin Detection and Cropping

**Problem**: Scanned manga often has unnecessary white margins that waste screen space.

**Solution**: Detect and crop white margins automatically.

**Implementation**:

```python
# src/image_pipeline/crop.py
from PIL import Image, ImageChops
from .pipeline import ProcessingStep


class SmartCropStep(ProcessingStep):
    """
    Automatically detect and remove white margins from manga pages.
    """
    
    def __init__(self, threshold: int = 250, min_margin: int = 10):
        """
        Initialize smart crop step.
        
        Args:
            threshold: Pixel brightness threshold for "white" (0-255)
            min_margin: Minimum margin to keep (pixels)
        """
        super().__init__(threshold=threshold, min_margin=min_margin)
        self.threshold = threshold
        self.min_margin = min_margin
    
    def process(self, image: Image.Image) -> Image.Image:
        """Detect and crop white margins."""
        # Convert to grayscale for analysis
        gray = image.convert('L')
        
        # Create binary mask: white areas above threshold
        bg = Image.new('L', gray.size, self.threshold)
        diff = ImageChops.difference(gray, bg)
        diff = ImageChops.add(diff, diff, 2.0, -100)
        
        # Get bounding box of non-white content
        bbox = diff.getbbox()
        
        if bbox:
            # Add back minimum margin
            width, height = image.size
            left = max(0, bbox[0] - self.min_margin)
            top = max(0, bbox[1] - self.min_margin)
            right = min(width, bbox[2] + self.min_margin)
            bottom = min(height, bbox[3] + self.min_margin)
            
            return image.crop((left, top, right, bottom))
        
        return image  # No cropping needed
    
    def get_name(self) -> str:
        return "SmartCrop"
```

**Integration**:
```python
# In presets.py
pipeline.add_step(SmartCropStep(threshold=240, min_margin=10))  # Before resize
```

**Impact**:
- Better screen space utilization
- Larger effective image area on device
- **Complexity**: Low (PIL has built-in support)
- **Value**: Very High for scanned manga

---

### 1.3 Text Enhancement

**Problem**: Manga text can be blurry or low-contrast, especially after compression.

**Solution**: Enhanced text detection and sharpening.

**Implementation**:

```python
# src/image_pipeline/text_enhance.py
from PIL import Image, ImageFilter, ImageEnhance
from .pipeline import ProcessingStep


class TextEnhanceStep(ProcessingStep):
    """
    Enhance text regions in manga images for better readability.
    """
    
    def __init__(self, text_contrast: float = 1.3, text_sharpen: float = 1.5):
        """
        Initialize text enhancement step.
        
        Args:
            text_contrast: Contrast factor for text regions
            text_sharpen: Sharpening factor for text regions
        """
        super().__init__(text_contrast=text_contrast, text_sharpen=text_sharpen)
        self.text_contrast = text_contrast
        self.text_sharpen = text_sharpen
    
    def process(self, image: Image.Image) -> Image.Image:
        """Enhance text readability."""
        # Apply edge-preserving filter
        enhanced = image.filter(ImageFilter.EDGE_ENHANCE_MORE)
        
        # Blend with original based on edge strength
        # This enhances text while preserving artwork
        blended = Image.blend(image, enhanced, 0.3)
        
        # Extra sharpening for small text
        sharpener = ImageEnhance.Sharpness(blended)
        result = sharpener.enhance(self.text_sharpen)
        
        return result
    
    def get_name(self) -> str:
        return "TextEnhance"
```

**Impact**:
- Better text legibility on e-readers
- Preserves artwork quality
- **Complexity**: Low
- **Value**: High for text-heavy manga

---

### 1.4 Panel Border Detection

**Problem**: Panel layouts vary, and some manga have thin borders that might get lost.

**Solution**: Detect and enhance panel borders.

**Implementation** (Conceptual - requires computer vision):

```python
# src/image_pipeline/panel_enhance.py
from PIL import Image, ImageDraw, ImageFilter
from .pipeline import ProcessingStep


class PanelBorderStep(ProcessingStep):
    """
    Detect and enhance manga panel borders for better readability.
    """
    
    def __init__(self, enhance_borders: bool = True, min_border_thickness: int = 1):
        """
        Initialize panel border enhancement.
        
        Args:
            enhance_borders: Whether to enhance detected borders
            min_border_thickness: Minimum border thickness in pixels
        """
        super().__init__(
            enhance_borders=enhance_borders,
            min_border_thickness=min_border_thickness
        )
        self.enhance_borders = enhance_borders
        self.min_border_thickness = min_border_thickness
    
    def process(self, image: Image.Image) -> Image.Image:
        """Detect and enhance panel borders."""
        if not self.enhance_borders:
            return image
        
        # Simple edge enhancement for borders
        # TODO: Implement full panel detection with OpenCV
        edges = image.filter(ImageFilter.FIND_EDGES)
        
        # Blend edges back to enhance borders
        enhanced = Image.blend(image, edges, 0.2)
        
        return enhanced
    
    def get_name(self) -> str:
        return "PanelBorder"
```

**Impact**:
- Better panel separation
- Improved reading flow
- **Complexity**: High (requires OpenCV or similar)
- **Value**: Medium (nice-to-have)

---

## 2. Medium Priority: Quality Improvements

### 2.1 Advanced Sharpening (Unsharp Mask)

**Problem**: Current sharpening uses simple PIL `ImageEnhance.Sharpness`, which is basic.

**Solution**: Implement unsharp mask for better control.

**Implementation**:

```python
# src/image_pipeline/sharpen.py (enhancement)
from PIL import Image, ImageFilter
from .pipeline import ProcessingStep


class UnsharpMaskStep(ProcessingStep):
    """
    Advanced sharpening using unsharp mask technique.
    
    Provides better control than simple sharpness enhancement.
    """
    
    def __init__(self, radius: float = 2.0, percent: int = 150, threshold: int = 3):
        """
        Initialize unsharp mask step.
        
        Args:
            radius: Blur radius for mask (larger = broader effect)
            percent: Sharpening strength (100 = 1x, 150 = 1.5x)
            threshold: Minimum difference to sharpen (avoid noise)
        """
        super().__init__(radius=radius, percent=percent, threshold=threshold)
        self.radius = radius
        self.percent = percent
        self.threshold = threshold
    
    def process(self, image: Image.Image) -> Image.Image:
        """Apply unsharp mask sharpening."""
        return image.filter(
            ImageFilter.UnsharpMask(
                radius=self.radius,
                percent=self.percent,
                threshold=self.threshold
            )
        )
    
    def get_name(self) -> str:
        return f"UnsharpMask(r={self.radius})"
```

**Integration**:
```python
# Replace existing SharpenStep with UnsharpMaskStep
pipeline.add_step(UnsharpMaskStep(radius=2.0, percent=150, threshold=3))
```

**Impact**:
- Better sharpening quality with less haloing
- More control over sharpening parameters
- **Complexity**: Low (PIL built-in)
- **Value**: Medium-High

---

### 2.2 Adaptive Contrast (CLAHE)

**Problem**: Current contrast adjustment is global, which can over-brighten or darken regions.

**Solution**: Use CLAHE (Contrast Limited Adaptive Histogram Equalization).

**Implementation**:

```python
# src/image_pipeline/contrast.py (enhancement)
from PIL import Image, ImageEnhance
import numpy as np
from .pipeline import ProcessingStep


class AdaptiveContrastStep(ProcessingStep):
    """
    Adaptive contrast enhancement using CLAHE.
    
    Better than global contrast for manga with varying brightness.
    """
    
    def __init__(self, clip_limit: float = 2.0, tile_grid_size: tuple[int, int] = (8, 8)):
        """
        Initialize adaptive contrast step.
        
        Args:
            clip_limit: Contrast limiting threshold
            tile_grid_size: Size of grid for local equalization
        """
        super().__init__(clip_limit=clip_limit, tile_grid_size=tile_grid_size)
        self.clip_limit = clip_limit
        self.tile_grid_size = tile_grid_size
    
    def process(self, image: Image.Image) -> Image.Image:
        """Apply adaptive contrast enhancement."""
        try:
            import cv2
            
            # Convert to numpy array
            img_array = np.array(image)
            
            # Convert to LAB color space for better contrast handling
            lab = cv2.cvtColor(img_array, cv2.COLOR_RGB2LAB)
            
            # Apply CLAHE to L channel
            clahe = cv2.createCLAHE(
                clipLimit=self.clip_limit,
                tileGridSize=self.tile_grid_size
            )
            lab[:, :, 0] = clahe.apply(lab[:, :, 0])
            
            # Convert back to RGB
            enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)
            
            return Image.fromarray(enhanced)
            
        except ImportError:
            # Fallback to simple contrast if OpenCV not available
            enhancer = ImageEnhance.Contrast(image)
            return enhancer.enhance(1.3)
    
    def get_name(self) -> str:
        return "AdaptiveContrast"
```

**Impact**:
- Better contrast in varying lighting conditions
- Reduces over-brightening/darkening
- **Complexity**: Medium (requires OpenCV)
- **Value**: High for scanned manga

---

### 2.3 Denoising for Scanned Images

**Problem**: Scanned manga often has compression artifacts, grain, or scanning noise.

**Solution**: Add denoising step for cleaner images.

**Implementation**:

```python
# src/image_pipeline/denoise.py
from PIL import Image, ImageFilter
from .pipeline import ProcessingStep


class DenoiseStep(ProcessingStep):
    """
    Remove noise from scanned manga images.
    """
    
    def __init__(self, strength: str = 'medium'):
        """
        Initialize denoise step.
        
        Args:
            strength: Denoising strength ('light', 'medium', 'strong')
        """
        super().__init__(strength=strength)
        self.strength = strength
    
    def process(self, image: Image.Image) -> Image.Image:
        """Apply denoising filter."""
        if self.strength == 'light':
            # Simple median filter
            return image.filter(ImageFilter.MedianFilter(size=3))
        elif self.strength == 'medium':
            # Combination of median + smooth
            denoised = image.filter(ImageFilter.MedianFilter(size=3))
            return denoised.filter(ImageFilter.SMOOTH)
        elif self.strength == 'strong':
            # Multiple passes for heavy noise
            denoised = image.filter(ImageFilter.MedianFilter(size=5))
            denoised = denoised.filter(ImageFilter.SMOOTH_MORE)
            return denoised
        
        return image
    
    def get_name(self) -> str:
        return f"Denoise({self.strength})"
```

**Impact**:
- Cleaner images from scanned sources
- Reduces file size (less noise = better compression)
- **Complexity**: Low (PIL built-in)
- **Value**: Medium for scanned content

---

### 2.4 Better Dithering for B&W E-Ink

**Problem**: Current quantization uses simple palette mapping, which can lose detail.

**Solution**: Add Floyd-Steinberg dithering option for B&W e-ink.

**Implementation**:

```python
# src/image_pipeline/quantize.py (enhancement)
from PIL import Image
from .pipeline import ProcessingStep


class DitherStep(ProcessingStep):
    """
    Advanced dithering for B&W e-ink displays.
    
    Uses Floyd-Steinberg error diffusion for better detail preservation.
    """
    
    def __init__(self, method: str = 'floyd-steinberg', colors: int = 16):
        """
        Initialize dithering step.
        
        Args:
            method: Dithering method ('floyd-steinberg', 'ordered', 'none')
            colors: Number of gray levels (typically 16 for 4-bit e-ink)
        """
        super().__init__(method=method, colors=colors)
        self.method = method
        self.colors = colors
    
    def process(self, image: Image.Image) -> Image.Image:
        """Apply dithering for better grayscale reproduction."""
        # Convert to grayscale first
        gray = image.convert('L')
        
        if self.method == 'floyd-steinberg':
            # PIL's quantize with dithering
            return gray.quantize(colors=self.colors, dither=Image.Dither.FLOYDSTEINBERG)
        elif self.method == 'ordered':
            # Ordered dithering (Bayer matrix)
            return gray.quantize(colors=self.colors, dither=Image.Dither.ORDERED)
        else:
            # No dithering
            return gray.quantize(colors=self.colors, dither=Image.Dither.NONE)
    
    def get_name(self) -> str:
        return f"Dither({self.method},{self.colors})"
```

**Impact**:
- Better detail preservation on B&W e-ink
- More natural-looking gradients
- **Complexity**: Low (PIL built-in)
- **Value**: High for B&W devices

---

## 3. Medium Priority: Performance Optimizations

### 3.1 Lazy Pipeline Evaluation

**Problem**: All steps execute even if not needed (e.g., quantization on color tablets).

**Solution**: Add conditional step execution.

**Implementation**:

```python
# src/image_pipeline/pipeline.py (enhancement)
from abc import ABC, abstractmethod
from typing import Any, Callable
from PIL import Image


class ConditionalStep(ProcessingStep):
    """
    Wrapper for conditional step execution.
    """
    
    def __init__(self, step: ProcessingStep, condition: Callable[[Image.Image], bool]):
        """
        Initialize conditional step.
        
        Args:
            step: The processing step to conditionally execute
            condition: Function that returns True if step should execute
        """
        super().__init__(step=step, condition=condition)
        self.step = step
        self.condition = condition
    
    def process(self, image: Image.Image) -> Image.Image:
        """Execute step only if condition is met."""
        if self.condition(image):
            return self.step.process(image)
        return image
    
    def get_name(self) -> str:
        return f"Conditional({self.step.get_name()})"


# Usage example:
def is_color_image(image: Image.Image) -> bool:
    """Check if image has color content."""
    if image.mode not in ('RGB', 'RGBA'):
        return False
    
    # Sample pixels to check for color variation
    extrema = image.getextrema()
    if image.mode == 'RGB':
        return extrema[0] != extrema[1] or extrema[1] != extrema[2]
    return False


# Add to pipeline:
pipeline.add_step(
    ConditionalStep(
        QuantizeStep(),
        condition=lambda img: not is_color_image(img)  # Only quantize B&W images
    )
)
```

**Impact**:
- Faster processing for images that don't need all steps
- More flexible pipeline configuration
- **Complexity**: Low
- **Value**: Medium

---

### 3.2 Image Caching for Retries

**Problem**: Failed processing retries re-process from scratch.

**Solution**: Cache intermediate results for retry logic.

**Implementation**:

```python
# src/image_pipeline/pipeline.py (enhancement)
from typing import Dict
from PIL import Image
import hashlib


class CachedPipeline(ImagePipeline):
    """
    Pipeline with intermediate result caching for retry logic.
    """
    
    def __init__(self, steps: list[ProcessingStep] | None = None, cache_enabled: bool = True):
        super().__init__(steps)
        self.cache_enabled = cache_enabled
        self._cache: Dict[str, Image.Image] = {}
    
    def process(self, image: Image.Image) -> Image.Image:
        """Process with caching at each step."""
        result = image
        
        for i, step in enumerate(self.steps):
            if self.cache_enabled:
                # Create cache key from image hash + step name
                cache_key = f"{self._hash_image(result)}_{step.get_name()}"
                
                if cache_key in self._cache:
                    result = self._cache[cache_key]
                else:
                    result = step.process(result)
                    self._cache[cache_key] = result.copy()
            else:
                result = step.process(result)
        
        return result
    
    def clear_cache(self):
        """Clear the cache to free memory."""
        self._cache.clear()
    
    def _hash_image(self, image: Image.Image) -> str:
        """Generate hash of image for cache key."""
        return hashlib.md5(image.tobytes()).hexdigest()[:8]
```

**Impact**:
- Faster retries on transient errors
- Memory trade-off (uses more RAM)
- **Complexity**: Medium
- **Value**: Low-Medium (retries are rare)

---

### 3.3 GPU Acceleration (Optional)

**Problem**: Large images are slow to process on CPU.

**Solution**: Add GPU acceleration option for supported operations.

**Implementation** (Conceptual):

```python
# src/image_pipeline/gpu_accelerated.py
from PIL import Image
from .pipeline import ProcessingStep


class GPUAcceleratedStep(ProcessingStep):
    """
    Base class for GPU-accelerated processing steps.
    
    Falls back to CPU if GPU unavailable.
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._gpu_available = self._check_gpu()
    
    def _check_gpu(self) -> bool:
        """Check if GPU acceleration is available."""
        try:
            import torch
            return torch.cuda.is_available()
        except ImportError:
            return False
    
    def process(self, image: Image.Image) -> Image.Image:
        """Process with GPU if available, otherwise CPU."""
        if self._gpu_available:
            return self._process_gpu(image)
        else:
            return self._process_cpu(image)
    
    def _process_gpu(self, image: Image.Image) -> Image.Image:
        """GPU implementation - override in subclass."""
        raise NotImplementedError
    
    def _process_cpu(self, image: Image.Image) -> Image.Image:
        """CPU fallback - override in subclass."""
        raise NotImplementedError
```

**Impact**:
- Significantly faster for large batches
- Requires CUDA/GPU setup
- **Complexity**: Very High
- **Value**: Low (most users won't have GPU)

---

## 4. Low Priority: Advanced Features

### 4.1 Color Palette Optimization for Color E-Ink

**Problem**: Color E Ink (Kaleido 3) has limited color gamut and specific color preferences.

**Solution**: Optimize color palette for E Ink Kaleido displays.

**Implementation**:

```python
# src/image_pipeline/color_optimize.py
from PIL import Image
import numpy as np
from .pipeline import ProcessingStep


class ColorEInkOptimizeStep(ProcessingStep):
    """
    Optimize colors for E Ink Kaleido 3 displays.
    
    Kaleido 3 characteristics:
    - 4096 colors (12-bit)
    - Muted saturation
    - Better with cooler tones
    """
    
    def __init__(self, saturation_reduce: float = 0.8, cool_bias: float = 1.1):
        """
        Initialize color E Ink optimization.
        
        Args:
            saturation_reduce: Factor to reduce saturation (0-1)
            cool_bias: Bias toward cooler tones (>1 = cooler)
        """
        super().__init__(saturation_reduce=saturation_reduce, cool_bias=cool_bias)
        self.saturation_reduce = saturation_reduce
        self.cool_bias = cool_bias
    
    def process(self, image: Image.Image) -> Image.Image:
        """Optimize colors for E Ink Kaleido display."""
        # Convert to HSV for saturation adjustment
        hsv = image.convert('HSV')
        h, s, v = hsv.split()
        
        # Reduce saturation for better E Ink reproduction
        s_array = np.array(s)
        s_array = (s_array * self.saturation_reduce).astype(np.uint8)
        s = Image.fromarray(s_array, mode='L')
        
        # Recombine and convert back to RGB
        optimized = Image.merge('HSV', (h, s, v)).convert('RGB')
        
        # Apply cool bias (shift blue channel slightly)
        r, g, b = optimized.split()
        b_array = np.array(b)
        b_array = np.clip(b_array * self.cool_bias, 0, 255).astype(np.uint8)
        b = Image.fromarray(b_array, mode='L')
        
        return Image.merge('RGB', (r, g, b))
    
    def get_name(self) -> str:
        return "ColorEInkOptimize"
```

**Impact**:
- Better color reproduction on color E Ink
- More natural-looking manga colors
- **Complexity**: Medium
- **Value**: Medium (for color E Ink users)

---

### 4.2 AI-Based Super Resolution

**Problem**: Low-resolution scans lose detail when resized up.

**Solution**: Use AI super-resolution for upscaling.

**Implementation** (Conceptual):

```python
# src/image_pipeline/super_resolution.py
from PIL import Image
from .pipeline import ProcessingStep


class SuperResolutionStep(ProcessingStep):
    """
    AI-based super-resolution for upscaling low-res manga.
    
    Requires models: ESRGAN, Real-ESRGAN, or waifu2x
    """
    
    def __init__(self, scale: int = 2, model: str = 'anime'):
        """
        Initialize super-resolution step.
        
        Args:
            scale: Upscaling factor (2x, 4x)
            model: Model type ('anime', 'photo', 'general')
        """
        super().__init__(scale=scale, model=model)
        self.scale = scale
        self.model = model
        self._model_loaded = self._load_model()
    
    def _load_model(self) -> bool:
        """Load super-resolution model."""
        # TODO: Implement model loading
        # Consider: RealESRGAN, waifu2x-ncnn-vulkan
        return False
    
    def process(self, image: Image.Image) -> Image.Image:
        """Apply super-resolution upscaling."""
        if not self._model_loaded:
            # Fallback to simple Lanczos upscaling
            new_size = (image.width * self.scale, image.height * self.scale)
            return image.resize(new_size, Image.Resampling.LANCZOS)
        
        # TODO: Apply AI model
        return image
    
    def get_name(self) -> str:
        return f"SuperRes({self.scale}x)"
```

**Impact**:
- Better quality from low-res sources
- Significantly slower processing
- **Complexity**: Very High (requires ML models)
- **Value**: Low (niche use case)

---

### 4.3 Page Type Detection

**Problem**: Different manga page types (cover, splash, regular) need different processing.

**Solution**: Auto-detect page type and apply appropriate processing.

**Implementation** (Conceptual):

```python
# src/image_pipeline/page_classifier.py
from PIL import Image
from enum import Enum
from .pipeline import ProcessingStep


class PageType(Enum):
    COVER = "cover"          # Full color cover page
    SPLASH = "splash"        # Full-page artwork
    REGULAR = "regular"      # Standard manga page
    TWO_PAGE = "two_page"    # Two-page spread


class PageClassifierStep(ProcessingStep):
    """
    Classify manga page type for adaptive processing.
    """
    
    def __init__(self):
        super().__init__()
        self.detected_type: PageType | None = None
    
    def process(self, image: Image.Image) -> Image.Image:
        """Classify page type (non-modifying step)."""
        self.detected_type = self._classify(image)
        
        # Store classification in image info for downstream steps
        image.info['page_type'] = self.detected_type.value
        
        return image
    
    def _classify(self, image: Image.Image) -> PageType:
        """Classify page type based on image characteristics."""
        width, height = image.size
        
        # Two-page spread: wider than tall
        if width > height * 1.3:
            return PageType.TWO_PAGE
        
        # Check for color (cover pages typically colorful)
        extrema = image.getextrema()
        if image.mode == 'RGB':
            color_range = sum(e[1] - e[0] for e in extrema) / 3
            if color_range > 200:  # Highly colorful
                return PageType.COVER
        
        # Check for high detail (splash pages)
        # Simple heuristic: count unique colors
        unique_colors = len(image.getcolors(maxcolors=10000) or [])
        if unique_colors > 5000:
            return PageType.SPLASH
        
        return PageType.REGULAR
    
    def get_name(self) -> str:
        return "PageClassifier"
```

**Impact**:
- Adaptive processing per page type
- Better quality for varied content
- **Complexity**: High
- **Value**: Medium (nice-to-have)

---

## 5. Low Priority: User Experience Enhancements

### 5.1 Quality Metrics and Reporting

**Problem**: No feedback on processing quality or issues.

**Solution**: Add quality metrics collection and reporting.

**Implementation**:

```python
# src/image_pipeline/quality_metrics.py
from PIL import Image
from dataclasses import dataclass
from .pipeline import ProcessingStep


@dataclass
class ImageQualityMetrics:
    """Quality metrics for processed image."""
    sharpness_score: float
    contrast_score: float
    brightness_avg: float
    color_count: int
    file_size_reduction: float  # Percentage
    processing_time_ms: float


class QualityMetricsStep(ProcessingStep):
    """
    Collect quality metrics from processed images.
    
    Non-modifying step that analyzes and reports metrics.
    """
    
    def __init__(self):
        super().__init__()
        self.metrics: ImageQualityMetrics | None = None
    
    def process(self, image: Image.Image) -> Image.Image:
        """Analyze image quality (non-modifying)."""
        import time
        start = time.time()
        
        # Calculate metrics
        self.metrics = ImageQualityMetrics(
            sharpness_score=self._calculate_sharpness(image),
            contrast_score=self._calculate_contrast(image),
            brightness_avg=self._calculate_brightness(image),
            color_count=len(image.getcolors(maxcolors=10000) or []),
            file_size_reduction=0.0,  # Set later by save step
            processing_time_ms=(time.time() - start) * 1000
        )
        
        return image
    
    def _calculate_sharpness(self, image: Image.Image) -> float:
        """Calculate sharpness score using Laplacian variance."""
        # Simple edge-based sharpness metric
        gray = image.convert('L')
        from PIL import ImageFilter
        edges = gray.filter(ImageFilter.FIND_EDGES)
        
        # Variance of edge image = sharpness
        import numpy as np
        edge_array = np.array(edges)
        return float(np.var(edge_array))
    
    def _calculate_contrast(self, image: Image.Image) -> float:
        """Calculate contrast score."""
        extrema = image.getextrema()
        if image.mode == 'RGB':
            # Average range across channels
            avg_range = sum(e[1] - e[0] for e in extrema) / 3
            return avg_range / 255.0
        else:
            return (extrema[1] - extrema[0]) / 255.0
    
    def _calculate_brightness(self, image: Image.Image) -> float:
        """Calculate average brightness."""
        gray = image.convert('L')
        import numpy as np
        return float(np.mean(np.array(gray))) / 255.0
    
    def get_name(self) -> str:
        return "QualityMetrics"
```

**Impact**:
- Better visibility into processing quality
- Helps tune parameters
- **Complexity**: Medium
- **Value**: Medium (for power users)

---

### 5.2 Pipeline Dry-Run Mode

**Problem**: Hard to preview pipeline results without processing.

**Solution**: Add dry-run mode with quality estimates.

**Implementation**:

```python
# src/image_pipeline/pipeline.py (enhancement)
from typing import List
from PIL import Image


class ImagePipeline:
    # ... existing code ...
    
    def dry_run(self, image: Image.Image) -> dict:
        """
        Simulate pipeline without modifying image.
        
        Returns:
            Dictionary with estimated processing info:
            - steps: List of step names
            - estimated_time_ms: Estimated processing time
            - warnings: List of potential issues
        """
        warnings = []
        estimated_time = 0
        
        for step in self.steps:
            # Estimate processing time (rough heuristic)
            step_name = step.get_name()
            
            if 'Quantize' in step_name:
                estimated_time += 50  # ms
            elif 'Sharpen' in step_name:
                estimated_time += 30
            elif 'Contrast' in step_name:
                estimated_time += 20
            else:
                estimated_time += 10
            
            # Check for potential issues
            if step_name.startswith('Quantize'):
                colors = image.getcolors(maxcolors=10000)
                if colors and len(colors) < 50:
                    warnings.append(f"Image already has few colors ({len(colors)}), quantization may not be necessary")
        
        return {
            'steps': self.get_steps(),
            'estimated_time_ms': estimated_time,
            'warnings': warnings,
            'pipeline': str(self)
        }
```

**Impact**:
- Better pipeline configuration
- Prevents unnecessary processing
- **Complexity**: Low
- **Value**: Low-Medium

---

### 5.3 Before/After Comparison Tool

**Problem**: Hard to evaluate processing quality without side-by-side comparison.

**Solution**: Generate comparison images.

**Implementation**:

```python
# src/image_pipeline/comparison.py
from PIL import Image, ImageDraw, ImageFont


def create_comparison(
    original: Image.Image,
    processed: Image.Image,
    labels: tuple[str, str] = ("Original", "Processed")
) -> Image.Image:
    """
    Create side-by-side comparison of original and processed images.
    
    Args:
        original: Original image
        processed: Processed image
        labels: Tuple of (original_label, processed_label)
    
    Returns:
        Combined comparison image
    """
    # Resize to same dimensions if needed
    if original.size != processed.size:
        processed = processed.resize(original.size, Image.Resampling.LANCZOS)
    
    width, height = original.size
    
    # Create new image with both side-by-side
    comparison = Image.new('RGB', (width * 2 + 20, height + 40), 'white')
    
    # Paste images
    comparison.paste(original, (10, 30))
    comparison.paste(processed, (width + 10, 30))
    
    # Add labels
    draw = ImageDraw.Draw(comparison)
    try:
        font = ImageFont.truetype("Arial.ttf", 20)
    except:
        font = ImageFont.load_default()
    
    draw.text((10, 5), labels[0], fill='black', font=font)
    draw.text((width + 10, 5), labels[1], fill='black', font=font)
    
    # Add dividing line
    draw.line([(width + 10, 0), (width + 10, height + 40)], fill='gray', width=2)
    
    return comparison
```

**Impact**:
- Easier quality evaluation
- Better parameter tuning
- **Complexity**: Low
- **Value**: Medium (for testing/development)

---

## Implementation Roadmap

### Phase 1: Quick Wins (v1.1.0) - 1-2 weeks

**High-value, low-complexity features:**

1. **Smart Crop** (1.2) - Remove white margins
2. **Unsharp Mask** (2.1) - Better sharpening
3. **Dithering** (2.4) - Better B&W quality
4. **Denoise** (2.3) - Clean up scanned images
5. **Conditional Steps** (3.1) - Skip unnecessary processing

**Estimated effort**: 20-30 hours  
**Impact**: High (immediate quality improvements)

---

### Phase 2: Manga Optimization (v1.2.0) - 2-4 weeks

**Manga-specific features:**

1. **Auto-Rotation** (1.1) - Correct tilted scans
2. **Text Enhancement** (1.3) - Better readability
3. **Adaptive Contrast** (2.2) - CLAHE for varied lighting
4. **Color E Ink Optimization** (4.1) - Better Kaleido 3 support
5. **Quality Metrics** (5.1) - Processing feedback

**Estimated effort**: 40-60 hours  
**Impact**: Very High (manga-specific quality boost)

---

### Phase 3: Advanced Features (v2.0.0) - 4-8 weeks

**Complex, high-impact features:**

1. **Panel Border Detection** (1.4) - Enhanced readability
2. **Page Classification** (4.3) - Adaptive processing
3. **GPU Acceleration** (3.3) - Performance boost
4. **Comparison Tool** (5.3) - Quality evaluation
5. **Pipeline Caching** (3.2) - Faster retries

**Estimated effort**: 80-120 hours  
**Impact**: Medium-High (power user features)

---

### Phase 4: AI Integration (v3.0.0) - Future

**Experimental, cutting-edge features:**

1. **Super Resolution** (4.2) - AI upscaling
2. **Advanced Panel Detection** - ML-based layout analysis
3. **Content-Aware Processing** - ML-driven parameter tuning

**Estimated effort**: 120+ hours  
**Impact**: High (but limited audience)

---

## Testing Strategy

### For Each New Feature:

1. **Unit Tests**
   - Test step initialization
   - Test processing logic
   - Test edge cases (empty images, single-color, etc.)

2. **Integration Tests**
   - Test in complete pipeline
   - Test with different device presets
   - Test with real manga samples

3. **Visual Tests**
   - Generate before/after comparisons
   - Validate on actual e-reader devices
   - User acceptance testing

4. **Performance Tests**
   - Benchmark processing time
   - Memory usage profiling
   - Batch processing stress tests

---

## Configuration Examples

### High-Quality Scanned Manga Preset

```python
# src/image_pipeline/presets.py (new preset)
@staticmethod
def scanned_manga() -> ImagePipeline:
    """
    Optimized for scanned manga with rotation/noise issues.
    """
    pipeline = ImagePipeline()
    pipeline.add_step(AutoRotateStep(max_angle=5.0))      # Fix rotation
    pipeline.add_step(SmartCropStep(threshold=240))       # Remove margins
    pipeline.add_step(DenoiseStep(strength='medium'))     # Clean noise
    pipeline.add_step(AdaptiveContrastStep())             # CLAHE
    pipeline.add_step(TextEnhanceStep())                  # Enhance text
    pipeline.add_step(UnsharpMaskStep(radius=2.0))        # Sharpen
    pipeline.add_step(QuantizeStep(palette=Palette16))    # Reduce colors
    return pipeline
```

### Color E Ink Optimized Preset

```python
@staticmethod
def color_eink() -> ImagePipeline:
    """
    Optimized for color E Ink devices (Kaleido 3).
    """
    pipeline = ImagePipeline()
    pipeline.add_step(SmartCropStep(threshold=240))
    pipeline.add_step(ColorEInkOptimizeStep(saturation_reduce=0.8))
    pipeline.add_step(ContrastStep(factor=1.3))
    pipeline.add_step(UnsharpMaskStep(radius=1.5, percent=120))
    pipeline.add_step(QuantizeStep(colors=4096))  # 12-bit color
    return pipeline
```

### High-Resolution Tablet Preset

```python
@staticmethod
def tablet_hires() -> ImagePipeline:
    """
    Optimized for high-resolution tablets (iPad Pro, etc.).
    """
    pipeline = ImagePipeline()
    pipeline.add_step(SmartCropStep(threshold=245))
    pipeline.add_step(ContrastStep(factor=1.1))
    pipeline.add_step(UnsharpMaskStep(radius=2.5, percent=140))
    # No quantization - preserve full color
    return pipeline
```

---

## Dependencies to Add

### Phase 1-2:
```txt
# requirements.txt additions
pillow >= 11.3.0         # Already present
numpy >= 1.24.0          # For advanced image processing
```

### Phase 2-3:
```txt
opencv-python >= 4.8.0   # For CLAHE, advanced CV features (optional)
scikit-image >= 0.21.0   # For quality metrics (optional)
```

### Phase 4:
```txt
torch >= 2.0.0           # For GPU acceleration (optional)
torchvision >= 0.15.0    # For AI models (optional)
```

**Note**: Keep optional dependencies truly optional with fallback implementations.

---

## Summary

This document provides a comprehensive roadmap for enhancing ShiroInk's image processing pipeline. The suggestions are prioritized by:

1. **Value to users** (manga quality improvements)
2. **Implementation complexity** (quick wins first)
3. **Maintenance burden** (avoid over-engineering)

**Recommended Next Steps:**

1. Review and prioritize features with stakeholders
2. Implement Phase 1 (Quick Wins) for v1.1.0
3. Gather user feedback on quality improvements
4. Proceed with Phase 2 (Manga Optimization) based on feedback
5. Evaluate advanced features (Phase 3+) based on user demand

**Key Principles:**

- Keep dependencies minimal (PIL-first approach)
- Provide graceful fallbacks for optional features
- Maintain backward compatibility
- Focus on manga-specific quality improvements
- Test on real e-reader devices

---

**Document Version**: 1.0  
**Last Updated**: 2026-01-04  
**Status**: Ready for Review
