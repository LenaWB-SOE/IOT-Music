import serial

# Configure the serial port
ser = serial.Serial(
    port='/dev/serial0',  # UART port on Raspberry Pi
    baudrate=115200,      # LD2420 default baud rate
    timeout=1             # 1 second timeout for reading
)

print("LD2420 Test: Listening for data...")

try:
    while True:
        if ser.in_waiting > 0:
            data = ser.read(ser.in_waiting).hex()  # Read all available data
            print("Received Data:", data)

except KeyboardInterrupt:
    print("Exiting...")
    ser.close()
