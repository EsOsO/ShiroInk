"""
JSON schema validation for ShiroInk profiles.
"""

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class ProfileSchema:
    """Schema definition for a ShiroInk profile."""

    name: str
    device: Optional[str] = None
    pipeline: Optional[str] = None
    resolution: Optional[tuple[int, int]] = None
    rtl: bool = False
    quality: int = 6
    workers: int = 4
    description: str = ""
    created: str = ""
    last_used: str = ""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ProfileSchema":
        """
        Create ProfileSchema from dictionary.

        Args:
            data: Dictionary with profile data

        Returns:
            ProfileSchema instance

        Raises:
            ValueError: If required fields are missing or invalid
        """
        if "name" not in data:
            raise ValueError("Profile must have 'name' field")

        # Extract and validate fields
        name = data["name"]
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Profile name must be non-empty string")

        device = data.get("device")
        if device is not None and not isinstance(device, str):
            raise ValueError("Device must be string or null")

        pipeline = data.get("pipeline")
        if pipeline is not None and not isinstance(pipeline, str):
            raise ValueError("Pipeline must be string or null")

        # Handle resolution - can be list/tuple
        resolution = data.get("resolution")
        if resolution is not None:
            if isinstance(resolution, (list, tuple)):
                if len(resolution) != 2:
                    raise ValueError("Resolution must be [width, height]")
                resolution = tuple(resolution)
            else:
                raise ValueError("Resolution must be array [width, height]")

        rtl = data.get("rtl", False)
        if not isinstance(rtl, bool):
            raise ValueError("RTL must be boolean")

        quality = data.get("quality", 6)
        if not isinstance(quality, int) or quality < 1 or quality > 9:
            raise ValueError("Quality must be integer 1-9")

        workers = data.get("workers", 4)
        if not isinstance(workers, int) or workers < 1:
            raise ValueError("Workers must be positive integer")

        description = data.get("description", "")
        if not isinstance(description, str):
            raise ValueError("Description must be string")

        created = data.get("created", "")
        last_used = data.get("last_used", "")

        return cls(
            name=name,
            device=device,
            pipeline=pipeline,
            resolution=resolution,
            rtl=rtl,
            quality=quality,
            workers=workers,
            description=description,
            created=created,
            last_used=last_used,
        )

    def to_dict(self) -> dict[str, Any]:
        """
        Convert ProfileSchema to dictionary for JSON serialization.

        Returns:
            Dictionary representation of profile
        """
        return {
            "name": self.name,
            "device": self.device,
            "pipeline": self.pipeline,
            "resolution": list(self.resolution) if self.resolution else None,
            "rtl": self.rtl,
            "quality": self.quality,
            "workers": self.workers,
            "description": self.description,
            "created": self.created,
            "last_used": self.last_used,
        }
