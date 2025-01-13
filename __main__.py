"""
This script connects to an XAir mixer and OBS (Open Broadcaster Software) to control the mixer based on OBS scene changes.
Classes:
    Observer: Handles events from OBS and controls the XAir mixer.
Functions:
    load_config(config: str) -> dict: Loads a configuration file in TOML format.
    parse_args() -> argparse.Namespace: Parses command-line arguments.
    main(): Main function to parse arguments, configure logging, load configuration, and start the XAir mixer observer.
Usage:
    Run this script with optional arguments for configuration file path and logging level.
    Example: python . --config path/to/config.toml --debug
"""

import argparse
import logging
import threading
from pathlib import Path
from typing import Callable, Mapping

import obsws_python as obs
import xair_api

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib


class Observer:
    """
    Observer class to handle events from OBS (Open Broadcaster Software) and control an XAir mixer.
    Attributes:
        _mixer (xair_api.xair.XAirRemote): The XAir mixer remote control instance.
        _stop_event (threading.Event): Event to signal stopping of the observer.
        _mapping (dict): Mapping of OBS scenes to mixer actions.
        _request (obs.ReqClient): OBS request client for sending requests.
        _event (obs.EventClient): OBS event client for receiving events.
    Methods:
        __enter__(): Enter the runtime context related to this object.
        __exit__(exc_type, exc_value, exc_traceback): Exit the runtime context related to this object.
        on_current_program_scene_changed(data: type) -> None: Handles the event when the current program scene changes.
        _mute_handler(i): Mutes the specified mixer strip.
        _unmute_handler(i): Unmutes the specified mixer strip.
        _toggle_handler(i): Toggles the mute state of the specified mixer strip.
        on_exit_started(_): Handles the event when OBS is closing.
    """

    def __init__(
        self, mixer: xair_api.xair.XAirRemote, stop_event: threading.Event, config: dict
    ):
        self._mixer = mixer
        self._stop_event = stop_event
        self._mapping = config["scene_mapping"]
        self._request = obs.ReqClient(**config["obs"])
        self._event = obs.EventClient(**config["obs"])
        self._event.callback.register(
            (self.on_current_program_scene_changed, self.on_exit_started)
        )
        resp = self._request.get_version()
        print(
            f"Connected to OBS version:{resp.obs_version} "
            f"with websocket version:{resp.obs_web_socket_version}"
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        for client in (self._request, self._event):
            client.disconnect()

    def on_current_program_scene_changed(self, data: type):
        """
        Handles the event when the current program scene changes.
        Args:
            data: An object containing information about the scene change event.
                  It is expected to have an attribute `scene_name` which is the name of the new scene.
        Returns:
            None
        """

        scene = data.scene_name
        print(f"Switched to scene {scene}")

        if not (map_ := self._mapping.get(scene)):
            return

        actions: Mapping[str, Callable] = {
            "mute": self._mute_handler,
            "unmute": self._unmute_handler,
            "toggle": self._toggle_handler,
        }

        for action, indices in map_.items():
            if action in actions:
                for i in indices:
                    actions[action](i - 1)

    def _mute_handler(self, i):
        self._mixer.strip[i].mute = True

    def _unmute_handler(self, i):
        self._mixer.strip[i].mute = False

    def _toggle_handler(self, i):
        self._mixer.strip[i].mute = not self._mixer.strip[i].mute

    def on_exit_started(self, _):
        print("OBS closing")
        self._stop_event.set()


def load_config(config: str) -> dict:
    """
    Load a configuration file in TOML format.
    Args:
        config (str): The filepath/name of the configuration file to load.
    Returns:
        dict: The contents of the configuration file as a dictionary.
    Raises:
        FileNotFoundError: If the configuration file does not exist.
        tomllib.TOMLDecodeError: If there is an error decoding the TOML file.
    """

    def get_filepath() -> Path | None:
        for filepath in (
            Path(config),
            Path.cwd() / config,
            Path(__file__).parent / config,
            Path.home() / ".config" / "xair-obs" / config,
        ):
            if filepath.is_file():
                return filepath
        return None

    if not (filepath := get_filepath()):
        raise FileNotFoundError(f"Config file {config} not found")
    try:
        with open(filepath, "rb") as f:
            return tomllib.load(f)
    except tomllib.TOMLDecodeError as e:
        raise tomllib.TOMLDecodeError(f"Error decoding config file {filepath}") from e


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="OBS to Xair Controller")
    parser.add_argument(
        "-c", "--config", default="config.toml", help="Path to the config file"
    )
    parser.add_argument(
        "-d",
        "--debug",
        help="Debug output",
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
        default=logging.WARNING,
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="Verbose output",
        action="store_const",
        dest="loglevel",
        const=logging.INFO,
    )
    args = parser.parse_args()
    return args


def main():
    """
    Main function to parse arguments, configure logging, load configuration,
    and start the XAir mixer observer.
    This function performs the following steps:
    1. Parses command-line arguments.
    2. Configures logging based on the provided log level.
    3. Loads the configuration file.
    4. Connects to the XAir mixer using the configuration.
    5. Starts an observer to monitor the mixer and waits for events.
    The function blocks until a stop event is received.
    Args:
        None
    Returns:
        None
    """

    args = parse_args()
    logging.basicConfig(level=args.loglevel)

    config = load_config(args.config)

    with xair_api.connect(**config["xair"]) as mixer:
        print(f"Connected to {mixer.kind} mixer at {mixer.xair_ip}:{mixer.xair_port}")
        stop_event = threading.Event()

        with Observer(mixer, stop_event, config):
            stop_event.wait()


if __name__ == "__main__":
    main()
