import serial
import pandas as pd
from datetime import datetime
import os

STOP_FILE = "/tmp/stop_dht_logger.flag"

# Serial port of the arduino
SERIAL_PORT = '/dev/ttyACM0'
BAUD_RATE = 9600
CSV_FILE = 'dht11_log.csv'

data = []

LOG_DIR = '/home/eric/temp-logger/csv_files'

# Generate unique timestamped filename
timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
CSV_FILE = f'{LOG_DIR}/log_{timestamp}.csv'

# Starts reading input
print("Listening to serial... Press Ctrl+C to stop.")

temp_plot = []
hum_plot = []
short_timestamp_plot = []
stop = False

if os.path.exists(STOP_FILE):
    os.remove(STOP_FILE)

ser = None
         
if __name__ == "__main__":    
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        while not os.path.exists(STOP_FILE):
            line = ser.readline().decode().strip()
            if not line:
                continue

            parts = line.split(',')

            if len(parts) == 2:
                temp = parts[0].strip()
                hum = parts[1].strip()
                timestamp = datetime.now().isoformat()
                short_timestamp = datetime.now().strftime("%H:%M:%S")

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
        df = pd.DataFrame(data, columns=["timestamp", "short_timestamp", "temperature", "humidity"])
        df.to_csv(CSV_FILE, index=False)
        print(f"Data saved to {CSV_FILE}")
        ser.close()
        if os.path.exists(STOP_FILE):
            os.remove(STOP_FILE)
        if ser and ser.is_open:
            ser.close()