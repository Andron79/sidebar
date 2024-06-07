import configparser
import json
import logging
import pickle
import subprocess
from pathlib import Path
from typing import Union, List

import fastjsonschema
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtProperty
from PyQt5.QtQml import QQmlListProperty

from gmbox_sidebar.schemas import SideLinkConfigSchema
from gmbox_sidebar.settings import (
    SideLinkApp,
    SIDE_LINKS_CONFIGS_DIRECTORY,
    PERSISTENT_SIDE_LINKS_CONFIGS_DIRECTORY,
    SIDE_LINK_CONFIG_FILE,
    SIDEBAR_DISABLE_KEY,
    USER_SETTINGS_SOURCE,
    add_section_header,
    get_parameter_from_ldap,
    to_bool,
    SIDEBAR_POSITION_SETTINGS_SOURCE,
    SIDEBAR_DEFAULT_MONITOR_SLIDER,
    SIDEBAR_DEFAULT_MONITOR_ID,
    SIDEBAR_VISIBLE_SIDES_KEY,
    MonitorSide,
)

logger = logging.getLogger(__name__)


class SidelinkConfiguration:
    @staticmethod
    def parse_sidelink_config(schema: SideLinkConfigSchema, sidelink_config_file: Path) -> Union[dict, None]:
        try:
            with Path.open(sidelink_config_file, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, PermissionError) as error:
            logger.warning(f"Failed to read file {sidelink_config_file}, error: {error}")
        except (json.JSONDecodeError, AttributeError) as error:
            logger.warning(f"Bad json schema in file {sidelink_config_file}, error: {error}")
            pass
        try:
            return schema(data)
        except fastjsonschema.JsonSchemaException as error:
            logger.warning(f"Failed to read file {sidelink_config_file}, error: {error}")
            return schema({})

    def _get_sidelink_app(self, sidelink_config_file: Path) -> SideLinkApp:
        return SideLinkApp(
            **self.parse_sidelink_config(schema=SideLinkConfigSchema, sidelink_config_file=sidelink_config_file)
        )

    def get_sidelink_app(self, sidelink_config_file: Path) -> Union[SideLinkApp, None]:
        if self._get_sidelink_app(sidelink_config_file).init_hook:
            try:
                command = subprocess.check_output(
                    self._get_sidelink_app(sidelink_config_file).init_hook,
                    shell=True,
                    stderr=subprocess.DEVNULL,
                )
                state = json.loads(command)
                if not state.get("visible"):
                    return None
            except subprocess.CalledProcessError as e:
                logger.error(f"Init hook error {e}")

                return None
        else:
            state = self._get_sidelink_app(sidelink_config_file).state
        return SideLinkApp(
            name=self._get_sidelink_app(sidelink_config_file).name,
            init_hook=self._get_sidelink_app(sidelink_config_file).init_hook,
            update_hook=self._get_sidelink_app(sidelink_config_file).update_hook,
            interface=self._get_sidelink_app(sidelink_config_file).interface,
            service=self._get_sidelink_app(sidelink_config_file).service,
            signal_name=self._get_sidelink_app(sidelink_config_file).signal_name,
            **state,
        )

    def find_sidelinks(
        self,
        sidelink_configs_directory: Path = SIDE_LINKS_CONFIGS_DIRECTORY,
        persistent_sidelink_configs_directory: Path = PERSISTENT_SIDE_LINKS_CONFIGS_DIRECTORY,
        sidelink_config_file: Path = SIDE_LINK_CONFIG_FILE,
    ) -> List[Union[SideLinkApp, None]]:
        sidelink_apps_list = []
        sidelinks_path_list = []
        for config_directory in [
            persistent_sidelink_configs_directory,
            sidelink_configs_directory,
        ]:
            if not config_directory.exists():
                continue
            sidelinks_path_list = [
                *sidelinks_path_list,
                *[directory for directory in sorted(config_directory.iterdir()) if directory.is_dir()],
            ]
        for directory in sidelinks_path_list:
            try:
                config_file = Path(directory, sidelink_config_file)
                sidelink_app = self.get_sidelink_app(sidelink_config_file=config_file)
                if not config_file.is_file() or sidelink_app in sidelink_apps_list or not sidelink_app:
                    logger.info(f"Sidelink {config_file} skipped...")
                    continue
                sidelink_apps_list.append(sidelink_app)
                logger.info(f'The "{sidelink_app.name}" app connected to sidebar from "{directory}" directory')
            except OSError as e:
                logger.error(f"Sidelink config file not found in {e} directory")
        return sidelink_apps_list

    @staticmethod
    def update_sidelink_by_hook(sidelink: SideLinkApp) -> SideLinkApp:
        try:
            command_data = json.loads(
                subprocess.check_output(sidelink.update_hook, shell=True, stderr=subprocess.DEVNULL)
            )
            logger.info(command_data["icon_horizontal"])
            sidelink.icon = command_data["icon"]
            sidelink.icon_horizontal = command_data["icon_horizontal"]
            sidelink.command = command_data["command"]
            sidelink.visible = command_data["visible"]
            sidelink.enable = command_data["enable"]
            sidelink.status_icon = command_data["status_icon"]
        except FileNotFoundError as e:
            logger.error(f"Fail to update sidelink: {e}")
        return sidelink


def get_sidebar_config(source, param):
    if not source.exists():
        return
    with Path.open(source, "r") as file:
        ldap_config = configparser.ConfigParser(strict=False, interpolation=None)
        ldap_config.read_file(add_section_header(file, "LDAP"), source=source)
        logger.info(f"Trying to import settings from {source}")
        config_value = get_parameter_from_ldap(param, ldap_config)
        return config_value


