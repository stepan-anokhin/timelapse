import sys
from typing import List

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog

from timelapse.dummy import DummyCamera
from timelapse.model import Camera, CameraProvider
from timelapse.opencv import OpenCVCameraProvider
from timelapse.ui.cam_picker import CamPicker
from timelapse.ui.interval_picker import IntervalPicker
from timelapse.ui.path_selector import PathSelector


class MainWindow(QMainWindow):
    camera: Camera = DummyCamera()

    def __init__(self, camera_provider: CameraProvider):
        super().__init__()
        self.camera_provider: CameraProvider = camera_provider
        self.setWindowTitle("TimeLapse")

        content = QWidget()
        layout = QVBoxLayout()

        self._cam_picker = CamPicker(camera_provider)
        layout.addWidget(self._cam_picker)

        self._interval_picker = IntervalPicker()
        layout.addWidget(self._interval_picker)

        self._path_selector = PathSelector()
        layout.addWidget(self._path_selector)

        button = QPushButton("Поехали!")
        layout.addWidget(button)

        content.setLayout(layout)
        self.setCentralWidget(content)
        QTimer().singleShot(500, self._cam_picker.start)

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
