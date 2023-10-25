import sys
from typing import List, Sequence

from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QComboBox, QLabel

from timelapse.dummy import DummyCamera
from timelapse.model import Camera, CameraProvider, CameraDescriptor
from timelapse.opencv import OpenCVCameraProvider


class MainWindow(QMainWindow):
    camera: Camera = DummyCamera()

    def __init__(self, camera_provider: CameraProvider):
        super().__init__()
        self.camera_provider: CameraProvider = camera_provider
        self.cameras: Sequence[CameraDescriptor] = tuple(self.camera_provider.list_webcams())

        self.setWindowTitle("TimeLapse")

        widget = QWidget()
        layout = QVBoxLayout()

        combo = QComboBox()
        combo.addItems([camera.name for camera in self.cameras])
        combo.currentIndexChanged.connect(self.set_preview)
        combo.currentIndexChanged.emit(0)
        self.combo = combo
        layout.addWidget(combo)

        self.frame_widget = QLabel()
        layout.addWidget(self.frame_widget)

        self.no_image = QPixmap("/timelapse/ui/resources/noimage.jpg")

        button = QPushButton("Start Recording")
        layout.addWidget(button)

        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def set_preview(self, index: int):
        """Select a new camera for preview."""
        camera_descriptor: CameraDescriptor = self.cameras[index]
        print("Selected", camera_descriptor.name)
        self.camera.close()
        self.camera = self.camera_provider.open_camera(camera_descriptor)

    def show_frame(self):
        frame = self.camera.read_frame()
        if frame is not None:
            self.frame_widget.setPixmap(frame.to_pixmap())
        else:
            self.frame_widget.setPixmap(self.no_image)


def main(qt_args: List[str]):
    app = QApplication(qt_args)
    window = MainWindow(OpenCVCameraProvider())
    window.show()

    timer = QTimer()
    timer.timeout.connect(window.show_frame)
    timer.start(10)

    app.exec()


if __name__ == '__main__':
    main(qt_args=sys.argv)
