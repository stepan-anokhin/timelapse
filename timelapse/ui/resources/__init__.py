import os.path

from PyQt6.QtGui import QPixmap


class Resources:
    """Provides quick access to the app resources."""

    @staticmethod
    def path(name: str) -> str:
        """Resource path."""
        return os.path.join(os.path.dirname(__file__), name)

    NO_IMAGE: QPixmap = QPixmap(path("no_image.jpg"))
