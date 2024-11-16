import serial

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


def parse_sensor_data(buffer, context):
    # Decode buffer to ASCII
    ascii_data = buffer.decode('utf-8', errors='ignore')
    
    # Split the data by delimiter (\r\n)
    packets = ascii_data.split("\r\n")
    results = []

    for packet in packets:
        # Carry over context from previous partial packet
        packet = context + packet
        context = ""  # Clear context after using it

        # Process packets that include "ON" and "Range"
        if "ON" in packet and "Range" in packet:
            try:
                # Extract the range value
                value = int(packet.split("Range")[1].strip())
                results.append(value)
            except ValueError:
                continue  # Ignore invalid or malformed data
        elif "ON" in packet or "Range" in packet:
            # If only part of the data is present, store it in context
            context = packet

    return results, context  # Return parsed results and remaining context

# Initialize an empty buffer and context
buffer = b""
context = ""

while True:
    # Read available data from the serial port
    raw_data = ser.read(ser.in_waiting or 1)
    if raw_data:
        buffer += raw_data  # Append new data to the buffer
        print(buffer)

        # Parse the buffer with context tracking
        parsed_data, context = parse_sensor_data(buffer, context)

        # Process valid parsed data
        if parsed_data:
            print("Parsed Values:", parsed_data)

        # Clear buffer after parsing
        buffer = b""




