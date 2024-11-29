import soco

# Discover all Sonos devices on your local network
devices = soco.discover()
print(devices)

if devices:
    print("Found Sonos devices:")
    for device in devices:
        print(device.player_name)
else:
    print("No Sonos devices found on the network.")
