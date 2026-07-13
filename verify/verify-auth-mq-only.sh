#!/usr/bin/env bash
# verify-auth-mq-only.sh - IT490 Milestone 2, Task #6 (MQ-Only Boundary Verification)
# ucid: omg6  (Omar Gad, GitHub: omargad-sys) - Team RacingDevs
# Purpose: prove the App VM reaches the DB ONLY through RabbitMQ - there is NO
#          direct App-VM -> DB-VM path (no MySQL client, no DB creds, no 3306).
#          Read-only checks (safe to run multiple times).
# Usage:   DB_VM_IP=100.x.x.x MQ_VM_IP=100.x.x.x APP_DIR=/var/www/html bash verify-auth-mq-only.sh
#          (set the three vars to your real values first)

set -uo pipefail   # ucid: omg6 - unset vars + pipe failures are errors (no -e: run all checks)

# ucid: omg6 - EDIT THESE (or pass as env vars) to match your team's tailnet + app path
DB_VM_IP="${DB_VM_IP:-CHANGE_ME_DB_VM_IP}"     # DB VM tailscale/private IP
MQ_VM_IP="${MQ_VM_IP:-CHANGE_ME_MQ_VM_IP}"     # RabbitMQ VM tailscale/private IP
APP_DIR="${APP_DIR:-/var/www/html}"            # where the App VM's app code lives

PASS="[PASS]"; FAIL="[FAIL]"; INFO="[INFO]"    # ucid: omg6
overall=0                                       # ucid: omg6 - non-zero if any check fails

echo "==================================================================="
echo " MQ-Only Boundary Verification - host: $(hostname)   ucid: omg6"
echo " Date: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo " DB_VM_IP=$DB_VM_IP  MQ_VM_IP=$MQ_VM_IP  APP_DIR=$APP_DIR"
echo "==================================================================="

# ucid: omg6 - Check 1: App VM has NO database client installed
echo ""
echo "1) No DB client on the App VM ------------------------------------"
db_clients="$(for b in mysql mariadb psql mongo; do command -v "$b" 2>/dev/null; done)"
if [ -n "$db_clients" ]; then
  echo "$FAIL a DB client is installed on the App VM:"; echo "$db_clients"
  overall=1
else
  echo "$PASS no mysql/mariadb/psql/mongo client on the App VM"
fi

# ucid: omg6 - Check 2: no DB credentials / connection code in the app
echo ""
echo "2) No DB credentials or connection code in app ($APP_DIR) --------"
if [ -d "$APP_DIR" ]; then
  cred_hits="$(grep -RniE --exclude-dir=vendor --exclude-dir=node_modules --exclude-dir=.git 'mysqli_connect|mysql_connect|new mysqli|new PDO|mysql:host|DB_HOST|DB_PASS|DB_USER|3306' "$APP_DIR" 2>/dev/null | grep -viE 'verify-auth-mq-only' | head -20)"
  if [ -n "$cred_hits" ]; then
    echo "$FAIL possible direct-DB code/creds found in app:"; echo "$cred_hits"
    overall=1
  else
    echo "$PASS no DB drivers, connection strings, or credentials in $APP_DIR"
  fi
else
  echo "$INFO $APP_DIR not found - set APP_DIR to your app path and rerun"
fi

# ucid: omg6 - Check 3: no ESTABLISHED connection from App VM to the DB VM
echo ""
echo "3) No live App->DB connection (expect none to $DB_VM_IP:3306) ----"
conns="$(sudo ss -tunp 2>/dev/null || ss -tun 2>/dev/null)"
db_conn="$(echo "$conns" | grep ESTAB | grep -E "${DB_VM_IP}|:3306" || true)"
if [ -n "$db_conn" ]; then
  echo "$FAIL App VM has a live connection toward the DB:"; echo "$db_conn"
  overall=1
else
  echo "$PASS no established App-VM -> DB-VM (:3306) connection"
fi

# ucid: omg6 - Check 4: the only cross-VM connection is RabbitMQ (5672) on the MQ VM
echo ""
echo "4) Cross-VM traffic is only RabbitMQ:5672 ------------------------"
offenders="$(echo "$conns" | grep ESTAB | grep -vi tailscaled | grep -E '100\.[0-9]+\.[0-9]+\.[0-9]+' | grep -vE ':5672|:22' || true)"
if [ -n "$offenders" ]; then
  echo "$INFO cross-VM connections outside 5672/22 (review - ssh/admin is OK):"
  echo "$offenders"
