import fire
from PySide6.QtWidgets import QApplication

from timelapse.config import TimelapseConfig
from timelapse.opencv import OpenCVCameraProvider
from timelapse.ui.main_window import MainWindow


class TimelapseApplicationLauncher:
    """Timelapse launcher."""

    def __init__(self, config: TimelapseConfig):
        self.config: TimelapseConfig = config

    def ui(self, sound: bool = True):
        """Launch ui application."""
        app = QApplication()
        window = MainWindow(self.config, sound)
        window.show()
        app.exec()

    def __call__(self, sound: bool = True):
        """Launch default (ui) application."""
        self.ui(sound)


def launch():
    """Launch application."""
    config = TimelapseConfig.default(OpenCVCameraProvider())
    launcher = TimelapseApplicationLauncher(config)
    fire.Fire(launcher)


if __name__ == '__main__':
    launch()
