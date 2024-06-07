import asyncio
import logging
import os
import signal
import sys
import gmos_logging

from PyQt5 import QtCore
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine

from gmbox_sidebar.sidebar_config import SidebarMonitorPosition
from gmbox_sidebar.utils import ScreenGeometry
from sidebarapps.sidebar_settings import resources  # noqa: F401
from sidebarapps.sidebar_settings.dbus import DBusClient
from sidebarapps.sidebar_settings.models import MonitorModel, SidebarScreen

import quamash

from sidebarapps.sidebar_settings.settings import MAIN_QML_PATH

logger = logging.getLogger(__name__)

signal.signal(signal.SIGINT, signal.SIG_DFL)


class SidebarSettingsConfiguration:
    def __init__(self):
        self.app: QGuiApplication = QGuiApplication(sys.argv)

    def create_qml_engine(self) -> QQmlApplicationEngine:
        self.app.setApplicationName("sidebar-settings")

        loop = quamash.QEventLoop(self.app)
        asyncio.set_event_loop(loop)

        def handler(*args):
            *_, message = args
            logger.error(message)

        QtCore.qInstallMessageHandler(handler)
        return QQmlApplicationEngine()


async def _main(engine):
    interface = await DBusClient.create_and_run()
    monitors = MonitorModel(interface=interface, parent=engine)
    for monitor in SidebarScreen().sidebar_settings_screens():
        monitors.add_monitor(monitor)

    sidebar_monitor_position = SidebarMonitorPosition()
    engine.rootContext().setContextProperty("monitorModel", monitors)
    engine.rootContext().setContextProperty("sidebarMonitorID", sidebar_monitor_position.monitor_id)
    engine.rootContext().setContextProperty("sidebarMonitorSide", sidebar_monitor_position.monitor_side)
    engine.rootContext().setContextProperty("sidebarSliderPosition", sidebar_monitor_position.slider_position)
    engine.rootContext().setContextProperty("visibleSides", sidebar_monitor_position.visible_sides)
    engine.rootContext().setContextProperty("screenGeometry", ScreenGeometry().available_screens)

    try:
        engine.load(MAIN_QML_PATH)
        if not engine.rootObjects():
            raise RuntimeError("Failed to load QML")

    except RuntimeError as error:
        logger.critical(f"Caught error: {error}")
        sys.exit(1)


def main():
    gmos_logging.log.init_logging(process_name="sidebar-settings")
    gmos_logging.exceptions.setup_exception_hook()
    sidebar_settings = SidebarSettingsConfiguration()
    engine = sidebar_settings.create_qml_engine()
    logger.info("Running sidebar-settings...")

    with asyncio.get_event_loop() as loop:
        loop.create_task(_main(engine))
        loop.run_forever()
    return os.EX_OK


if __name__ == "__main__":
    sys.exit(main())
