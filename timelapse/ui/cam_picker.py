from typing import Sequence

from PySide6.QtCore import Signal, QTimer
from PySide6.QtGui import QPixmap, QShowEvent, QHideEvent
from PySide6.QtWidgets import QWidget, QLayout, QVBoxLayout, QComboBox, QLabel

from timelapse.dummy import DummyCamera
from timelapse.model import Camera, CameraProvider, CameraDescriptor
from timelapse.ui.resources import Resources


class CamPicker(QWidget):
    """Camera picker widget: camera list + video preview."""

    camera_changed: Signal = Signal(CameraDescriptor)
    camera: Camera = DummyCamera()

    def __init__(self, descriptor: CameraDescriptor, camera_provider: CameraProvider, no_image: QPixmap = None):
        super().__init__()
        self.camera_provider: CameraProvider = camera_provider
        self.cameras: Sequence[CameraDescriptor] = self.camera_provider.list_webcams()
        self.camera = self.camera_provider.open_camera(descriptor)
        self.no_image: QPixmap = no_image or QPixmap(Resources.NO_IMAGE)
        self._timer: QTimer | None = None
        self._init_ui()
        self._preview_cam(0)

    def _init_ui(self):
        """Initialize ui."""
        self._layout: QLayout = QVBoxLayout()

        self._cam_list_combo = QComboBox()
        self._cam_list_combo.addItems([camera.name for camera in self.cameras])
        self._cam_list_combo.currentIndexChanged.connect(self._preview_cam)
        self._cam_list_combo.currentIndexChanged.emit(0)
        self._layout.addWidget(self._cam_list_combo)

        self._frame_container = QLabel()
        self._layout.addWidget(self._frame_container)

        self.setLayout(self._layout)

    def _preview_cam(self, index: int):
        """Preview ith camera from the list."""
        self.camera.close()
        descriptor = self.cameras[index]
        self.camera = self.camera_provider.open_camera(descriptor)
        self.camera_changed.emit(descriptor)

    def _display_frame(self):
        """Preview frame from the camera."""
        frame = self.camera.read_frame()
        if frame is not None:
            self._frame_container.setPixmap(frame.scale(0.5).to_pixmap())
        else:
            self._frame_container.setPixmap(self.no_image)

    def start_preview(self, period: int = 100):
        """Start playing video from the current camera."""
        if self._timer is not None:
            self._timer.stop()
        self._timer: QTimer = QTimer(self)
        self._timer.timeout.connect(self._display_frame)
        self._timer.start(period)

    def stop_preview(self):
        """Stop playing video from the current camera."""
        if self._timer is not None:
            self._timer.stop()
        self.camera.close()

    def showEvent(self, event: QShowEvent) -> None:
        """Start camera preview on show()."""
        super().showEvent(event)
        QTimer().singleShot(500, self.start_preview)

    def hideEvent(self, event: QHideEvent) -> None:
        """Stop camera preview."""
        super().hideEvent(event)
        self.stop_preview()
