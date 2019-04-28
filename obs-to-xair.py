#!/usr/bin/env python

import websocket, json
from time import sleep
from pythonosc import osc_message_builder
from pythonosc import udp_client

mapping = {"scene1": "01", "scene2": "02", "scene3": "03"} #set the mapping for the scene to channel mapping here. "scenename": "channel"
obsip = "localhost"     #set the obs machine ip here. localhost works if you run this script on the same machine.
obsport = "4444"        #set the ob websocket port here. 4444 is defult
xairip = "192.168.1.10" #set the xairip here

def ws1_on_message(ws, message):
    jsn = json.loads(message)
    if jsn["update-type"] == "SwitchScenes":
        for scene in mapping:
            if scene == jsn["scene-name"]:
                client.send_message("/ch/" + mapping[scene] + "/mix/on", 1)
            else:
                client.send_message("/ch/" + mapping[scene] + "/mix/on", 0)
    elif jsn["update-type"] == "TransitionBegin":
        for scene in mapping:
            if scene == jsn["to-scene"]:
                client.send_message("/ch/" + mapping[scene] + "/mix/on", 1)
            elif scene == jsn["from-scene"] and not jsn["name"] == "Cut":
                client.send_message("/ch/" + mapping[scene] + "/mix/on", 1)
            else:
                client.send_message("/ch/" + mapping[scene] + "/mix/on", 0)

def ws1_on_error(ws, error):
    print(error)

def ws1_on_close(ws):
    print("Websocket close")

def ws1_on_open(ws):
    print("Websocket open")

def ws1_start():
    while True:
        ws1.run_forever()
        print("Websocket restart")
        print("This most likely means that OBS is not open or you lost network connection.")
        sleep(1)

if __name__ == "__main__":
    client = udp_client.SimpleUDPClient(xairip, 10024)
    ws1 = websocket.WebSocketApp("ws://" + obsip + ":" + obsport, on_message = ws1_on_message, on_error = ws1_on_error, on_close = ws1_on_close)
    ws1.on_open = ws1_on_open
    ws1_start()