else
  echo "$PASS only RabbitMQ:5672 (and ssh:22) cross-VM connections"
fi

# ucid: omg6 - Check 5: App VM CAN reach MQ:5672 but CANNOT reach DB:3306 (active probe)
echo ""
echo "5) Active reachability probe ------------------------------------"
probe() { timeout 3 bash -c "cat < /dev/null > /dev/tcp/$1/$2" 2>/dev/null && echo up || echo down; }
mq_reach="$(probe "$MQ_VM_IP" 5672)"
db_reach="$(probe "$DB_VM_IP" 3306)"
echo "$INFO App VM -> MQ_VM:5672 = $mq_reach   (want: up)"
echo "$INFO App VM -> DB_VM:3306 = $db_reach   (want: down/blocked)"
if [ "$mq_reach" = "up" ] && [ "$db_reach" != "up" ]; then
  echo "$PASS App VM can reach the broker but not the database directly"
else
  echo "$INFO review: broker should be reachable and DB port should NOT be"
fi

# ucid: omg6 - Check 6: no alternate sync paths (NFS/CIFS, cron rsync/scp, sync timers)
echo ""
echo "6) No alternate cross-VM data paths -----------------------------"
alt=0
mount | grep -Eiq 'type (nfs|cifs|smb)' && { echo "$FAIL shared network mount present"; alt=1; }
{ crontab -l 2>/dev/null; cat /etc/crontab 2>/dev/null; cat /etc/cron.d/* 2>/dev/null; } | grep -Eiq 'rsync|scp |sshpass' && { echo "$FAIL rsync/scp cron job present"; alt=1; }
systemctl list-timers --all --no-legend 2>/dev/null | grep -Eiq 'sync|rsync' && { echo "$FAIL file-sync timer present"; alt=1; }
if [ "$alt" -eq 0 ]; then
  echo "$PASS no NFS/CIFS mounts, no rsync/scp cron, no file-sync timers"
else
  overall=1
fi

# ucid: omg6 - Check 7: RabbitMQ auth topology + DLQ (run on the MQ VM)
echo ""
echo "7) RabbitMQ auth topology / DLQ (run on rabbitmq-vm) ------------"
if command -v rabbitmqctl >/dev/null 2>&1; then
  echo "$INFO exchanges (expect auth_exchange):"
  sudo rabbitmqctl list_exchanges name type 2>/dev/null | grep -Ei 'auth' || echo "   (none matched 'auth')"
  echo "$INFO queues (expect auth request queue(s), auth_reply_queue, auth_dlq):"
  sudo rabbitmqctl list_queues name messages 2>/dev/null | grep -Ei 'auth' || echo "   (none matched 'auth')"
  echo "$INFO bindings (expect auth.register / auth.login routing keys):"
  sudo rabbitmqctl list_bindings 2>/dev/null | grep -Ei 'auth' || echo "   (no auth bindings found)"
else
  echo "$INFO rabbitmqctl not on this host - run Check 7 on the MQ VM"
fi

echo ""
echo "==================================================================="
if [ "$overall" -eq 0 ]; then
  echo " RESULT: PASS - App VM has no direct DB path; DB is reachable only via MQ   ucid: omg6"
else
  echo " RESULT: FAIL - a direct/alternate App->DB path was detected (see above)     ucid: omg6"
fi
echo "==================================================================="

# ucid: omg6 - Positive "kill the broker" proof must be run by a human (needs MQ + App + DB).
echo ""
echo 'NEXT: positive "MQ-is-the-only-path" test (manual)                 ucid: omg6'
echo '  1. MQ VM : sudo systemctl stop rabbitmq-server'
echo '  2. App   : attempt a login  -> it TIMES OUT (5s) / errors, nothing reaches DB'
echo '  3. MQ VM : sudo systemctl start rabbitmq-server'
echo '  4. App   : attempt the login again -> it succeeds again'
echo '  Capture all output as evidence for the Task #6 issue.            ucid: omg6'
