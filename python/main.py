import streamlit as st
import subprocess
import os
import signal
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import AutoMinorLocator, MaxNLocator
import time
import glob
from streamlit_autorefresh import st_autorefresh

from components.download_csv import download_button
from components.strip_labels import label

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
    if csv_files:
        csv_labels, label_to_file = label(csv_files)
        selected_label = st.selectbox("Choose CSV to view:", csv_labels)
        selected_csv = label_to_file[selected_label]
        df = pd.read_csv(selected_csv)
        try:
            # Timestamp
            df["Timestamp"] = pd.to_datetime(df["Timestamp"])
            if not df.empty:
                st.subheader("Sensor Data")
                fig, ax = plt.subplots()
                ax.plot(df["Timestamp"], df["Temperature"], label="Temp (°C)")
                ax.plot(df["Timestamp"], df["Humidity"], label="Humidity (%)")
                # Format axis with fewer ticks
                ax.xaxis.set_major_locator(mdates.AutoDateLocator())
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
                fig.autofmt_xdate()
                ax.yaxis.set_major_locator(MaxNLocator(nbins=6))
                # Minor ticks
                ax.xaxis.set_minor_locator(mdates.AutoDateLocator())
                ax.tick_params(axis='x', which='minor', length=4, color='gray')
                ax.yaxis.set_minor_locator(AutoMinorLocator())
                ax.tick_params(axis='y', which='minor', length=4, color='gray')
                ax.legend()
                ax.set_xlabel("Time")
                st.pyplot(fig)
                st.caption(f"Last updated: {df['Timestamp'].iloc[-1].strftime('%Y-%m-%d %H:%M:%S')}")
                download_button(selected_csv)
            else:
                st.info("CSV exists but no data yet.")
        except Exception as e:
            st.error(f"Failed to load CSV: {e}")
    else:
        st.info("No CSV file yet. Press 'Start Collecting'.")