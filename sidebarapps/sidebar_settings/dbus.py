import logging

from dbus_next import BusType
from dbus_next.aio import MessageBus

from sidebarapps.sidebar_settings.settings import SIDEBAR_PATH, SIDEBAR_INTERFACE_NAME

logger = logging.getLogger(__name__)


class DBusClient:
    def __init__(self, interface):
        self.interface = interface

    @staticmethod
    async def create_and_run():
        bus = await MessageBus(bus_type=BusType.SESSION).connect()
        introspection = await bus.introspect(SIDEBAR_INTERFACE_NAME, SIDEBAR_PATH)
        proxy_object = bus.get_proxy_object(SIDEBAR_INTERFACE_NAME, SIDEBAR_PATH, introspection)
        interface = proxy_object.get_interface(SIDEBAR_INTERFACE_NAME)
        logger.info("Running sidebar D-Bus client...")
        return DBusClient(interface=interface)

    async def send_modified_settings(self) -> "b":  # noqa: F821
        return await self.interface.call_change_settings_sidebar()
