import serial
from serial import SerialException
from zoneinfo import ZoneInfo
import os
import signal
import sys
import time

SERIAL_PORT = '/dev/ttyACM0'
BAUD_RATE = 9600
STOP_FILE = "/tmp/stop_dht_logger.flag"
LOCK_FILE = "/tmp/read_serial.lock"
ser = None

def handle_exit(sig, frame):
    print("\nInterrupted. Cleaning up...")
    if ser and ser.is_open:
        ser.close()
        print("Serial closed.")
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)
    sys.exit(0)

signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)

def setup_serial():
    global ser
    if os.path.exists(STOP_FILE):
        os.remove(STOP_FILE)
    if os.path.exists(LOCK_FILE):
        print("Another instance is already running.")
        sys.exit(1)
    with open(LOCK_FILE, "w") as f:
        f.write(str(os.getpid()))
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        return ser
    except SerialException as e:
        print(f"Could not open serial port {SERIAL_PORT}: {e}")
        return None
