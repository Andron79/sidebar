import asyncio
import logging
from collections import deque

from typing import Any, Dict, List
from PyQt5.QtGui import QScreen
from dataclasses import fields, dataclass

from gmbox_sidebar.settings import (
    GMBoxBuiltInScreen,
    SIDEBAR_MONITOR_ID_KEY,
    SIDEBAR_MONITOR_SLIDER_KEY,
    SIDEBAR_MONITOR_SIDE_KEY,
)

from PyQt5.QtCore import QAbstractListModel, QCoreApplication, QModelIndex, Qt, pyqtSlot

from gmbox_sidebar.sidebar_config import SidebarMonitorPosition

logger = logging.getLogger(__name__)

send_dbus_task = None


@dataclass
class Monitor:
    monitor_id: int
    name: str
    port: str


class SidebarScreen:
    def __init__(self):
        self.app = QCoreApplication.instance()
        self.primary_screen: QScreen = self.app.primaryScreen()
        self._monitors_list: List[Monitor] = []

    def sidebar_settings_screens(self) -> List[Monitor]:
        screens = [screen for screen in self.app.screens() if screen.name() != GMBoxBuiltInScreen.NAME]
        for index, screen in enumerate(screens):
            self._monitors_list.append(Monitor(monitor_id=index, name=screen.manufacturer(), port=screen.name()))
        try:
            return self._monitors_list
        except IndexError as e:
            raise RuntimeError("Monitors not found") from e


class MonitorModel(QAbstractListModel):
    def __init__(self, interface, parent=None) -> None:
        super().__init__(parent)
        self._monitor_list = []
        self.interface = interface
        self.sidebar_monitor_position = SidebarMonitorPosition()
        self.queue = deque()

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        if index.row() >= self.rowCount():
            return None
        monitor = self._monitor_list[index.row()]
        name = self.roleNames().get(role)
        if name is not None:
            return getattr(monitor, name.decode())
        return None

    def roleNames(self) -> Dict[int, bytes]:
        roles_dict = {}
        for i, field in enumerate(fields(Monitor)):
            roles_dict[Qt.UserRole + i] = field.name.encode()
        return roles_dict

    def rowCount(self, parent: QModelIndex = None) -> int:
        return len(self._monitor_list)

    def add_monitor(self, monitor: Monitor) -> None:
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._monitor_list.append(monitor)
        self.endInsertRows()

    @pyqtSlot(int, int, float)
    def set_sidebar_settings(self, monitor_id: int, monitor_side: int, slider_position: float) -> None:
        self.sidebar_monitor_position.save_sidebar_position_config(
            {
                SIDEBAR_MONITOR_ID_KEY: monitor_id,
                SIDEBAR_MONITOR_SIDE_KEY: monitor_side,
                SIDEBAR_MONITOR_SLIDER_KEY: slider_position,
            }
        )
        global send_dbus_task

        if send_dbus_task and not send_dbus_task.done():
            # пропускаем отправку сообщения в dbus, если отправка предыдущего еще не завершена, чтобы не загружать
            # dbus шину
            return
        send_dbus_task = asyncio.create_task(self.interface.send_modified_settings())
