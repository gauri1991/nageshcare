#!/bin/bash
# Database Backup Script for NageshCare
# This script creates a timestamped backup of the SQLite database

# Get the script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
DB_FILE="$PROJECT_ROOT/db.sqlite3"
BACKUP_DIR="$PROJECT_ROOT/backups"

# Create backups directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Create timestamp
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/db_backup_$TIMESTAMP.sqlite3"

# Check if database exists
if [ ! -f "$DB_FILE" ]; then
    echo "❌ Error: Database file not found at $DB_FILE"
    exit 1
fi

# Create backup
echo "Creating database backup..."
cp "$DB_FILE" "$BACKUP_FILE"

# Check if backup was successful
if [ $? -eq 0 ]; then
    echo "✓ Database backed up successfully!"
    echo "  Location: $BACKUP_FILE"
    echo "  Size: $(du -h "$BACKUP_FILE" | cut -f1)"

    # Keep only last 10 backups
    echo ""
    echo "Cleaning old backups (keeping last 10)..."
    cd "$BACKUP_DIR"
    ls -t db_backup_*.sqlite3 | tail -n +11 | xargs -r rm
    echo "  Current backups: $(ls -1 db_backup_*.sqlite3 | wc -l)"
else
    echo "❌ Error: Backup failed!"
    exit 1
fi

exit 0
