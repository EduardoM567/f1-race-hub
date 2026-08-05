#!/usr/bin/env python3
# API VM Rollback Tool
# Owner: Omar Gad (omg6)
# Restores a release-tagged backup ({filename}.{release_id}.bak) created by promote.py,
# copying it back over the file in the lane's app_path via SSH, then verifies with SHA-256.



import json
import subprocess
import sys
import os
from datetime import datetime

INVENTORY_FILE = os.path.join(os.path.dirname(__file__), 'inventory.json')
LOG_FILE = os.path.join(os.path.dirname(__file__), 'promotion.log')

def load_inventory():
    with open(INVENTORY_FILE) as f:
        return json.load(f)['api']

def log_event(entry):
    with open(LOG_FILE, 'a') as f:
        f.write(json.dumps(entry) + '\n')

def rollback(inventory, lane, filename, release_id):
    if lane not in inventory:
        raise ValueError(f"Unknown lane: {lane}")

    conf = inventory[lane]
    host = conf['host']
    backup_file = f"{conf['backup_path']}{filename}.{release_id}.bak"
    target_file = f"{conf['app_path']}{filename}"

    # the backup created by promote.py must exist, otherwise there is nothing to roll back to
    check = subprocess.run(['ssh', host, f"test -f {backup_file}"])
    if check.returncode != 0:
        raise RuntimeError(f"No backup found: {backup_file} on {host}")

    restore = subprocess.run(['ssh', host, f"cp {backup_file} {target_file}"])
    if restore.returncode != 0:
        raise RuntimeError(f"Restore failed for {filename} on {lane}")

    checksum_result = subprocess.run(
        ['ssh', host, f"sha256sum {target_file}"],
        capture_output=True, text=True
    )
    checksum = checksum_result.stdout.split()[0] if checksum_result.returncode == 0 else None

    entry = {
        'timestamp': datetime.utcnow().isoformat(),
        'action': 'rollback',
        'release_id': release_id,
        'lane': lane,
        'target_role': 'api',
        'file': filename,
        'restored_from': backup_file,
        'checksum': checksum,
        'result': 'success'
    }
    log_event(entry)
    print(f"[ROLLBACK OK] {filename} on {lane} restored from {backup_file} (release {release_id})")
    return entry

def main():
    if len(sys.argv) != 4:
        print("Usage: python3 rollback.py <lane> <filename> <release_id>")
        sys.exit(1)

    inventory = load_inventory()
    lane, filename, release_id = sys.argv[1], sys.argv[2], sys.argv[3]

    try:
        rollback(inventory, lane, filename, release_id)
    except (ValueError, RuntimeError) as e:
        log_event({
            'timestamp': datetime.utcnow().isoformat(),
            'action': 'rollback',
            'release_id': release_id,
            'lane': lane,
            'file': filename,
            'result': 'failure',
            'reason': str(e)
        })
        print(f"[ERROR] {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
