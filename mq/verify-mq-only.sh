#!/usr/bin/env bash
# verify-mq-only.sh - IT490 Milestone 1, Issue #16 (MQ-Only Synchronization Verification)
# ucid: omg6  (Omar Gad, GitHub: omargad-sys)
# Purpose: prove this VM does NOT sync logs through any non-MQ path.
#          Read-only checks (safe to run multiple times). Run on each role VM.
# Usage:   bash verify-mq-only.sh

set -uo pipefail   # ucid: omg6 - unset vars and pipe failures are errors (no -e: run all checks)

PASS="[PASS]"      # ucid: omg6 - check found no forbidden sync path
FAIL="[FAIL]"      # ucid: omg6 - check found a forbidden sync path
INFO="[INFO]"      # ucid: omg6 - informational only
overall=0          # ucid: omg6 - non-zero if any check fails

echo "==================================================================="
echo " MQ-Only Verification (negative checks) - host: $(hostname)  ucid: omg6"
echo " Date: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "==================================================================="

# ucid: omg6 - Check 1: no NFS/CIFS/shared network folders mounted
echo ""
echo "1) Shared folders (NFS/CIFS) -------------------------------------"
if mount | grep -Eiq 'type (nfs|cifs|smb)'; then
  echo "$FAIL shared network mount found:"; mount | grep -Ei 'type (nfs|cifs|smb)'
  overall=1
else
  echo "$PASS no NFS/CIFS/SMB mounts (no shared-folder log path)"
fi

# ucid: omg6 - Check 2: no rsync/scp jobs in user or system cron
echo ""
echo "2) Cron jobs (rsync/scp) ----------------------------------------"
cron_hits="$( { crontab -l 2>/dev/null; cat /etc/crontab 2>/dev/null; cat /etc/cron.d/* 2>/dev/null; } | grep -Ei 'rsync|scp |sshpass' || true )"
if [ -n "$cron_hits" ]; then
  echo "$FAIL cron entry referencing a copy tool:"; echo "$cron_hits"
  overall=1
else
  echo "$PASS no rsync/scp/sshpass cron jobs"
fi

# ucid: omg6 - Check 3: no systemd timers that could sync files
echo ""
echo "3) systemd timers -----------------------------------------------"
timer_hits="$(systemctl list-timers --all --no-legend 2>/dev/null | grep -Ei 'sync|rsync|log.*copy' || true)"
if [ -n "$timer_hits" ]; then
  echo "$FAIL suspicious timer(s):"; echo "$timer_hits"
  overall=1
else
  echo "$PASS no file-sync systemd timers"
fi

# ucid: omg6 - Check 4: established cross-VM TCP traffic should only be RabbitMQ (5672)
echo ""
echo "4) Cross-VM connections (expect only 5672) ----------------------"
conns="$(sudo ss -tunp 2>/dev/null || ss -tun 2>/dev/null)"
offenders="$(echo "$conns" | grep ESTAB | grep -E '100\.' | grep -vE ':5672' || true)"
if [ -n "$offenders" ]; then
  echo "$INFO established non-5672 connections to peers (review these):"
  echo "$offenders"
  echo "$INFO confirm none of these carry log data (ssh/admin is OK)."
else
  echo "$PASS no established cross-VM connections outside RabbitMQ:5672"
fi

# ucid: omg6 - Check 5: no scripts in common dirs that ship logs via scp/rsync/curl
echo ""
echo "5) Log-shipping scripts -----------------------------------------"
script_hits="$(grep -RniE --include='*.sh' --include='*.py' 'rsync .*log|scp .*log|curl .*log|sshpass' /home /opt /usr/local 2>/dev/null | grep -vi 'verify-mq-only' | head -20 || true)"
if [ -n "$script_hits" ]; then
  echo "$FAIL script(s) appear to ship logs outside MQ:"; echo "$script_hits"
  overall=1
else
  echo "$PASS no scripts shipping logs via scp/rsync/curl"
fi

echo ""
echo "==================================================================="
if [ "$overall" -eq 0 ]; then
  echo " RESULT: PASS - no non-MQ log sync path found on $(hostname)   ucid: omg6"
else
  echo " RESULT: FAIL - a non-MQ sync path was detected (see above)    ucid: omg6"
fi
echo "==================================================================="

# ucid: omg6 - Positive test must be run by a human across two VMs + the broker.
echo ""
echo 'NEXT: positive "MQ-is-the-only-path" test (manual, needs broker + 2 VMs)  ucid: omg6'
echo '  1. Listener VM : tail -f <mirrored-log-file>'
echo '  2. Publisher VM: emit one test log event (the #6 logging interface)'
echo '                   -> confirm it appears in the listener log (timestamp/content)'
echo '  3. rabbitmq-vm : sudo systemctl stop rabbitmq-server'
echo '     Publisher VM: emit another event -> confirm it does NOT appear (sync stopped)'
echo '  4. rabbitmq-vm : sudo systemctl start rabbitmq-server'
echo '     Publisher VM: emit again -> confirm it appears (sync resumes)'
echo '  Capture all output as evidence for issue #16.    ucid: omg6'
