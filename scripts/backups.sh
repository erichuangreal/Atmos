#!/bin/bash

# CONFIG DIRECTORIES
SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"  # project root
CSV_DIR="$SRC_DIR/csv_files"
BACKUP_DIR="$SRC_DIR/logs"
TIMESTAMP=$(date +'%Y-%m-%d_%H-%M-%S')
DEST="$BACKUP_DIR/csv_backup_$TIMESTAMP.tar.gz"

# Create the backup
tar -czf "$DEST" -C "$CSV_DIR" .

echo "✅ CSV backup saved to: $DEST"