import logging
import subprocess
from PyQt5.QtCore import QObject, pyqtSlot

from sidebarapps.logout.settings import KILL_SESSION_SCRIPT_PATH


logger = logging.getLogger(__name__)


class SessionKiller(QObject):
    def __init__(self, parent: QObject = None):
        QObject.__init__(self, parent)

    @pyqtSlot(name="killSession")
    def kill_session(self) -> None:
        try:
            kill_session = subprocess.run([KILL_SESSION_SCRIPT_PATH])
            logger.info(f"Closing user session ended with an exit code: {kill_session.returncode}")
        except FileNotFoundError as e:
            logger.error(f"Fail to run script: {e}")
