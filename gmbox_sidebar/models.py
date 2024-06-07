import subprocess
from dataclasses import fields
from typing import Any, Dict, Union
from PyQt5 import QtDBus
from PyQt5.QtCore import (
    QModelIndex,
    Qt,
    QAbstractListModel,
    pyqtSlot,
    QObject,
    pyqtSignal,
)
import logging

from PyQt5.QtDBus import QDBusMessage

from gmbox_sidebar.settings import SideLinkApp
from gmbox_sidebar.sidebar_config import SidelinkConfiguration

logger = logging.getLogger(__name__)


class SidebarSlot(QObject):
    def __init__(self, name, parent=None) -> None:
        super().__init__(parent)
        self.name = name

    link_updated = pyqtSignal(str)

    @pyqtSlot(QDBusMessage)
    def on_update_notify_arrived(self, msg):
        self.link_updated.emit(self.name)


class SidebarButtonsModel(QAbstractListModel):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._sidelink_list = []
        self.sidelink_config = SidelinkConfiguration()

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> Any:
        if self.rowCount() > index.row() >= 0:
            sidelink = self._sidelink_list[index.row()]
            name = self.roleNames().get(role)
            if name:
                return getattr(sidelink, name.decode())
        return None

    def roleNames(self) -> Dict[Union[int, Any], bytes]:
        roles_dict = {}
        for i, field in enumerate(fields(SideLinkApp)):
            roles_dict[Qt.DisplayRole + i] = field.name.encode()
        return roles_dict

    def rowCount(self, index: QModelIndex = QModelIndex()) -> int:
        return len(self._sidelink_list)

    def add_side_link(self, sidelink: SideLinkApp) -> None:
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._sidelink_list.append(sidelink)
        if sidelink.update_hook:
            slot = SidebarSlot(parent=self, name=sidelink.name)
            slot.link_updated.connect(self.on_link_updated)
            self._dbus_connect(
                sidelink.service,
                sidelink.path,
                sidelink.interface,
                sidelink.signal_name,
                slot.on_update_notify_arrived,
            )
        self.endInsertRows()

    def _dbus_connect(
        self,
        dbus_name: str,
        path: str,
        interface: str,
        signal_name: str,
        slot: pyqtSlot,
    ) -> None:
        QtDBus.QDBusConnection.systemBus()
        bus = QtDBus.QDBusConnection.systemBus()
        bus.registerObject("/", self)
        bus.connect(dbus_name, path, interface, signal_name, slot)
        if bus.isConnected():
            logger.info(f'Success connect to DBus interface "{interface}"')

    def _get_sidelink_index_by_name(self, name) -> int:
        for index, sidelink in enumerate(self._sidelink_list):
            if sidelink.name == name:
                return index

    @pyqtSlot(str)
    def on_link_updated(self, name: str) -> None:
        index = self._get_sidelink_index_by_name(name=name)
        self.sidelink_config.update_sidelink_by_hook(sidelink=self._sidelink_list[index])
        self.dataChanged.emit(self.index(index, 0), self.index(0, index))

    @pyqtSlot(str)
    def execute(self, command: str) -> None:
        try:
            run_command = subprocess.run(command, shell=True, start_new_session=True)
            logger.info(f"Command '{command}' ended with an exit code: {run_command.returncode}")
        except FileNotFoundError as e:
            logger.error(f"Fail to run script: {e}")
