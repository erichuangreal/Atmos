import serial
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo
import os
import signal
import sys

STOP_FILE = "/tmp/stop_dht_logger.flag"

# Serial port of the arduino
SERIAL_PORT = '/dev/ttyACM0'
BAUD_RATE = 9600
CSV_FILE = 'dht11_log.csv'

data = []

LOG_DIR = '/home/eric/temp-logger/csv_files'

# Generate unique timestamped filename
file_timestamp = datetime.now(ZoneInfo("America/Toronto")).strftime("%Y-%m-%d_%H-%M-%S")
CSV_FILE = f'{LOG_DIR}/log_{file_timestamp}.csv'

# Starts reading input
print("Listening to serial... Press Ctrl+C to stop.")

temp_plot = []
hum_plot = []
short_timestamp_plot = []
stop = False

if os.path.exists(STOP_FILE):
    os.remove(STOP_FILE)

ser = None

# DELETE WHEN FINISHED (TEMP) - handles closed serial on a clean exit
def handle_exit(sig, frame):
    print("\nInterrupted. Cleaning up...")
    if ser and ser.is_open:
        ser.close()
        print("Serial closed.")
    sys.exit(0)

signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)

if __name__ == "__main__":    
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        while not os.path.exists(STOP_FILE):
            line = ser.readline().decode().strip()
            if not line:
                continue

            parts = line.split(',')
            
            if len(parts) == 2:
                now = datetime.now(ZoneInfo("America/Toronto"))
                temp = parts[0].strip()
                hum = parts[1].strip()
                timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
                short_timestamp = now.strftime("%H:%M:%S")

                # Handle missing/error values
                if temp == "" or hum == "" or "ERROR" in hum:
                    continue;
                else :
                    temp_plot.append(float(temp))
                    hum_plot.append(float(hum))
                    short_timestamp_plot.append(short_timestamp)
                    print(f"{timestamp}  Temp: {temp}°C  Hum: {hum}%")
                    data.append([timestamp, short_timestamp, temp, hum])
    except SerialException as e:
        print(f"Could not open serial port {SERIAL_PORT}: {e}")
    finally:
        print("\nSaving CSV and exiting...")
        df = pd.DataFrame(data, columns=["Timestamp", "Shortened Timestamp", "Temperature", "Humidity"])
        df.to_csv(CSV_FILE, index=False)
        print(f"Data saved to {CSV_FILE}")
        if os.path.exists(STOP_FILE):
            os.remove(STOP_FILE)
        if ser and ser.is_open:
            ser.close()