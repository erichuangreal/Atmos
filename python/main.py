import streamlit as st
import subprocess
import os
import signal
import pandas as pd
import matplotlib.pyplot as plt
import time
import glob
from streamlit_autorefresh import st_autorefresh

from components.download_csv import download_button

# Refresh
st_autorefresh(interval=5000, limit=None, key="auto-refresh")

st.title("Temperature and Humidity Logger")

# Global state to store the process
if "proc" not in st.session_state:
    st.session_state.proc = None

script_path = os.path.abspath("python/components/read_serial.py")

# Start button
if st.button("Start Collecting"):
    if st.session_state.proc is None:
        st.session_state.proc = subprocess.Popen(["python3", script_path])
        st.success("Started collecting data.")
    else:
        st.warning("Already collecting!")

if st.button("Stop Collecting"):
    if st.session_state.proc:
        # Create stop flag
        with open("/tmp/stop_dht_logger.flag", "w") as f:
            f.write("stop")

        # Wait for child to exit cleanly
        st.session_state.proc.wait()
        st.session_state.proc.terminate()
        st.session_state.proc = None
        st.success("Stopped data collection.")
    else:
        st.warning("No process to stop.")

# Wait for file to be flushed
time.sleep(1)

# Determine the base directory
DIREC = os.getcwd()  # This gives you the directory from which Streamlit is running
st.write("Running in:", DIREC)  # Optional debug info

# Build the full path to the CSV directory
LOG_DIR = os.path.join(DIREC, "csv_files")

# Make sure it exists
if not os.path.exists(LOG_DIR):
    st.warning(f"CSV log directory not found: {LOG_DIR}")
else:
    # Search for log CSV files
    csv_files = sorted(glob.glob(os.path.join(LOG_DIR, "log_*.csv")), reverse=True)
    st.write("Found CSVs:", csv_files)
    
    if csv_files:
        latest_csv = csv_files[0]
        try:
            df = pd.read_csv(latest_csv)
            if not df.empty:
                st.subheader("Sensor Data")
                fig, ax = plt.subplots()
                ax.plot(df["short_timestamp"], df["temperature"], label="Temp (°C)")
                ax.plot(df["short_timestamp"], df["humidity"], label="Humidity (%)")
                ax.legend()
                ax.set_xlabel("Time")
                st.pyplot(fig)
                
                download_button(latest_csv)
            else:
                st.info("CSV exists but no data yet.")
        except Exception as e:
            st.error(f"Failed to load CSV: {e}")
    else:
        st.info("No CSV file yet. Press 'Start Collecting'.")