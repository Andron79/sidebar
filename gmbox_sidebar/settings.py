import configparser
import enum
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Generator, Optional, TextIO, Union, Tuple

logger = logging.getLogger(__name__)


# gmbox built in screen parameters
@dataclass
class GMBoxBuiltInScreen:
    NAME: str = "DSI1"
    MARGIN: int = 10
    WIDTH: int = 1280
    HEIGHT: int = 720


# sidebar configs
SIDEBAR_DISABLE_KEY = "SIDEBAR_DISABLE"
SIDEBAR_VISIBLE_SIDES_KEY = "SIDEBAR_VISIBLE_SIDES"
USER_SETTINGS_FILENAME = ".gmbox-current-user-config"
USER_SETTINGS_SOURCE = Path.home() / USER_SETTINGS_FILENAME
SETTINGS_PATH = "/persistent/configs/gm-sidebar/"

# sidebar position on screens
SIDEBAR_SIDE_KEY = "SIDEBAR_POSITION"
SIDEBAR_MONITOR_SIDE_KEY = "SIDEBAR_MONITOR_SIDE"
SIDEBAR_MONITOR_SLIDER_KEY = "SIDEBAR_MONITOR_SLIDER_POSITION"
SIDEBAR_MONITOR_ID_KEY = "SIDEBAR_MONITOR_ID"
SIDEBAR_POSITION_SETTINGS_FILENAME = "sidebar_position.pkl"
SIDEBAR_POSITION_SETTINGS_SOURCE = Path(SETTINGS_PATH, SIDEBAR_POSITION_SETTINGS_FILENAME)


class MonitorSide(enum.IntEnum):
    RIGHT: int = 0
    LEFT: int = 1
    TOP: int = 2
    BOTTOM: int = 3


SIDEBAR_DEFAULT_SIDE_POSITION = MonitorSide.RIGHT
SIDEBAR_DEFAULT_MONITOR_SLIDER = 0.5
SIDEBAR_DEFAULT_MONITOR_ID = 0

# dbus interface sidebar
GMBOX_SIDEBAR_DBUS_NAME = "org.getmobit.sidebar"
GMBOX_SIDEBAR_INTERFACE_NAME = "org.getmobit.sidebar"
GMBOX_SIDEBAR_INTERFACE_SERVICE = "org.getmobit.sidebar"
GMBOX_SIDEBAR_PATH = "/"

# side-link confIg
SIDE_LINKS_CONFIGS_DIRECTORY = Path("/opt/getmobit/gm-sidebar/side-link")
PERSISTENT_SIDE_LINKS_CONFIGS_DIRECTORY = Path("/persistent/configs/gm-sidebar/side-link")
SIDE_LINK_CONFIG_FILE = "config.json"

DEFAULT_SIDEBAR_STATUS_ICON = "qrc:/icons/default.svg"


@dataclass
class SideLinkAppState:
    icon: Optional[str] = None
    icon_horizontal: Optional[str] = None
    command: Optional[str] = None
    visible: Optional[str] = bool
    enable: Optional[str] = bool
    status_icon: Optional[str] = None


@dataclass
class SideLinkApp:
    name: str
    update_hook: Optional[str] = None
    init_hook: Optional[str] = None
    service: Optional[str] = None
    path: Optional[str] = None
    interface: Optional[str] = None
    signal_name: Optional[str] = None
    state: SideLinkAppState = SideLinkAppState
    icon: Optional[str] = None
    icon_horizontal: Optional[str] = None
    command: Optional[str] = None
    visible: Optional[str] = bool
    enable: Optional[str] = bool
    status_icon: Optional[str] = None


@dataclass
class BooleanValues:
    TRUE: Tuple[str, ...] = ("true", "yes")
    FALSE: Tuple[str, ...] = ("false", "no")


def to_bool(value: Optional[Union[str, int, float]]) -> bool:
    """Parses string to boolean"""
    if value:
        if value.isdigit():
            return bool(int(value))
        if value.lower() in BooleanValues.TRUE:
            return True
        if value.lower() in BooleanValues.FALSE:
            return False
    return False


def add_section_header(properties_file: TextIO, header_name: Union[str, Path]) -> Generator:
    """
    ConfigParser requires at least one section header in a properties file.
    Our properties file doesn't have one, so add a header to it on the fly.
    """
    yield f"[{header_name}]\n"
    for line in properties_file:
        yield line


def get_parameter_from_ldap(
    parameter: str,
    config: configparser.ConfigParser,
    section: str = "LDAP",
    hidden: bool = False,
) -> Union[str, None]:
    if parameter not in config[section]:
        logger.warning(f'Option "{parameter}" was not obtained from LDAP')
        return None

    value = config[section][parameter]
    value = str(value).strip('"')

    if not value:
        logger.warning(f'Setting "{parameter}" came empty from LDAP')
        return None
    if not hidden:
        logger.info(f"{parameter}: {value}")
    else:
        logger.info(f"{parameter} obtained")
    return value
