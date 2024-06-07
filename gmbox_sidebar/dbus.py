import logging

import dbus_next
from dbus_next.aio import MessageBus
from dbus_next.service import ServiceInterface, method

from gmbox_sidebar.settings import GMBOX_SIDEBAR_INTERFACE_NAME, GMBOX_SIDEBAR_PATH
from gmbox_sidebar.sidebar_config import SidebarMonitorPosition

logger = logging.getLogger(__name__)


class SidebarDBusInterface(ServiceInterface):
    def __init__(self, widget: SidebarMonitorPosition) -> None:
        super().__init__(GMBOX_SIDEBAR_INTERFACE_NAME)
        self.widget = widget

    @staticmethod
    async def create_and_run(widget):
        instance = SidebarDBusInterface(widget)
        bus = await MessageBus(bus_type=dbus_next.BusType.SESSION).connect()
        bus.export(GMBOX_SIDEBAR_PATH, instance)
        await bus.request_name(GMBOX_SIDEBAR_INTERFACE_NAME)
        logger.info(f'Sidebar D-Bus interface up on: "{GMBOX_SIDEBAR_INTERFACE_NAME}"')
        return instance

    @method(name="changeSettingsSidebar")
    def change_settings_sidebar(self) -> "b":  # noqa: F821
        self.widget.monitor_side = self.widget.get_monitor_side_from_config()
        self.widget.slider_position = self.widget.get_slider_position_from_config()
        self.widget.monitor_id = self.widget.get_monitor_id_from_config()
        return True
