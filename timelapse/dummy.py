from typing import Sequence

import numpy as np

from timelapse.model import Camera, CameraProvider, CameraDescriptor


class DummyCamera(Camera):
    """Dummy camera."""

    @property
    def is_open(self) -> bool:
        return False

    def close(self):
        pass

    def read_frame(self) -> np.ndarray | None:
        return None


class DummyProvider(CameraProvider):
    """Dummy camera provider."""

    def list_webcams(self) -> Sequence[CameraDescriptor]:
        return [CameraDescriptor(None, "No camera")]

    def open_camera(self, descriptor: CameraDescriptor) -> Camera:
        return DummyCamera()