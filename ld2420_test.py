import serial
import time

# Configure the serial port
ser = serial.Serial(
    port='/dev/serial0',  # UART port on Raspberry Pi
    baudrate=115200,      # LD2420 default baud rate
    timeout=1             # 1 second timeout for reading
)

print("LD2420 Test: Listening for data...")

# try:
#     while True:
#         if ser.in_waiting > 0:
#             data = ser.read(ser.in_waiting).hex()  # Read all available data
#             print("Received Data:", data)

# except KeyboardInterrupt:
#     print("Exiting...")
#     ser.close()


# while True:
#     raw_data = ser.read(ser.in_waiting or 1).hex()  # Read available data
#     if raw_data:
#         print(raw_data)


# def parse_sensor_data(buffer):
#     # Convert buffer to ASCII
#     ascii_data = buffer.decode('utf-8', errors='ignore')
    
#     # Split by the delimiter (\r\n)
#     packets = ascii_data.split("\r\n")
#     print(f"Packets: {packets}")
#     results = []

#     for i, packet in enumerate(packets):
#         if "ON" in packet and "Range" in packet:
#             try:
#                 # Extract the measurement value
#                 value = int(packet.split("Range")[1].strip())
#                 results.append(value)
#             except ValueError:
#                 continue  # Ignore invalid data
#         elif "Range" in packet:
#             try:
#                 # Extract the measurement value
#                 value = int(packet.split("Range")[1].strip())
#                 results.append(value)
#             except ValueError:
#                 continue  # Ignore invalid data
#         elif "ON" in packet:
#             results.append("ON")
#         elif "OFF" in packet:
#             results.append("OFF")
#     return results, packets[-1]  # Return results and the last partial packet

# # Initialize an empty buffer
# buffer = b""

# while True:
#     # Read available data from the serial port
#     raw_data = ser.read(ser.in_waiting or 1)
#     if raw_data:
#         buffer += raw_data  # Append new data to the buffer

#         # Parse the buffer
#         parsed_data, remaining_buffer = parse_sensor_data(buffer)

#         # Process valid parsed data
#         if parsed_data:
#             print("Parsed Values:", parsed_data)

#         # Retain the remaining partial packet for the next loop
#         buffer = remaining_buffer.encode('utf-8', errors='ignore')


def parse_sensor_data(buffer):
    # Convert buffer to ASCII
    ascii_data = buffer.decode('utf-8', errors='ignore')
    
    # Split by the delimiter (\r\n)
    packets = ascii_data.split("\r\n")
    #print(f"Packets: {packets}")
    results = []

    for i, packet in enumerate(packets):
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

# Initialize an empty buffer
buffer = b""

while True:
    # Read available data from the serial port
    raw_data = ser.read(ser.in_waiting or 1)
    if raw_data:
        buffer += raw_data  # Append new data to the buffer
        #print(f"Buffer: {buffer}")

        if b"\r\n" in buffer:
            #print("Parsing")
            # Parse the buffer
            parsed_data, remaining_buffer = parse_sensor_data(buffer)
            # Retain the remaining partial packet for the next loop
            buffer = remaining_buffer.encode('utf-8', errors='ignore')

            # Process valid parsed data
            if parsed_data:
                print("Parsed Values:", parsed_data)

    time.sleep(1)

        
"""
def movement_readings(self):
        # Configure the serial port
        ser = serial.Serial(
            port='/dev/serial0',  # UART port on Raspberry Pi
            baudrate=115200,      # LD2420 default baud rate
            timeout=1             # 1 second timeout for reading
        )

        print("LD2420 Test: Listening for data...")

        # Initialize an empty buffer
        buffer = b""
        last_update_time = datetime.now().timestamp()
        update_interval = 5
        data = []

        while True:
            current_time = datetime.now().timestamp()
            # Read available data from the serial port
            raw_data = ser.read(ser.in_waiting or 1)
            if raw_data:
                buffer += raw_data  # Append new data to the buffer
                #print(f"Buffer: {buffer}")

                if b"\r\n" in buffer:
                    #print("Parsing")
                    # Parse the buffer
                    parsed_data, remaining_buffer = self.parse_sensor_data(buffer)
                    # Retain the remaining partial packet for the next loop
                    buffer = remaining_buffer.encode('utf-8', errors='ignore')

                    # Process valid parsed data
                    if parsed_data:
                        print("Parsed Values:", parsed_data)
                        if isinstance(parsed_data[0], str) == False:
                            print("appended")
                            data.append(int(parsed_data[0]))

            if current_time - last_update_time >= update_interval:
                if data:
                    average = st.mean(data)
                    print(f"-----------------------AVERAGE: {average}")
                    environment_dict = {
                        'Light': 44,
                        'Radar': average
                    }
                    self.thingspeak_client.update_environment_channel(environment_dict)
                    data = []
                    last_update_time = current_time
                    """



