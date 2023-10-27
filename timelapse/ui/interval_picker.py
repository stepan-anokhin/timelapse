from typing import Sequence

from PySide6.QtCore import Signal
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QComboBox, QHBoxLayout

from timelapse.model import TimeUnit, TimeUnits


class TimeIntervalPicker(QWidget):
    """Choose time interval between consequent frames."""

    interval_changed: Signal = Signal(int)

    def __init__(self, amount: int = 10, unit: TimeUnit = TimeUnits.SEC, units: Sequence[TimeUnit] = TimeUnits.ALL):
        super().__init__()
        if unit not in units:
            raise ValueError(f"{unit} is not among known units: {units}")
        self.amount: int = amount
        self.units: Sequence[TimeUnit] = units
        self.unit: TimeUnit = unit
        self._setup_ui()

    def _setup_ui(self):
        """Set up contents."""
        self._label = QLabel("Capture frame every")
        self._amount_input = QLineEdit()
        self._amount_input.setValidator(QIntValidator(0, 10 ** 6, self))
        self._amount_input.setText(str(self.amount))
        self._amount_input.textEdited.connect(self._amount_changed)
        self._time_unit_input = QComboBox()
        self._time_unit_input.addItems([unit.name for unit in self.units])
        self._time_unit_input.setCurrentIndex(self.units.index(self.unit))
        self._time_unit_input.currentIndexChanged.connect(self._unit_changed)

        self._layout = QHBoxLayout()
        self._layout.addWidget(self._label)
        self._layout.addWidget(self._amount_input)
        self._layout.addWidget(self._time_unit_input)
        self.setLayout(self._layout)

    def _amount_changed(self, new_amount: str):
        """Handle amount changed."""
        self.amount = int(new_amount)
        self.interval_changed.emit(self.amount * self.unit.millis)

    def _unit_changed(self, index: int):
        """Handle time-unit changed."""
        self.unit = self.units[index]
        self.interval_changed.emit(self.amount * self.unit.millis)
