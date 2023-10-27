from pathlib import Path

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QPushButton, QVBoxLayout, QWidget

from timelapse.config import TimelapseConfig
from timelapse.model import CameraDescriptor
from timelapse.ui.cam_picker import CamPicker
from timelapse.ui.interval_picker import TimeIntervalPicker
from timelapse.ui.path_selector import PathSelector


class Configurer(QWidget):
    """A widget that allows to set up all configuration options."""

    config_changed: Signal = Signal(TimelapseConfig)
    config_done: Signal = Signal()
    config: TimelapseConfig

    def __init__(self, config: TimelapseConfig):
        super().__init__()
        self.config = config
        self._init_ui()

    def _init_ui(self):
        """Set up content."""
        self._layout = QVBoxLayout()

        self._cam_picker = CamPicker(self.config.camera, self.config.camera_provider)
        self._cam_picker.camera_changed.connect(self._camera_changed)
        self._layout.addWidget(self._cam_picker)

        self._interval_picker = TimeIntervalPicker()
        self._interval_picker.interval_changed.connect(self._interval_changed)
        self._layout.addWidget(self._interval_picker)

        self._path_selector = PathSelector()
        self._path_selector.path_changed.connect(self._path_changed)
        self._layout.addWidget(self._path_selector)

        self._button = QPushButton("Let's go!")
        self._button.clicked.connect(self.config_done)
        self._layout.addWidget(self._button)

        self.setLayout(self._layout)

    def _camera_changed(self, camera: CameraDescriptor):
        """Handle camera changed."""
        self.config.camera = camera
        self.config_changed.emit(self.config)

    def _interval_changed(self, interval_millis: int):
        """Handle frame interval changed."""
        self.config.frame_interval = interval_millis
        self.config_changed.emit(self.config)

    def _path_changed(self, new_path: Path):
        """Handle path changed."""
        self.config.destination_directory = new_path
        self.config_changed.emit(self.config)
