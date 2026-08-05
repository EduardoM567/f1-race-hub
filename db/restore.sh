#!/bin/bash
# Owner: Branden Brison (bb449)
# Restore script - restores DB and config files from a release-linked backup

set -e

DB_NAME="bb449"
DB_USER="bb449"
PROJECT_DIR="/home/bb449/f1-migrations/alembic/versions"
BACKUP_DIR="/home/bb449/backups"

# Load release ID and timestamp from config
source /home/bb449/restore_config.sh

if [ -z "$RELEASE_ID" ] || [ -z "$TIMESTAMP" ]; then
    echo "ERROR: RELEASE_ID and TIMESTAMP must be set in restore_config.sh"
    exit 1
fi

echo "Restoring release: $RELEASE_ID"
echo "Backup directory: $BACKUP_DIR"

# Verify backup files exist before doing anything
DBBACKUP="$BACKUP_DIR/dbbackup_${RELEASE_ID}_${TIMESTAMP}.sql"
CONFIGBACKUP="$BACKUP_DIR/configbackup_${RELEASE_ID}_${TIMESTAMP}.tar.gz"

if [ ! -f "$DBBACKUP" ]; then
    echo "ERROR: DB backup not found: $DBBACKUP"
    exit 1
fi

if [ ! -f "$CONFIGBACKUP" ]; then
    echo "ERROR: Config backup not found: $CONFIGBACKUP"
    exit 1
fi

# Restore database
echo "Restoring database..."
mysql -u "$DB_USER" -p "$DB_NAME" < "$DBBACKUP"
echo "Database restored successfully"

# Verify database state
echo "Verifying database..."
mysql -u "$DB_USER" -p "$DB_NAME" -e "SHOW TABLES;"
mysql -u "$DB_USER" -p "$DB_NAME" -e "SELECT * FROM alembic_version;"
mysql -u "$DB_USER" -p "$DB_NAME" -e "SELECT COUNT(*) as user_count FROM users;"
mysql -u "$DB_USER" -p "$DB_NAME" -e "SELECT COUNT(*) as fav_count FROM favorites;"

# Restore files/config
echo "Restoring files..."
tar -xzvf "$CONFIGBACKUP" -C "$PROJECT_DIR"
echo "Files restored successfully"

# Verify restored files
echo "Verifying restored files..."
ls -la "$PROJECT_DIR"/*.py 2>/dev/null || echo "No .py files found in project dir"

echo "Restore complete for release $RELEASE_ID"