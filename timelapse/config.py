from dataclasses import dataclass
from pathlib import Path

from timelapse.model import CameraDescriptor


@dataclass
class TimelapseConfig:
    """Timelapse config contains all required config options."""

    camera: CameraDescriptor
    frame_interval: int
    destination: Path
