from datetime import datetime
import os

def label(csv_files):
    """
    Create display-friendly names for CSV files.
    Returns a tuple: (csv_labels, label_to_file)
    """
    csv_labels = []
    label_to_file = {}
    for f in csv_files:
        basename = os.path.basename(f)
        try:
            timestamp_str = basename[4:-4]  # removes 'log_' and '.csv'
            dt = datetime.strptime(timestamp_str, "%Y-%m-%d_%H-%M-%S")
            dt = dt.replace(tzinfo=ZoneInfo("America/Toronto"))
            label = dt.strftime("%b %d, %H:%M")
        except Exception:
            label = basename  # fallback
        csv_labels.append(label)
        label_to_file[label] = f
    return csv_labels, label_to_file
