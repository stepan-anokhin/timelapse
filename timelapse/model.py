import abc
from abc import abstractmethod
from dataclasses import dataclass
from types import TracebackType
from typing import Any, Sequence, ContextManager

import cv2
import numpy as np
from PyQt6.QtGui import QImage, QPixmap


@dataclass
class Frame:
    """Wrapper around retrieved frame."""
    data: np.ndarray

    def scale(self, factor: float) -> "Frame":
        """Create scaled frame copy."""
        width = int(self.data.shape[1] * factor)
        height = int(self.data.shape[0] * factor)
        return Frame(cv2.resize(self.data, (width, height), interpolation=cv2.INTER_AREA))

    def to_image(self, format: QImage.Format = QImage.Format.Format_BGR888) -> QImage:
        """Convert frame data to QImage."""
        return QImage(self.data, self.data.shape[1], self.data.shape[0], format)

    def to_pixmap(self, format: QImage.Format = QImage.Format.Format_BGR888) -> QPixmap:
        """Convert frame data to QPixmap."""
        return QPixmap.fromImage(self.to_image(format))


class Camera(ContextManager):
    """Abstract camera."""

    def __enter__(self) -> "Camera":
        """Enter the context."""
        return self

    def __exit__(self, __exc_type, __exc_value, __traceback: TracebackType | None) -> bool | None:
        """Exit the context."""
        self.close()
        return None

    @property
    @abstractmethod
    def is_open(self) -> bool:
        """Check if the camera is open."""

    @abstractmethod
    def close(self):
        """Release the camera."""

    @abstractmethod
    def read_frame(self) -> Frame | None:
        """Get a single frame."""


@dataclass(frozen=True)
class CameraDescriptor:
    """Camera descriptor.

    Required to identify camera without accessing it.
    """
    id: Any
    name: str


class CameraProvider(abc.ABC):
    """Abstract Camera provider."""

    @abstractmethod
    def list_webcams(self) -> Sequence[CameraDescriptor]:
        """List available cameras."""

    @abstractmethod
    def open_camera(self, descriptor: CameraDescriptor) -> Camera:
        """Get access to the Camera."""
