import fastjsonschema

SIDELINK_STATUS_SCHEMA = {
    "type": "object",
    "properties": {
        "icon": {"type": "string"},
        "icon_horizontal": {"type": "string"},
        "command": {"type": "string"},
        "visible": {"type": "boolean"},
        "enable": {"type": "boolean"},
        "status_icon": {"type": "string"},
    },
}

SIDELINK_CONFIG_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "service": {"type": "string"},
        "path": {"type": "string"},
        "interface": {"type": "string"},
        "signal_name": {"type": "string"},
        "icon": {"type": "string"},
        "icon_horizontal": {"type": "string"},
        "command": {"type": "string"},
        "visible": {"type": "boolean"},
        "enable": {"type": "boolean"},
        "state": SIDELINK_STATUS_SCHEMA,
    },
    "required": ["name"],
}

SideLinkConfigSchema = fastjsonschema.compile(SIDELINK_CONFIG_SCHEMA)
