# OBS-to-XAir
This is a small script that mutes and unmutes channels on Behringer XAir Mixers depending on the current scene.

## Requirements

- The [obs-websocket plugin](https://github.com/Palakis/obs-websocket/releases) (Version >= 4.5.1)
- A fairly recent version of Python 3
- [websocket-client](https://github.com/websocket-client/websocket-client)
- [python-osc](https://github.com/attwad/python-osc)

## General Setup

- Install Python 3.x.x 
  - On Windows: Make sure you trick "Add Python 3.x to PATH" in the setup
- Make sure you also install pip
- Open up a command line and execute these commands to install the required pip modules:
  - pip install python-osc
  - pip install websocket-client
- OBS Websocket:
  - Download the installer from the link above and run it
  - Start OBS, open the "Tools" menu and select "websocket server settings"
  - Make sure that "Enable Websocket server" is checked, "Server Port" is 4444 and "Enable authentification" is unchecked

## Configuration

You have to configure your scene-to-channel mapping and the IP settings. Open up the .py file with a text editor.

- The mapping:
This python dict resolves the OBS scene names to the XAir channels. 3 Channels come pre-set as a template.
The format follows the rule "scene name": "mixer channel".
"scene name" is the scene name in OBS which you want to pair to a mixer channel. "mixer channel" is the channel on the XAir mixer. Important: If you use the lower channels 1-9 you have to add zero-padding so "1" becomes "01" and so on. You can find all available channel names besides the normal 01-16 in the "parameters.txt" when you download the latest mixer firmware zip.

- OBS IP and Port:
In line 9 and 10 you can set the IP and port from the machine that runs OBS. If you are running the script locally you don't need to change anything.

- XAir Mixer IP:
In line 11 you need to set the IP address of your XAir Mixer. The OSC Port can't be changed so it's hardcoded.

## Usage

Just run the script, either from the command line or with a double-click. There will be no further output besides "Websocket open" when it's running. If the connection to OBS is broken, you will get an error.

## Compatibility

This script was developed and tested with:
- OBS 23.1.0
- obs-websocket 4.5.1
- A Behringer XR18

It should theoretically also work with the XR12, XR16 and X32 but i cannot validate this myself. Feel free to let me know if it worked for you.