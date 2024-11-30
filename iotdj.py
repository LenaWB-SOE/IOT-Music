from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, AUTH_URL, TOKEN_URL, API_BASE_URL, SECRET_KEY, TS_FEATURES_WRITE_API_KEY, TS_SONGS_WRITE_API_KEY, TS_EVIRON_WRITE_API_KEY
from spotify_client import SpotifyClient
from thingspeak_client import ThingSpeakClient
from flask import Flask, redirect, request, jsonify, session
import requests
from datetime import datetime
import time
import urllib.parse
import csv
import serial
import statistics as st
import threading
import os
import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

class iot_dj:
    def __init__(self, spotify_client, thingspeak_client):
        #initialising variables for when a new iotdj object is created
        #this is run when the application first runs
        self.spotify_client = spotify_client
        self.thingspeak_client = thingspeak_client
        self.in_error_mode = False

    def start_recording(self):
        self.music_recording_thread = threading.Thread(target=self.record_music) 
        self.environment_recording_thread = threading.Thread(target=self.ambient_readings)
        self.music_recording_thread.start()
        self.environment_recording_thread.start()

    def record_music(self):
        last_update_time = datetime.now().timestamp()
        last_track = None
        counter = 0
        update_interval = 60

        while True:
            current_time = datetime.now().timestamp()
            
            if current_time - last_update_time >= update_interval or counter == 0:
                current_track = self.spotify_client.get_current_track()
                if current_track != None and (counter == 0 or current_track['song uri'] != last_track['song uri']):
                    print(f"Current Track: {current_track.get('song')}")
                    self.thingspeak_client.update_songs_played_channel(current_track)

                    last_track = current_track

                last_update_time = current_time
                counter += 1

    def parse_sensor_data(self, buffer):
        # Convert buffer to ASCII
        ascii_data = buffer.decode('utf-8', errors='ignore')
        
        # Split by the delimiter (\r\n)
        packets = ascii_data.split("\r\n")
        #print(f"Packets: {packets}")
        results = []

        for packet in packets:
            if "Range" in packet:
                try:
                    # Extract the measurement value
                    value = int(packet.split("Range")[1].strip())
                    results.append(value)
                except ValueError:
                    continue  # Ignore invalid data
            elif "ON" in packet:
                results.append("ON")
            elif "OFF" in packet:
                results.append("OFF")
        return results, packets[-1]  # Return results and the last partial packet
    

    def radar_readings(self, serial, data, buffer):
        # Read available data from the serial port
        raw_data = serial.read(serial.in_waiting or 1)
        if raw_data:
            buffer += raw_data  # Append new data to the buffer

            if b"\r\n" in buffer:
                # Parse the buffer
                parsed_data, remaining_buffer = self.parse_sensor_data(buffer)
                # Retain the remaining partial packet for the next loop
                buffer = remaining_buffer.encode('utf-8', errors='ignore')

                # Process valid parsed data
                if parsed_data:
                    if isinstance(parsed_data[0], str) == False:
                        data.append(int(parsed_data[0]))

        return data


    def ambient_readings(self):
        # Configure the serial port for Radar
        ser = serial.Serial(
            port='/dev/serial0',  # UART port on Raspberry Pi
            baudrate=115200,      # LD2420 default baud rate
            timeout=1             # 1 second timeout for reading
        )

        # For reading LDR values via  ADC MCP3008
        spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI) # create the spi bus
        cs = digitalio.DigitalInOut(board.D24) # create the cs (chip select)
        mcp = MCP.MCP3008(spi, cs) # create the mcp object
        LDR = AnalogIn(mcp, MCP.P0) # create an analog input channel on pin 0

        # Initialize variables
        buffer = b""
        last_update_time = datetime.now().timestamp()
        update_interval = 60
        data = []

        while True:
            current_time = datetime.now().timestamp()

            data = self.radar_readings(ser, data, buffer)

            LightRawValue = LDR.value
            LightVoltage = LDR.voltage

            if current_time - last_update_time >= update_interval:
                if data:
                    average = st.mean(data)
                    print(f"-----------------------AVERAGE: {average}")
                    environment_dict = {
                        'Light RAW': LightRawValue,
                        'Light VOLTAGE': LightVoltage,
                        'Radar': average
                    }
                    self.thingspeak_client.update_environment_channel(environment_dict)
                    data = []
                    last_update_time = current_time

    def queue_song(self):
        # recommendation = spotify_client.create_recommendation(current_track['song_id'])
        # print(f"Song recommendation: {recommendation['song_name']}")
        waxwing = "spotify:track:4gGh7b3nKa4rlxyPLWcfTd"
        response = self.spotify_client.queue_song(waxwing)
        print(response)

    def fade_in_song(self, song_uri):
        return None


def main():
    print("Don't run this file")

if __name__ == "__main__":
    main()