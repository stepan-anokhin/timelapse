import os.path


class Resources:
    """Provides quick access to the app resources."""

    @staticmethod
    def path(name: str) -> str:
        """Resource path."""
        return os.path.join(os.path.dirname(__file__), name)

    NO_IMAGE: str = path("no_image.jpg")
    START_SOUND: str = path("start.mp3")
