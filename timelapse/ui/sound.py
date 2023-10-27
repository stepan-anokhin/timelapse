from pathlib import Path

from PySide6.QtCore import QUrl
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput, QSoundEffect


def play_sound(path: Path):
    """Play sound."""
    player = QMediaPlayer()
    audio_output = QAudioOutput()
    player.setAudioOutput(audio_output)
    player.setSource(QUrl.fromLocalFile(str(path)))
    audio_output.setVolume(50)
    player.play()


def play_sound_effect(path: Path):
    """Play sound as effect (using different Qt API)."""
    effect = QSoundEffect()
    effect.setSource(QUrl.fromLocalFile(str(path)))
    # possible bug: QSoundEffect::Infinite cannot be used in setLoopCount
    effect.setLoopCount(-2)
    effect.play()
