import serial
import pandas as pd
from datetime import datetime

# Serial port of the arduino
SERIAL_PORT = '/dev/ttyACM0'
BAUD_RATE = 9600
CSV_FILE = 'dht11_log.csv'

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
data = []

LOG_DIR = '/home/eric/temp-logger/csv_files'

# Generate unique timestamped filename
timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
CSV_FILE = f'{LOG_DIR}/log_{timestamp}.csv'

# Starts reading input
print("Listening to serial... Press Ctrl+C to stop.")

try:
    while True:
        line = ser.readline().decode().strip()
        if not line:
            continue

        parts = line.split(',')

        if len(parts) == 2:
            temp = parts[0].strip()
            hum = parts[1].strip()
            timestamp = datetime.now().isoformat()

            # Handle missing/error values
            if temp == "" or hum == "" or "ERROR" in hum:
                continue;
            else :
                print(f"{timestamp}  Temp: {temp}°C  Hum: {hum}%")
                data.append([timestamp, temp, hum])
except KeyboardInterrupt:
    print("\nSaving CSV and exiting...")
    df = pd.DataFrame(data, columns=["timestamp", "temperature", "humidity"])
    df.to_csv(CSV_FILE, index=False)
    print(f"Data saved to {CSV_FILE}")
    ser.close()