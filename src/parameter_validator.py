"""
Parameter validation and suggestion system for ShiroInk.

This module provides utilities for validating user inputs and
offering helpful suggestions when invalid parameters are provided.
"""

import os
from pathlib import Path
from typing import Any, Optional


class ParameterValidator:
    """
    Validates and provides suggestions for ShiroInk parameters.

    This class checks user inputs against known constraints and offers
    helpful suggestions when validation fails.
    """

    @staticmethod
    def _get_all_devices() -> list[str]:
        """Get all available device keys from DeviceSpecs."""
        try:
            from image_pipeline.devices import DeviceSpecs

            return DeviceSpecs.list_devices()
        except ImportError:
            return []

    @classmethod
    def validate_resolution(
        cls, resolution: tuple[int, int]
    ) -> tuple[bool, Optional[str]]:
        """
        Validate image resolution.

        Args:
            resolution: Tuple of (width, height) in pixels.

        Returns:
            Tuple of (is_valid, error_message).
        """
        if not isinstance(resolution, tuple) or len(resolution) != 2:
            return False, "Resolution must be a tuple of (width, height)"

        width, height = resolution

        if not isinstance(width, int) or not isinstance(height, int):
            return False, "Resolution values must be integers"

        if width < 200 or height < 200:
            return False, "Resolution must be at least 200x200 pixels"

        if width > 10000 or height > 10000:
            return False, "Resolution exceeds maximum of 10000x10000 pixels"

        return True, None

    @classmethod
    def validate_quality(cls, quality: int) -> tuple[bool, Optional[str]]:
        """
        Validate quality level.

        Args:
            quality: Quality level (1-9).

        Returns:
            Tuple of (is_valid, error_message).
        """
        if not isinstance(quality, int):
            return False, "Quality must be an integer"

        if quality < 1 or quality > 9:
            return False, "Quality must be between 1 and 9"

        return True, None

    @classmethod
    def validate_workers(cls, workers: int) -> tuple[bool, Optional[str]]:
        """
        Validate number of worker threads.

        Args:
            workers: Number of worker threads.

        Returns:
            Tuple of (is_valid, error_message).
        """
        if not isinstance(workers, int):
            return False, "Workers must be an integer"

        if workers < 1:
            return False, "Workers must be at least 1"

        if workers > 256:
            return False, "Workers cannot exceed 256"

        return True, None

    @classmethod
    def validate_path(cls, path: Path) -> tuple[bool, Optional[str]]:
        """
        Validate file system path.

        Args:
            path: Path to validate.

        Returns:
            Tuple of (is_valid, error_message).
        """
        if not isinstance(path, (Path, str)):
            return False, "Path must be a string or Path object"

        path_obj = Path(path) if isinstance(path, str) else path

        if not path_obj.exists():
            return False, f"Path does not exist: {path_obj}"

        if not path_obj.is_dir():
            return False, f"Path is not a directory: {path_obj}"

        if not os.access(str(path_obj), os.R_OK):
            return False, f"No read permission for: {path_obj}"

        return True, None

    @classmethod
    def validate_device(cls, device_key: str) -> tuple[bool, Optional[str]]:
        """
        Validate device key.

        Args:
            device_key: Device key to validate.

        Returns:
            Tuple of (is_valid, error_message).
        """
        if not isinstance(device_key, str):
            return False, "Device key must be a string"

        all_devices = cls._get_all_devices()

        if device_key in all_devices:
            return True, None

        similar = cls._find_similar_device(device_key, all_devices)
        if similar:
            return False, f"Unknown device. Did you mean '{similar}'?"

        return (
            False,
            f"Unknown device '{device_key}'. "
            f"Use --list-devices to see available devices.",
        )

    @classmethod
    def _find_similar_device(
        cls, device_key: str, all_devices: list[str]
    ) -> Optional[str]:
        """
        Find device similar to the provided key.

        Uses simple string matching to find close matches.

        Args:
            device_key: Device key to find match for.
            all_devices: List of all valid device keys.

        Returns:
            Similar device key or None.
        """
        device_lower = device_key.lower()

        for device in all_devices:
            if device_lower in device or device in device_lower:
                return device

        device_prefix = device_lower.split("_")[0]
        for device in all_devices:
            if device.startswith(device_prefix):
                return device

        return None

    @classmethod
    def suggest_quality_level(cls, use_case: str) -> tuple[int, str]:
        """
        Suggest quality level based on use case.

        Args:
            use_case: Use case description (e.g., 'fast', 'balanced', 'best').

        Returns:
            Tuple of (quality_level, description).
        """
        suggestions = {
            "fast": (3, "Fast processing, lower quality"),
            "balanced": (6, "Balanced speed and quality (default)"),
            "best": (9, "Best quality, slower processing"),
        }

        return suggestions.get(
            use_case.lower(),
            (6, "Balanced speed and quality (default)"),
        )

    @classmethod
    def suggest_workers(cls) -> int:
        """
        Suggest number of workers based on CPU cores.

        Returns:
            Recommended number of worker threads.
        """
        import multiprocessing

        cores = multiprocessing.cpu_count()
        suggested = max(1, cores - 1)

        return suggested

    @classmethod
    def validate_configuration(cls, config: dict[str, Any]) -> tuple[bool, list[str]]:
        """
        Validate complete configuration dictionary.

        Args:
            config: Configuration dictionary to validate.

        Returns:
            Tuple of (is_valid, list of error messages).
        """
        errors = []

        required_fields = ["src_dir", "dest_dir"]
        for field in required_fields:
            if field not in config:
                errors.append(f"Missing required field: {field}")
            elif not config[field]:
                errors.append(f"Empty value for required field: {field}")

        if "resolution" in config and config["resolution"]:
            is_valid, error = cls.validate_resolution(config["resolution"])
            if not is_valid:
                errors.append(f"Invalid resolution: {error}")

        if "quality" in config and config["quality"]:
            is_valid, error = cls.validate_quality(config["quality"])
            if not is_valid:
                errors.append(f"Invalid quality: {error}")

        if "workers" in config and config["workers"]:
            is_valid, error = cls.validate_workers(config["workers"])
            if not is_valid:
                errors.append(f"Invalid workers: {error}")

        if "device" in config and config["device"]:
            is_valid, error = cls.validate_device(config["device"])
            if not is_valid:
                errors.append(f"Invalid device: {error}")

        return len(errors) == 0, errors
