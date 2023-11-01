import os.path
from pathlib import Path

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QHBoxLayout, QFileDialog, QPushButton


class PathSelector(QWidget):
    """Destination path selector."""

    path_changed: Signal = Signal(Path)

    def __init__(self, default_path: Path = None):
        super().__init__()
        self.path: Path = os.path.abspath(default_path or Path.home())
        self._setup_ui()

    def _setup_ui(self):
        """Set up widget contents."""
        self._label = QLabel("Save frames in")
        self._path_edit = QLineEdit()
        self._path_edit.setText(str(self.path))
        self._path_edit.textEdited.connect(self._text_changed)
        self._browse_button = QPushButton("Browse")
        self._browse_button.clicked.connect(self._on_browse)

        self._layout = QHBoxLayout()
        self._layout.addWidget(self._label)
        self._layout.addWidget(self._path_edit)
        self._layout.addWidget(self._browse_button)
        self.setLayout(self._layout)

        self.path_changed.connect(lambda path: self._path_edit.setText(str(path)))

    def _text_changed(self, new_text: str):
        """Handle text input changed."""
        self.path = Path(new_text)
        self.path_changed.emit(self.path)

    def _on_browse(self):
        """Handle 'Browse' button."""
        selected_path = QFileDialog.getExistingDirectory(
            parent=self,
            caption="Select directory",
            options=QFileDialog.Option.DontUseNativeDialog,
            dir=str(self.path),
        )
        self.path = Path(selected_path or self.path).absolute()
        self.path_changed.emit(self.path)
