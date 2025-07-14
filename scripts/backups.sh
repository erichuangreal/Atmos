#!/bin/bash

# CONFIG DIRECTORIES
SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"  # project root
CSV_DIR="$SRC_DIR/csv_files"
BACKUP_DIR="$SRC_DIR/logs"
TIMESTAMP=$(date +'%Y-%m-%d_%H-%M-%S')
DEST="$BACKUP_DIR/csv_backup_$TIMESTAMP.tar.gz"

# Backup only CSV files modified in the last 1 day
find "$CSV_DIR" -type f -name '*.csv' -mtime -1 > /tmp/csv_files_to_backup.txt

# Only create backup if there are files to include
if [ -s /tmp/csv_files_to_backup.txt ]; then
  tar -czf "$DEST" -T /tmp/csv_files_to_backup.txt
  echo "CSV backup saved to: $DEST"
else
  echo "No new CSV files to back up."
fi

# Auto-delete backup archives older than 7 days
find "$BACKUP_DIR" -type f -name '*.tar.gz' -mtime +7 -exec rm {} \;