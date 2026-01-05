"""
Profile manager for ShiroInk.

Handles saving, loading, listing, editing, and deleting profiles.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

from .schema import ProfileSchema


class ProfileManager:
    """Manages ShiroInk configuration profiles."""

    def __init__(self):
        """Initialize profile manager."""
        self.profiles_dir = self._get_profiles_dir()
        self.profiles_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _get_profiles_dir() -> Path:
        """
        Get profiles directory following OS standards (POSIX-compliant).

        Returns:
            Path to profiles directory
        """
        if os.name == "nt":  # Windows
            base = Path(os.getenv("APPDATA", Path.home() / "AppData" / "Roaming"))
        else:  # Linux/macOS
            xdg_config = os.getenv("XDG_CONFIG_HOME")
            if xdg_config:
                base = Path(xdg_config)
            else:
                base = Path.home() / ".config"

        return base / "shiroink" / "profiles"

    def _get_profile_path(self, name: str) -> Path:
        """
        Get full path for a profile file.

        Args:
            name: Profile name (without .json extension)

        Returns:
            Full path to profile file
        """
        # Sanitize profile name
        safe_name = "".join(c for c in name if c.isalnum() or c in "-_")
        if not safe_name:
            raise ValueError(f"Invalid profile name: {name}")

        return self.profiles_dir / f"{safe_name}.json"

    def save(
        self,
        name: str,
        device: Optional[str] = None,
        pipeline: Optional[str] = None,
        resolution: Optional[tuple[int, int]] = None,
        rtl: bool = False,
        quality: int = 6,
        workers: int = 4,
        description: str = "",
    ) -> None:
        """
        Save a configuration profile.

        Args:
            name: Profile name
            device: Device preset name
            pipeline: Pipeline preset name
            resolution: Target resolution (width, height)
            rtl: Right-to-left mode
            quality: Quality level (1-9)
            workers: Number of parallel workers
            description: Profile description

        Raises:
            ValueError: If profile name is invalid
            IOError: If save fails
        """
        profile_path = self._get_profile_path(name)

        # Create profile schema
        profile = ProfileSchema(
            name=name,
            device=device,
            pipeline=pipeline,
            resolution=resolution,
            rtl=rtl,
            quality=quality,
            workers=workers,
            description=description,
            created=datetime.now().isoformat(),
            last_used=datetime.now().isoformat(),
        )

        # Save to file
        try:
            with open(profile_path, "w", encoding="utf-8") as f:
                json.dump(profile.to_dict(), f, indent=2)
        except Exception as e:
            raise IOError(f"Failed to save profile: {e}")

    def load(self, name: str) -> ProfileSchema:
        """
        Load a configuration profile.

        Args:
            name: Profile name

        Returns:
            ProfileSchema instance

        Raises:
            FileNotFoundError: If profile doesn't exist
            ValueError: If profile is invalid
        """
        profile_path = self._get_profile_path(name)

        if not profile_path.exists():
            raise FileNotFoundError(f"Profile not found: {name}")

        try:
            with open(profile_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Update last_used timestamp
            profile = ProfileSchema.from_dict(data)
            profile.last_used = datetime.now().isoformat()
            self.save(
                profile.name,
                device=profile.device,
                pipeline=profile.pipeline,
                resolution=profile.resolution,
                rtl=profile.rtl,
                quality=profile.quality,
                workers=profile.workers,
                description=profile.description,
            )

            return profile
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid profile format: {e}")
        except Exception as e:
            raise ValueError(f"Failed to load profile: {e}")

    def list_profiles(self) -> list[dict]:
        """
        List all available profiles with metadata.

        Returns:
            List of dicts with profile metadata
        """
        profiles = []

        if not self.profiles_dir.exists():
            return profiles

        for profile_file in sorted(self.profiles_dir.glob("*.json")):
            try:
                with open(profile_file, "r", encoding="utf-8") as f:
                    data = json.load(f)

                profile = ProfileSchema.from_dict(data)
                profiles.append(
                    {
                        "name": profile.name,
                        "device": profile.device,
                        "pipeline": profile.pipeline,
                        "description": profile.description,
                        "created": profile.created,
                        "last_used": profile.last_used,
                    }
                )
            except Exception:
                # Skip invalid profiles silently
                pass

        return profiles

    def edit(
        self,
        name: str,
        device: Optional[str] = None,
        pipeline: Optional[str] = None,
        resolution: Optional[tuple[int, int]] = None,
        rtl: Optional[bool] = None,
        quality: Optional[int] = None,
        workers: Optional[int] = None,
        description: Optional[str] = None,
    ) -> None:
        """
        Edit an existing profile.

        Args:
            name: Profile name to edit
            device: New device (or None to keep current)
            pipeline: New pipeline (or None to keep current)
            resolution: New resolution (or None to keep current)
            rtl: New RTL setting (or None to keep current)
            quality: New quality (or None to keep current)
            workers: New workers (or None to keep current)
            description: New description (or None to keep current)

        Raises:
            FileNotFoundError: If profile doesn't exist
        """
        # Load current profile
        profile = self.load(name)

        # Update fields if provided
        if device is not None:
            profile.device = device
        if pipeline is not None:
            profile.pipeline = pipeline
        if resolution is not None:
            profile.resolution = resolution
        if rtl is not None:
            profile.rtl = rtl
        if quality is not None:
            profile.quality = quality
        if workers is not None:
            profile.workers = workers
        if description is not None:
            profile.description = description

        # Save updated profile
        self.save(
            profile.name,
            device=profile.device,
            pipeline=profile.pipeline,
            resolution=profile.resolution,
            rtl=profile.rtl,
            quality=profile.quality,
            workers=profile.workers,
            description=profile.description,
        )

    def delete(self, name: str) -> None:
        """
        Delete a profile.

        Args:
            name: Profile name to delete

        Raises:
            FileNotFoundError: If profile doesn't exist
        """
        profile_path = self._get_profile_path(name)

        if not profile_path.exists():
            raise FileNotFoundError(f"Profile not found: {name}")

        try:
            profile_path.unlink()
        except Exception as e:
            raise IOError(f"Failed to delete profile: {e}")

    def exists(self, name: str) -> bool:
        """
        Check if a profile exists.

        Args:
            name: Profile name to check

        Returns:
            True if profile exists, False otherwise
        """
        try:
            profile_path = self._get_profile_path(name)
            return profile_path.exists()
        except ValueError:
            return False
