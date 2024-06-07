import logging
from typing import List

from PyQt5.QtCore import QCoreApplication, QRect
from gmbox_sidebar.settings import GMBoxBuiltInScreen

logger = logging.getLogger(__name__)


class ScreenGeometry:
    def __init__(self):
        self.app = QCoreApplication.instance()

    @property
    def available_screens(self) -> List[QRect]:
        try:
            return [screen.geometry() for screen in self.app.screens() if screen.name() != GMBoxBuiltInScreen.NAME]
        except IndexError as e:
            raise RuntimeError("Monitors not found") from e
