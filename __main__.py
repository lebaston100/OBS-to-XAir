import time

import obsws_python as obs
import xair_api

mapping = {
    "START": 1,
    "BRB": 2,
    "END": 3,
    "LIVE": 4,
}  # set the mapping for the scene to channel mapping here. "scenename": "channel"


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
        scene = data.scene_name
        print(f"Switched to scene {scene}")
        for k, v in mapping.items():
            self._mixer.strip[v - 1].mix.on = k == scene

    def on_exit_started(self, _):
        print("OBS closing")
        self._event.unsubscribe()
        self.running = False


def main():
    with xair_api.connect(kind_mixer) as mixer:
        o = Observer(mixer)

        while o.running:
            time.sleep(0.5)


if __name__ == "__main__":
    kind_mixer = "XR18"

    main()
