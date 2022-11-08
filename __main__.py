import logging
import time
from pathlib import Path

import obsws_python as obs
import xair_api

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

logging.basicConfig(level=logging.disable())


def _get_mapping():
    filepath = Path.cwd() / "mapping.toml"
    with open(filepath, "rb") as f:
        return tomllib.load(f)


mapping = _get_mapping()


class Observer:
    def __init__(self, mixer):
        self._mixer = mixer
        self._request = obs.ReqClient()
        self._event = obs.EventClient()
        self._event.callback.register(
            (self.on_current_program_scene_changed, self.on_exit_started)
        )
        self.running = True
        resp = self._request.get_version()
        info = (
            f"Connected to OBS version:{resp.obs_version}",
            f"with websocket version:{resp.obs_web_socket_version}",
        )
        print(" ".join(info))

    def on_current_program_scene_changed(self, data):
        def ftoggle(i):
            self._mixer.strip[i - 1].mix.on = not self._mixer.strip[i - 1].mix.on

        def fset(i, is_muted):
            self._mixer.strip[i - 1].mix.on = is_muted

        scene = data.scene_name
        print(f"Switched to scene {scene}")
        if map_ := mapping.get(scene):
            for key in map_.keys():
                if key == "toggle":
                    [ftoggle(i) for i in map_[key]]
                else:
                    [fset(i, key == "mute") for i in map_[key]]

    def on_exit_started(self, _):
        print("OBS closing")
        self._event.unsubscribe()
        self.running = False


def main():
    filepath = Path.cwd() / "config.toml"
    with open(filepath, "rb") as f:
        kind_mixer = tomllib.load(f)["connection"].get("mixer")

    with xair_api.connect(kind_mixer) as mixer:
        o = Observer(mixer)

        while o.running:
            time.sleep(0.5)


if __name__ == "__main__":
    main()
