from typing import Sequence, List

import cv2

from timelapse.model import CameraProvider, CameraDescriptor, Camera, Frame


class OpenCVCameraProvider(CameraProvider):
    """Camera provider based on OpenCV VideoCapture API."""

    def list_webcams(self) -> Sequence[CameraDescriptor]:
        """List all available cameras."""

        # OpenCV has no API for listing available cameras.
        # So we need to detect them by checking one by one.
        # See: https://stackoverflow.com/a/57579550

        cameras: List[CameraDescriptor] = []
        for i in range(10):
            with OpenCVCamera(cv2.VideoCapture(i)) as camera:
                if camera.is_open:
                    cameras.append(CameraDescriptor(i, f"Camera {i}"))
        return cameras

    def open_camera(self, descriptor: CameraDescriptor) -> Camera:
        """Access camera via OpenCV API."""
        return OpenCVCamera(cv2.VideoCapture(descriptor.id))


class OpenCVCamera(Camera):
    """Wrapper around OpenCV VideoCapture device."""

    def __init__(self, device: cv2.VideoCapture):
        self._device: cv2.VideoCapture = device

    @property
    def is_open(self) -> bool:
        return self._device.isOpened()

    def close(self):
        self._device.release()

    def read_frame(self) -> Frame | None:
        """Read a single frame."""
        if not self.is_open:
            return None
        ret, data = self._device.read()
        if ret:
            return Frame(data)
