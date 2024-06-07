import asyncio
import logging
import os
import signal
import sys

import gmos_logging
import quamash
from PyQt5 import QtCore, QtQml
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine

from gmbox_sidebar import resources  # noqa: F401
from gmbox_sidebar.dbus import SidebarDBusInterface
from gmbox_sidebar.sidebar_config import (
    CommonConfiguration,
    SidelinkConfiguration,
    SidebarMonitorPosition,
)
from gmbox_sidebar.settings import DEFAULT_SIDEBAR_STATUS_ICON

from gmbox_sidebar.utils import ScreenGeometry
from gmbox_sidebar.models import SidebarButtonsModel

logger = logging.getLogger(__name__)

signal.signal(signal.SIGINT, signal.SIG_DFL)


class SidebarConfiguration:
    def __init__(self):
        self.app: QGuiApplication = QGuiApplication(sys.argv)
        self.main_qml_path: str = "qrc:/qml/Main.qml"
        self.sidebar_position = SidebarMonitorPosition()
        self.sidebar_configuration = CommonConfiguration()

    def create_qml_engine(self) -> QQmlApplicationEngine:
        self.app.setApplicationName("gmbox-sidebar")

        loop = quamash.QEventLoop(self.app)
        asyncio.set_event_loop(loop)

        def handler(*args):
            *_, message = args
            logger.error(message)

        QtCore.qInstallMessageHandler(handler)
        return QQmlApplicationEngine()

    def configure_ui(self, engine: QtQml.QQmlApplicationEngine) -> None:
        sidebar = SidebarButtonsModel(parent=engine)
        status_icon = DEFAULT_SIDEBAR_STATUS_ICON
        for sidelink in SidelinkConfiguration().find_sidelinks():
            if sidelink.status_icon:
                status_icon = sidelink.status_icon
            sidebar.add_side_link(sidelink)

        engine.rootContext().setContextProperty("statusIcon", status_icon)
        engine.rootContext().setContextProperty("sidebarModel", sidebar)
        engine.rootContext().setContextProperty("sidebarPosition", self.sidebar_position)
        engine.rootContext().setContextProperty("screenGeometry", ScreenGeometry().available_screens)

        engine.load(self.main_qml_path)
        if not engine.rootObjects():
            raise RuntimeError("Failed to load QML")

    @property
    def enabled(self):
        return self.sidebar_configuration.enabled

    @property
    def visible_sides(self):
        return self.sidebar_position.visible_sides()


def main():
    gmos_logging.log.init_logging(process_name="gmbox-sidebar")
    gmos_logging.exceptions.setup_exception_hook()
    sidebar = SidebarConfiguration()
    if not sidebar.enabled:
        logger.info("The sidebar is disabled in config file!")
        sys.exit(0)

    engine = sidebar.create_qml_engine()
    try:
        sidebar.configure_ui(engine)
        if not engine.rootObjects():
            raise RuntimeError("Failed to load QML")
    except RuntimeError as error:
        logger.critical(f"Caught error: {error}")
    logger.info("Running gmbox-sidebar...")

    with asyncio.get_event_loop() as loop:
        loop.create_task(SidebarDBusInterface.create_and_run(widget=sidebar.sidebar_position))
        loop.run_forever()

    return os.EX_OK


if __name__ == "__main__":
    sys.exit(main())
