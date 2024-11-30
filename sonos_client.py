import soco
from soco import SoCo
import time
import math

# Discover all Sonos devices on your local network
devices = soco.discover()
print(devices)

if devices:
    print("Found Sonos devices:")
    for device in devices:
        print(device.player_name)
else:
    print("No Sonos devices found on the network.")

# Replace with the IP address of your Sonos speaker
ip = "192.168.1.118"
speaker = SoCo(ip)

print(f"Connected to: {speaker.player_name}")

volume = 0
speaker.volume = volume
theta=0
t = 0

while True:
    volume = 30* (1 + math.sin(t))
    speaker.volume = volume
    t += 20
    time.sleep(0.2)

