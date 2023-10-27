from timelapse.dummy import DummyProvider
from timelapse.model import CameraProvider
from timelapse.opencv import OpenCVCameraProvider


def resolve_provider() -> CameraProvider:
    """Resolve camera provider."""
    provider = OpenCVCameraProvider()
    if provider.list_webcams():
        return provider
    return DummyProvider()
