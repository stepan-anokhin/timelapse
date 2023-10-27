import sys
from typing import List

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

from timelapse.config import TimelapseConfig
from timelapse.dummy import DummyCamera
from timelapse.model import Camera
from timelapse.opencv import OpenCVCameraProvider
from timelapse.ui.capturer import Capturer
from timelapse.ui.configurer import Configurer


class MainWindow(QMainWindow):
    camera: Camera = DummyCamera()

    def __init__(self, initial_config: TimelapseConfig):
        super().__init__()
        self.config = initial_config
        self.setWindowTitle("TimeLapse")

        self._layout = QVBoxLayout()

        self._capturer: Capturer | None = None
        self._configurer = Configurer(self.config)
        self._configurer.config_changed.connect(self.update_config)
        self._configurer.config_done.connect(self._start_capturing)
        self._layout.addWidget(self._configurer)

        content = QWidget(self)
        content.setLayout(self._layout)
        self.setCentralWidget(content)

    def update_config(self, new_config: TimelapseConfig):
        """Set new config."""
        self.config = new_config
        print(self.config)

    def _start_capturing(self):
        """Handle start frame capturing."""
        self._configurer.hide()
        self._capturer = Capturer(self.config)
        self._layout.addWidget(self._capturer)


def main(qt_args: List[str]):
    app = QApplication(qt_args)
    config = TimelapseConfig.default(OpenCVCameraProvider())
    window = MainWindow(config)
    window.show()

    app.exec()


if __name__ == '__main__':
    main(qt_args=sys.argv)
