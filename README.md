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

```bash
cd OBS-to-XAir
pip install .
```

## Configuration

-   Configure websocket settings within `OBS->Tools->obs-websocket Settings`

-   Open the included `config.toml`, use it to:
    -   Set the obs connection info `host`, `port` and `password`

    -   Set the mixer's `kind_id` and `ip`.
        -   Mixer kind_id may be any one of (`XR12, XR16, XR18, MR18, X32`)

    -   Set the scene to channel mapping.

## Usage

Simply run the script, there will be confirmation of mixer connection and OBS connection if everything is successful. Switch between the defined scenes.

Closing OBS will stop the script.

#### CLI options

-   `--config`: may be a full path to a config file or just a config name.
    -   If only a config name is passed the script will look in the following locations, returning the first config found:
        -   Current working directory (may be different from script location depending on how you launch the script)
        -   In the directory the script is located.
        -   `user home directory / .config / xair-obs`
-   `--debug`, `--verbose`: separate logging levels. Debug will produce a lot of logging output.

## Further notes

Since this script relies upon two interfaces, `obsws-python` and `xair-api` this code can be readily modified to interact with any OBS events and set any xair parameters. Check the README files for each interface for further details.

## Compatibility

This script was developed and tested with:

-   OBS 31.0.0
-   obs-websocket 5.5.4
-   A Midas MR18 and an X32 emulator.

## Special Thanks

-   [Lebaston](https://github.com/lebaston100) for the initial implementation of this script.
-   OBS team and the obs-websocket developers.
-   Behringer/Midas for making their mixers programmable!
-   [Adem](https://github.com/aatikturk) for contributions towards the obsws-python clients.
-   [Onyx-and-Iris](https://github.com/onyx-and-iris) for contributions towards the obsws-python and xair-api interfaces.
