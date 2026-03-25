#!/bin/bash

# Simple PostgreSQL backup script for Widle Insure Database
# Useful for the 'Backup and recovery test' Week 8 task.

set -e

# Default to environment variables if set, otherwise use standard defaults
DB_USER=${POSTGRES_USER:-postgres}
DB_HOST=${POSTGRES_SERVER:-localhost}
DB_PORT=${POSTGRES_PORT:-5432}
DB_NAME=${POSTGRES_DB:-widle_insure}

# Output directory and filename
BACKUP_DIR="./backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/widle_backup_$TIMESTAMP.sql"

# Ensure backup directory exists
mkdir -p "$BACKUP_DIR"

echo "Starting backup of database '$DB_NAME' at $DB_HOST..."

# Execute pg_dump
# Note: PGPASSWORD should be set in the environment before running this script
pg_dump -U "$DB_USER" -h "$DB_HOST" -p "$DB_PORT" -F c -f "$BACKUP_FILE" "$DB_NAME"

echo "Backup successful! Saved to $BACKUP_FILE"
echo "To restore, run: pg_restore -U $DB_USER -h $DB_HOST -d $DB_NAME -1 $BACKUP_FILE"
