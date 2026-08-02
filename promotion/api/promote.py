#!/usr/bin/env python3
# API VM Promotion Tool
# Owner: Eduardo (em567)
# Promotes API files from development -> QA -> production via SSH.
# Enforces: dev->QA and QA->prod only, blocks dev->prod directly.
# Creates a backup on the target before promoting.
# Logs source lane, target lane, target file(s), release ID, backup path, result, timestamp.
# Supports single-file promotion and bulk release promotion via a release manifest.

import json
import subprocess
import sys
import os
from datetime import datetime

INVENTORY_FILE = os.path.join(os.path.dirname(__file__), 'inventory.json')
LOG_FILE = os.path.join(os.path.dirname(__file__), 'promotion.log')

VALID_PATHS = {
    ('dev', 'qa'),
    ('qa', 'prod')
}

def load_inventory():
    with open(INVENTORY_FILE) as f:
        return json.load(f)['api']

def log_event(entry):
    with open(LOG_FILE, 'a') as f:
        f.write(json.dumps(entry) + '\n')

def backup_target(inventory, target_lane, filename, release_id):
    lane = inventory[target_lane]
    backup_name = f"{filename}.{release_id}.bak"

    subprocess.run(['ssh', lane['host'], f"mkdir -p {lane['backup_path']}"], check=True)

    check = subprocess.run(['ssh', lane['host'], f"test -f {lane['app_path']}{filename}"])
    if check.returncode != 0:
        return None  # nothing to back up yet, first-time promotion

    result = subprocess.run(['ssh', lane['host'],
                              f"cp {lane['app_path']}{filename} {lane['backup_path']}{backup_name}"])
    if result.returncode != 0:
        raise RuntimeError(f"Backup failed for {filename} on {target_lane}")

    return f"{lane['backup_path']}{backup_name}"

def promote_file(inventory, source_lane, target_lane, filename, release_id):
    if (source_lane, target_lane) not in VALID_PATHS:
        raise ValueError(f"Invalid promotion path: {source_lane} -> {target_lane}. Only dev->qa and qa->prod are allowed.")

    src = inventory[source_lane]
    dst = inventory[target_lane]

    src_path = f"{src['host']}:{src['app_path']}{filename}"
    dst_path = f"{dst['host']}:{dst['app_path']}{filename}"

    backup_path = backup_target(inventory, target_lane, filename, release_id)

    result = subprocess.run(['scp', src_path, dst_path])
    success = result.returncode == 0

    checksum = None
    if success:
        checksum_result = subprocess.run(
            ['ssh', dst['host'], f"sha256sum {dst['app_path']}{filename}"],
            capture_output=True, text=True
        )
        checksum = checksum_result.stdout.split()[0] if checksum_result.returncode == 0 else None

    entry = {
        'timestamp': datetime.utcnow().isoformat(),
        'release_id': release_id,
        'source_lane': source_lane,
        'target_lane': target_lane,
        'target_role': 'api',
        'file': filename,
        'backup_path': backup_path,
        'checksum': checksum,
        'result': 'success' if success else 'failure'
    }
    log_event(entry)

    if not success:
        raise RuntimeError(f"Promotion failed for {filename}: {source_lane} -> {target_lane}")

    print(f"[{entry['result'].upper()}] {filename}: {source_lane} -> {target_lane} (release {release_id})")
    return entry

def promote_bulk(inventory, source_lane, target_lane, manifest_path):
    with open(manifest_path) as f:
        manifest = json.load(f)

    release_id = manifest['release_id']
    files = manifest['files']

    results = []
    for filename in files:
        entry = promote_file(inventory, source_lane, target_lane, filename, release_id)
        results.append(entry)

    print(f"\n[BULK COMPLETE] release {release_id}: {len(results)} files promoted {source_lane} -> {target_lane}")
    return results

def main():
    if len(sys.argv) < 4:
        print("Usage:")
        print("  Single file:  python3 promote.py <source_lane> <target_lane> <filename> [release_id]")
        print("  Bulk release: python3 promote.py <source_lane> <target_lane> --manifest <manifest_path>")
        sys.exit(1)

    inventory = load_inventory()
    source_lane = sys.argv[1]
    target_lane = sys.argv[2]

    if sys.argv[3] == '--manifest':
        if len(sys.argv) < 5:
            print("Missing manifest path")
            sys.exit(1)
        manifest_path = sys.argv[4]
        try:
            promote_bulk(inventory, source_lane, target_lane, manifest_path)
        except ValueError as e:
            print(f"[REJECTED] {e}")
            sys.exit(1)
        except RuntimeError as e:
            print(f"[ERROR] {e}")
            sys.exit(1)
        return

    filename = sys.argv[3]
    release_id = sys.argv[4] if len(sys.argv) > 4 else datetime.utcnow().strftime('%Y%m%d-%H%M%S')

    try:
        promote_file(inventory, source_lane, target_lane, filename, release_id)
    except ValueError as e:
        entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'release_id': release_id,
            'source_lane': source_lane,
            'target_lane': target_lane,
            'target_role': 'api',
            'file': filename,
            'backup_path': None,
            'checksum': None,
            'result': 'rejected',
            'reason': str(e)
        }
        log_event(entry)
        print(f"[REJECTED] {e}")
        sys.exit(1)
    except RuntimeError as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()