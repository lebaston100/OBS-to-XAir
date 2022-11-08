# OBS-to-XAir

This is a small script that mutes, unmutes and toggles groups of channels on Behringer XAir Mixers depending on the current scene.

## Requirements

-   The [obs-websocket-v5 plugin](https://github.com/obsproject/obs-websocket/releases) (Version 5.0.0+)
    -   Note, this now comes included with OBS 28+
-   [obsws-python](https://github.com/aatikturk/obsws-python)
-   [xair-api](https://github.com/onyx-and-iris/xair-api-python)
-   Python 3.10 or greater

## Installation

-   First install [latest version of Python](https://www.python.org/downloads/).

    -   Ensure you tick `Add Python 3.x to PATH` during setup.

-   Download the repository files with git or the green `Code` button. Then in command prompt:

```
cd OBS-to-XAir
pip install .
```

## Configuration

-   Configure websocket settings within `OBS->Tools->obs-websocket Settings`

-   Open the included `config.toml` and set OBS host, port and password as well as the xair mixers ip.

    -   You may also set the kind of mixer in the script. (`XR12, XR16, XR18, MR18, X32`)

-   Set the scene to channel mutes mapping in `mapping.toml`.

## Usage

Simply run the script, there will be confirmation of mixer connection and OBS connection if everything is successful. Switch between the defined scenes.

Closing OBS will stop the script.

## Further notes

Since this script relies upon two interfaces, `obsws-python` and `xair-api` this code can be readily modified to interact with any OBS events and set any xair parameters. Check the README files for each interface for further details.

## Compatibility

This script was developed and tested with:

-   OBS 28.01
-   obs-websocket 5.0.1
-   A Midas MR18 and an X32 emulator.

## Special Thanks

-   OBS team and the obs-websocket developers + Behringer/Midas for the OSC protocol.
-   [Adem](https://github.com/aatikturk) for contributions towards the obsws-python wrapper.
-   [Onyx-and-Iris](https://github.com/onyx-and-iris) for contributions towards the obsws-python and xair-api wrappers.
