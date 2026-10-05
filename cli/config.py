"""
Persistent Configuration Profiles & Peer Aliasing.
Loads and saves user-defined defaults and peer aliases from a local
TOML config file (e.g. ~/.config/meshvault/config.toml).

Issue #13 Deliverable.
"""

import os
import toml

DEFAULT_CONFIG_PATH = os.path.expanduser("~/.config/meshvault/config.toml")

# What a fresh config file looks like if none exists yet.
DEFAULT_CONFIG = {
    "defaults": {
        "interface": "eth0",
        "n": 5,
        "k": 3,
        "log_level": "info",
    },
    "peers": {
        # "192.168.1.50": "alice-laptop",
    },
}


def load_config(path: str = DEFAULT_CONFIG_PATH) -> dict:
    """
    Load the config file from `path`. If it doesn't exist yet, return a
    copy of the default config (does not create the file automatically —
    call save_config() explicitly if you want to persist defaults).
    """
    if not os.path.exists(path):
        return {
            "defaults": dict(DEFAULT_CONFIG["defaults"]),
            "peers": dict(DEFAULT_CONFIG["peers"]),
        }

    with open(path, "r", encoding="utf-8") as f:
        config = toml.load(f)

    config.setdefault("defaults", dict(DEFAULT_CONFIG["defaults"]))
    config.setdefault("peers", {})
    return config


def save_config(config: dict, path: str = DEFAULT_CONFIG_PATH) -> None:
    """
    Save `config` to `path`, creating the parent directory
    (e.g. ~/.config/meshvault/) if it doesn't exist yet.
    """
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        toml.dump(config, f)


def get_defaults(config: dict) -> dict:
    """
    Return the [defaults] section: preferred interface, N, K, log level.
    """
    return config.get("defaults", dict(DEFAULT_CONFIG["defaults"]))


def set_default(config: dict, key: str, value, path: str = DEFAULT_CONFIG_PATH) -> dict:
    """
    Update a single default value (e.g. set_default(config, "n", 7))
    and persist it to disk immediately.
    """
    config.setdefault("defaults", {})
    config["defaults"][key] = value
    save_config(config, path)
    return config


def add_peer_alias(
    config: dict, address: str, alias: str, path: str = DEFAULT_CONFIG_PATH
) -> dict:
    """
    Add or update a friendly name for a peer's IP/MAC address, e.g.
    add_peer_alias(config, "192.168.1.50", "alice-laptop").
    Persists the change to disk immediately.
    """
    config.setdefault("peers", {})
    config["peers"][address] = alias
    save_config(config, path)
    return config


def get_peer_alias(config: dict, address: str) -> str:
    """
    Look up a friendly name for a peer's address. Falls back to the raw
    address itself if no alias has been configured for it — so callers
    can always safely display get_peer_alias(config, ip) without checking
    for None first.
    """
    return config.get("peers", {}).get(address, address)
