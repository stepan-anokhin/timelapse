import fire

from timelapse.config import TimelapseConfig
from timelapse.opencv import OpenCVCameraProvider


class TimelapseApplicationLauncher:
    """Timelapse launcher."""

    def __init__(self, config: TimelapseConfig):
        self.config: TimelapseConfig = config

    def ui(self, sound: bool = False):
        """Launch ui application."""

    def __call__(self, sound: bool = False):
        """Launch default (ui) application."""


def launch():
    """Launch application."""
    config = TimelapseConfig.default(OpenCVCameraProvider())
    launcher = TimelapseApplicationLauncher(config)
    fire.Fire(launcher)
