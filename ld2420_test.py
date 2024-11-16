import serial

# Configure the serial port
ser = serial.Serial(
    port='/dev/serial0',  # UART port on Raspberry Pi
    baudrate=115200,      # LD2420 default baud rate
    timeout=1             # 1 second timeout for reading
)

print("LD2420 Test: Listening for data...")

def parse_sensor_data(raw_data):
    # Convert raw data to ASCII
    ascii_data = raw_data.decode('utf-8', errors='ignore')
    
    # Split by the delimiter (\r\n)
    packets = ascii_data.split("\r\n")
    results = []

    for packet in packets:
        if "ON" in packet and "Range" in packet:
            try:
                # Extract the measurement value
                value = int(packet.split("Range")[1].strip())
                results.append(value)
            except ValueError:
                continue  # Ignore invalid data
    return results

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


while True:
    raw_data = ser.read(ser.in_waiting or 1)  # Read available data
    if raw_data:
        parsed_data = parse_sensor_data(raw_data)
        if parsed_data:
            print("Parsed Values:", parsed_data)


