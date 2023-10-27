from datetime import datetime
from pathlib import Path

from PySide6.QtCore import Signal, QTimer
from PySide6.QtGui import QShowEvent, QPixmap
from PySide6.QtWidgets import QVBoxLayout, QWidget, QLayout, QLabel

from timelapse.config import TimelapseConfig
from timelapse.model import Camera
from timelapse.recorder import TimelapseRecorder
from timelapse.ui.resources import Resources


class Capturer(QWidget):
    """A widget that displays capture details."""

    frame_captured: Signal = Signal(Path)
    capture_done: Signal = Signal()
    _camera: Camera
    _timer: QTimer

    def __init__(self, config: TimelapseConfig, no_image: QPixmap = None):
        super().__init__()
        self._config = config
        self._captured: int = 0
        self._started: datetime = datetime.now()
        self.no_image: QPixmap = no_image or QPixmap(Resources.NO_IMAGE)
        self.recorder: TimelapseRecorder = TimelapseRecorder(config)
        self._init_ui()

    def _init_ui(self):
        """Set up content."""
        self._layout: QLayout = QVBoxLayout()

        self._frame_container = QLabel()
        self._layout.addWidget(self._frame_container)

        self._start_time_label = QLabel(f"Started: {self._started}")
        self._layout.addWidget(self._start_time_label)

        self._capture_count_label = QLabel(f"Captured frames: {self._captured}")
        self._layout.addWidget(self._capture_count_label)
        self.setLayout(self._layout)

    def _capture_frame(self):
        """Capture frame from the camera."""
        frame = self.recorder.capture_frame()
        if frame is not None:
            self._frame_container.setPixmap(frame.to_pixmap())
        else:
            self._frame_container.setPixmap(self.no_image)
        self._captured += 1
        self._capture_count_label.setText(f"Captured frames: {self._captured}")

    def showEvent(self, event: QShowEvent):
        """Start capturing on show."""
        super().showEvent(event)
        QTimer().singleShot(100, self.start_capture)

    def start_capture(self):
        """Start capturing."""
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._capture_frame)
        self._timer.start(self._config.frame_interval)

    def stop_capture(self):
        """Stop capturing frames."""
        if self._timer is not None:
            self._timer.stop()
        self.recorder.close()
