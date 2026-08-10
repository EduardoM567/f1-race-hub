#!/bin/bash
#Owner: Branden Brison (bb449)
#Pre-promotion backup script - backs up DB and config files before applying changes
set -e

DB_NAME="bb449"
DB_USER="bb449"
PROJECT_DIR="/home/bb449/f1-migrations/alembic/versions"
BACKUP_DIR="/home/bb449/backups"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)

# Create backup dir if it doesn't exist
mkdir -p "$BACKUP_DIR"

#Get Release ID from alembic
cd "$PROJECT_DIR"
source "${PROJECT_DIR}/.venv/bin/activate"
RELEASE_ID=$(alembic heads | awk '{print $1}')

if [ -z "$RELEASE_ID" ]; then
    echo "Failed to obtain Release ID"
    exit 1
fi

echo "Release ID: $RELEASE_ID"
echo "Backup directory: $BACKUP_DIR"

#Database Backup
mysqldump -u "$DB_USER" -p "$DB_NAME" > "$BACKUP_DIR/dbbackup${RELEASE_ID}${TIMESTAMP}.sql"
echo "DB backup completed: dbbackup${RELEASE_ID}${TIMESTAMP}.sql"

#File/Config Backup
tar -czvf "$BACKUP_DIR/configbackup${RELEASE_ID}${TIMESTAMP}.tar.gz" -C "$PROJECT_DIR" .
echo "File backup completed: configbackup${RELEASE_ID}${TIMESTAMP}.tar.gz"

echo "All backups done for release $RELEASE_ID"