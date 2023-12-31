from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from timelapse.dummy import DummyProvider
from timelapse.model import CameraDescriptor, CameraProvider


@dataclass
class TimelapseConfig:
    """Timelapse config contains all required config options."""

    camera_provider: CameraProvider
    camera: CameraDescriptor
    frame_interval: int
    destination_directory: Path
    group_size: int = 1000
    skip: int = 5  # May be useful to compensate frame buffering

    @staticmethod
    def default(provider: CameraProvider) -> TimelapseConfig:
        """Create default config."""
        cameras = provider.list_webcams()
        if len(cameras) == 0:
            provider = DummyProvider()
            cameras = provider.list_webcams()
        return TimelapseConfig(provider, cameras[0], 1000, Path.home())
