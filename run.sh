#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

arduino-cli compile --fqbn arduino:avr:uno "$SCRIPT_DIR"/arduino/temp-sensor
arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:uno --input-dir "$SCRIPT_DIR"/arduino/temp-sensor
sleep 5
streamlit run "$SCRIPT_DIR"/python/main.py