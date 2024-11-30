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

class SensorClient:
    def __init__(self):
        # Configure the serial port for Radar
        self.RadarSerial = serial.Serial(
            port='/dev/serial0',  # UART port on Raspberry Pi
            baudrate=115200,      # LD2420 default baud rate
            timeout=1             # 1 second timeout for reading
        )

        # For reading LDR values via  ADC MCP3008
        self.spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI) # create the spi bus
        self.cs = digitalio.DigitalInOut(board.D24) # create the cs (chip select)
        self.mcp = MCP.MCP3008(self.spi, self.cs) # create the mcp object
        self.LDR = AnalogIn(self.mcp, MCP.P0) # create an analog input channel on pin 0

        self.buffer = b""

    def parse_sensor_data(self, buffer):
        # This is for interpretting the data received from the radar sensor that comes as a series of binary values that must be divided into packets and interpretted
        ascii_data = buffer.decode('utf-8', errors='ignore') # Convert buffer to ASCII
        packets = ascii_data.split("\r\n") # Split by the delimiter (\r\n)
        results = []

        for packet in packets:
            if "Range" in packet:
                try:
                    value = int(packet.split("Range")[1].strip()) # Extract the measurement value
                    results.append(value)
                except ValueError:
                    continue  # Ignore invalid data
            elif "ON" in packet:
                results.append("ON")
            elif "OFF" in packet:
                results.append("OFF")
        return results, packets[-1]  # Return results and the last partial packet
    

    def radar_readings_append(self, data_list):
        # Read available data from the serial port
        raw_data = serial.read(serial.in_waiting or 1)
        if raw_data:
            self.buffer += raw_data  # Append new data to the buffer

            if b"\r\n" in self.buffer:
                # Parse the buffer
                parsed_data, remaining_buffer = self.parse_sensor_data(self.buffer)
                # Retain the remaining partial packet for the next loop
                self.buffer = remaining_buffer.encode('utf-8', errors='ignore')

                # Process valid parsed data
                if parsed_data:
                    if isinstance(parsed_data[0], str) == False:
                        self.radar_data.append(int(parsed_data[0]))

        return data_list
    
    def light_raw_append(self, data_list):
        LightRawValue = self.LDR.value
        data_list.append(LightRawValue)

        return data_list
    
    def light_voltage_append(self, data_list):
        LightVoltage = self.LDR.voltage
        data_list.append(LightVoltage)

        return data_list


sensor_client = SensorClient()

def ambient_readings(sensor_client):

    # Initialize variables
    last_update_time = datetime.now().timestamp()
    update_interval = 60
    radar_data = []
    light_raw_data = []
    light_volt_data = []


    while True:
        current_time = datetime.now().timestamp()

        sensor_client.radar_readings_append(radar_data)
        sensor_client.light_raw_append(light_raw_data)
        sensor_client.light_voltage_append(light_volt_data)

        if current_time - last_update_time >= update_interval:
            if radar_data and light_raw_data and light_volt_data:
                radar_avg = st.mean(radar_data)
                lightraw_avg = st.mean(light_raw_data)
                lightvolt_avg = st.mean(light_volt_data)

                environment_dict = {
                    'Light RAW': lightraw_avg,
                    'Light VOLTAGE': lightvolt_avg,
                    'Radar': radar_avg
                }
                #self.thingspeak_client.update_environment_channel(environment_dict)
                print(environment_dict)
                radar_data = []
                light_raw_data = []
                light_volt_data = []
                last_update_time = current_time

ambient_readings(sensor_client)