#!/bin/bash

# CONFIG DIRECTORIES
SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"  # project root
BACKUP_DIR="$SRC_DIR/logs"
TIMESTAMP=$(date +'%Y-%m-%d_%H-%M-%S')
DEST="$BACKUP_DIR/backup_$TIMESTAMP.tar.gz"

# Create the backup
tar -czf "$DEST" -C "$SRC_DIR" .

echo "Backup saved to: $DEST"