class CommonConfiguration:
    """
     Structure for stores information about the current general configuration of the sidebar
    (location, read from the user profile of the customization configuration)
    """

    def __init__(self, sidebar_disabled: bool = SIDEBAR_DISABLE_KEY, source: Union[str, Path] = USER_SETTINGS_SOURCE):
        self.sidebar_disabled: bool = sidebar_disabled
        self.source: Union[str, Path] = source

    @property
    def enabled(self) -> bool:
        config_value = None
        try:
            config_value = get_sidebar_config(source=self.source, param=self.sidebar_disabled)
        except configparser.ParsingError as e:
            logger.error(f"Parsing error: {e}")
        if config_value:
            return not to_bool(config_value.lower())
        return True


class SidebarMonitorPosition(QtCore.QObject):
    sideChanged = QtCore.pyqtSignal(int)
    sliderChanged = QtCore.pyqtSignal(float)
    monitorChanged = QtCore.pyqtSignal(int)

    def __init__(
        self,
        source: Union[str, Path] = SIDEBAR_POSITION_SETTINGS_SOURCE,
        user_settings_source: Union[str, Path] = USER_SETTINGS_SOURCE,
        cache_dict: dict = None,
    ):
        super().__init__(parent=None)
        self.source: Union[str, Path] = source
        self.user_settings_source = user_settings_source
        self._monitor_side: int = self.get_monitor_side_from_config()
        self._monitor_id: int = self.get_monitor_id_from_config()
        self._slider_position: float = self.get_slider_position_from_config()
        self.cache_dict = cache_dict

    @pyqtProperty(QQmlListProperty)
    def visible_sides(self) -> List[int]:
        config_value = None
        try:
            config_value = get_sidebar_config(source=self.user_settings_source, param=SIDEBAR_VISIBLE_SIDES_KEY)
        except configparser.ParsingError as e:
            logger.error(f"Parsing error: {e}")

        if not config_value:
            return [MonitorSide.RIGHT.value, MonitorSide.LEFT.value, MonitorSide.TOP.value, MonitorSide.BOTTOM.value]
        visible_sides_list = [
            side.upper() for side in config_value.split(",") if side.upper() in MonitorSide.__members__.keys()
        ]
        return [side.value for side in MonitorSide if side.name in visible_sides_list]

    def _read_sidebar_position_config(self) -> dict:
        try:
            with Path.open(self.source, "rb") as f:
                data = pickle.load(f)
                if isinstance(data, dict):
                    self.cache_dict = data
                    return self.cache_dict
                else:
                    return {}
        except FileNotFoundError as error:
            logger.warning(f"Failed to read file {self.source}, error: {error}")
            return {}
        except pickle.UnpicklingError as error:
            logger.warning(
                f"Failed to unpickle data from file {self.source}, error: {error}, " f"data from the cache was used"
            )
            return self.cache_dict
        except EOFError as error:
            logger.warning(f"Failed to read file {self.source}, error: {error}, data from the cache was used")
            return self.cache_dict
        except PermissionError as error:
            logger.warning(f"Failed to read file {self.source}, error: {error}")
            return {}

    def save_sidebar_position_config(self, data: dict) -> None:
        try:
            with Path.open(self.source, "wb", pickle.HIGHEST_PROTOCOL) as f:
                pickle.dump(data, f)
        except (FileNotFoundError, PermissionError) as error:
            logger.warning(f"Failed to save file {self.source}, error: {error}")

    def get_monitor_side_from_config(self) -> int:
        try:
            return self._read_sidebar_position_config()["SIDEBAR_MONITOR_SIDE"]
        except (ValueError, KeyError, AttributeError) as e:
            logger.info(f"{e} - sidebar starts in default position")
            return self.visible_sides[0]

    def get_slider_position_from_config(self) -> float:
        try:
            return self._read_sidebar_position_config()["SIDEBAR_MONITOR_SLIDER_POSITION"]
        except (ValueError, KeyError, AttributeError) as e:
            logger.info(f"{e} - sidebar slider starts in {SIDEBAR_DEFAULT_MONITOR_SLIDER} position")
            return SIDEBAR_DEFAULT_MONITOR_SLIDER

    def get_monitor_id_from_config(self) -> int:
        try:
            return self._read_sidebar_position_config()["SIDEBAR_MONITOR_ID"]
        except (ValueError, KeyError, AttributeError) as e:
            logger.info(f"{e} - sidebar starts in default monitor {SIDEBAR_DEFAULT_MONITOR_ID}")
            return SIDEBAR_DEFAULT_MONITOR_ID

    @pyqtProperty(int, notify=sideChanged)
    def monitor_side(self) -> int:
        return self._monitor_side

    @monitor_side.setter
    def monitor_side(self, value):
        if value == self._monitor_side:
            return
        self._monitor_side = value
        self.sideChanged.emit(value)

    @pyqtProperty(float, notify=sliderChanged)
    def slider_position(self) -> float:
        return self._slider_position

    @slider_position.setter
    def slider_position(self, value):
        if value == self._slider_position:
            return
        self._slider_position = value
        self.sliderChanged.emit(value)

    @pyqtProperty(int, notify=monitorChanged)
    def monitor_id(self) -> int:
        return self._monitor_id

    @monitor_id.setter
    def monitor_id(self, value):
        if value == self._monitor_id:
            return
        self._monitor_id = value
        self.monitorChanged.emit(value)
