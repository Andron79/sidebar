import asyncio
import logging
import sys

import quamash
from PyQt5 import QtCore, QtGui, QtQml
from PyQt5.QtQml import QQmlApplicationEngine

from sidebarapps.logout.utils import SessionKiller

from sidebarapps.logout import resources  # noqa: F401
import gmos_logging.exceptions
import gmos_logging.log

logger = logging.getLogger(__name__)


def create_qml_engine() -> QtQml.QQmlApplicationEngine:
    app = QtGui.QGuiApplication(sys.argv)
    app.setApplicationName("logout-app")

    loop = quamash.QEventLoop(app)
    asyncio.set_event_loop(loop)

    def handler(*args):
        *_, message = args
        logger.error(message)

    QtCore.qInstallMessageHandler(handler)
    return QQmlApplicationEngine()


def configure_ui(engine: QtQml.QQmlApplicationEngine) -> None:
    session_killer = SessionKiller(parent=engine)
    engine.rootContext().setContextProperty("sessionKiller", session_killer)
    engine.load("qrc:/ui/qml/LogoutWindow.qml")
    if not engine.rootObjects():
        raise RuntimeError("Failed to load QML")


def main():
    gmos_logging.log.init_logging(process_name="gmbox-logout")
    gmos_logging.exceptions.setup_exception_hook()

    engine = create_qml_engine()
    try:
        configure_ui(engine)
    except RuntimeError as error:
        logger.critical(f"Caught error: {error}")

    logger.info("Running gmbox-logout...")
    with asyncio.get_event_loop() as loop:
        loop.run_forever()


if __name__ == "__main__":
    sys.exit(main())
