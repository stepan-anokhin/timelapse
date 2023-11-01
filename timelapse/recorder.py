import os
from datetime import datetime
from pathlib import Path

import cv2

from timelapse.config import TimelapseConfig
from timelapse.model import Camera, Frame


class TimelapseRecorder:
    """A class to record timelapse."""
    config: TimelapseConfig
    camera: Camera
    _group_count: int
    group_folder: Path

    def __init__(self, config: TimelapseConfig):
        self.config: TimelapseConfig = config
        os.makedirs(config.destination_directory, exist_ok=True)
        self.camera = config.camera_provider.open_camera(config.camera)
        self._start_group()

    @staticmethod
    def _timestamp() -> int:
        """Get current timestamp."""
        return int(datetime.now().timestamp() * 1000)

    def _start_group(self):
        """Start a new frame group."""
        timestamp_now = self._timestamp()
        group_name = f"frames_{timestamp_now}"
        self._group_count = 0
        self.group_folder = self.config.destination_directory.joinpath(group_name)
        os.makedirs(self.group_folder, exist_ok=True)

    def capture_frame(self) -> Frame | None:
        """Capture a single frame."""
        for _ in range(self.config.skip):
            self.camera.read_frame()
        frame = self.camera.read_frame()
        if frame is not None:
            filename = f"frame_{self._timestamp()}.jpg"
            path = self.group_folder.joinpath(filename)
            cv2.imwrite(str(path), frame.data)
        return frame

    def close(self):
        """Release resources."""
        self.camera.close()
