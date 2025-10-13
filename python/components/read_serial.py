# Serial reading logic is now split into:
# - serial_setup.py (serial port setup and signal handling)
# - csv_writer.py (CSV writing)
# - plotting.py (plot data management)

from .serial_setup import setup_serial, handle_exit
from .csv_writer import save_csv
from .plotting import add_plot_data