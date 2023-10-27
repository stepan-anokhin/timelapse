import sys
from typing import List

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog

from timelapse.dummy import DummyCamera
from timelapse.model import Camera, CameraProvider
from timelapse.opencv import OpenCVCameraProvider
from timelapse.ui.cam_picker import CamPicker
from timelapse.ui.interval_picker import IntervalPicker


class MainWindow(QMainWindow):
    camera: Camera = DummyCamera()

    def __init__(self, camera_provider: CameraProvider):
        super().__init__()
        self.camera_provider: CameraProvider = camera_provider
        self.setWindowTitle("TimeLapse")

        content = QWidget()
        layout = QVBoxLayout()

        self.cam_picker = CamPicker(camera_provider)
        layout.addWidget(self.cam_picker)

        self.interval_picker = IntervalPicker()
        layout.addWidget(self.interval_picker)

        button = QPushButton("Select Directory")
        button.clicked.connect(self.select_dir)
        layout.addWidget(button)

        button = QPushButton("Start Recording")
        layout.addWidget(button)

        content.setLayout(layout)
        self.setCentralWidget(content)
        QTimer().singleShot(500, self.cam_picker.start)

    def select_dir(self):
        path = QFileDialog.getExistingDirectory(
            parent=self,
            caption="Select directory",
            options=QFileDialog.Option.DontUseNativeDialog,
        )
        print(path)


def main(qt_args: List[str]):
    app = QApplication(qt_args)
    window = MainWindow(OpenCVCameraProvider())
    window.show()

    app.exec()


if __name__ == '__main__':
    main(qt_args=sys.argv)
