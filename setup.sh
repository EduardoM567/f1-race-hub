#!/usr/bin/env bash
# setup.sh - IT490-2026 Module 02 RabbitMQ sample automated setup
# ucid: omg6
# Purpose: install everything and prepare the RabbitMQ PHP sample so the
#          echo and ping/pong examples run immediately after this script.
# Idempotent: safe to run multiple times without errors (re-running just updates).

set -euo pipefail   # ucid: omg6 - stop on any error, unset variable, or failed pipe

# ucid: omg6 - configuration variables
REPO_URL="https://github.com/MattToegel/IT490-2026.git"   # ucid: omg6 - instructor's sample repo
APP_DIR="$HOME/IT490-2026"                                 # ucid: omg6 - where the code lands

# ucid: omg6 - refresh the package index so apt sees current versions
sudo apt-get update -y

# ucid: omg6 - base tools: git (clone), curl (composer dl), unzip, PPA helper
sudo apt-get install -y git curl unzip software-properties-common

# ucid: omg6 - install the RabbitMQ broker (the message server)
sudo apt-get install -y rabbitmq-server
sudo systemctl enable rabbitmq-server   # ucid: omg6 - auto-start on boot
sudo systemctl start  rabbitmq-server   # ucid: omg6 - make sure it is running now

# ucid: omg6 - the sample requires PHP >= 8.4, but Ubuntu 24.04 ships 8.3,
#              so add the ondrej/php PPA (add-apt-repository is idempotent).
sudo add-apt-repository -y ppa:ondrej/php
sudo apt-get update -y

# ucid: omg6 - install PHP 8.4 CLI plus the extensions php-amqplib needs
sudo apt-get install -y php8.4-cli php8.4-mbstring php8.4-bcmath php8.4-xml php8.4-curl

# ucid: omg6 - install Composer system-wide only if it is not already present
if ! command -v composer >/dev/null 2>&1; then
  curl -sS https://getcomposer.org/installer -o /tmp/composer-setup.php          # ucid: omg6 - download installer
  sudo php /tmp/composer-setup.php --install-dir=/usr/local/bin --filename=composer  # ucid: omg6 - install globally
  rm -f /tmp/composer-setup.php                                                  # ucid: omg6 - clean up installer
fi

# ucid: omg6 - clone the sample on first run, or fast-forward pull if it exists
if [ -d "$APP_DIR/.git" ]; then
  git -C "$APP_DIR" pull --ff-only   # ucid: omg6 - already cloned: just update it
else
  git clone "$REPO_URL" "$APP_DIR"   # ucid: omg6 - first run: clone the repo
fi

# ucid: omg6 - install PHP dependencies (php-amqplib) defined in composer.json
cd "$APP_DIR"
composer install --no-interaction --prefer-dist   # ucid: omg6 - pull vendor libs

# ucid: omg6 - final instructions for the two SSH sessions
echo ""
echo "Setup complete. Open TWO SSH sessions to this VM and run:"            # ucid: omg6
echo "  Terminal 1 (server): cd $APP_DIR && php RabbitMQServerSample.php"   # ucid: omg6
echo "  Terminal 2 (echo):   cd $APP_DIR && php RabbitMQClientSample.php echo \"hello from IT490\""  # ucid: omg6
echo "  Terminal 2 (ping):   cd $APP_DIR && php RabbitMQClientSample.php ping"  # ucid: omg6
