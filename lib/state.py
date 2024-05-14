### Utility methods for managing the main application state """
import lib.files as files
from random import randint

def make_default_state(root_dir: str) -> dict:
    stations = files.load_path(root_dir)
    return {
        "current": randint(0, len(stations) - 1),   # Current station index
        "stations": stations,   # List of stations & their respective states,
        "root": root_dir
    }

def set_state(state: dict, key: str, value: any) -> dict:
    state[key] = value
    return state

def root_dir(state: dict) -> str:
    return state["root"]


# Station-specific
def current_station(state: dict) -> dict:
    return state["stations"][state["current"]]

def current_station_state(state: dict) -> dict:
    return state["stations"][state["current"]]["state"]

def set_current_station_state(state: dict, key: str, value: any) -> dict:
    state["stations"][state["current"]][key] = value
    return state