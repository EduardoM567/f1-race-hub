# F1 Race Hub

A distributed web application built for NJIT IT490 that displays real Formula 1 data including race schedules, driver standings, race results, and a live news feed. Built with a microservices architecture across 12 Linux VMs communicating exclusively through RabbitMQ.

## Architecture

- **App VM** — PHP frontend served via Apache
- **API VM** — Python consumers fetching from OpenF1 REST API
- **DB VM** — MySQL database with Python consumers handling auth and favorites
- **MQ VM** — RabbitMQ message broker routing all inter-service communication

## Features

- User registration and login with bcrypt password hashing
- F1 race schedule, driver standings, and driver detail pages
- Race results page with finishing positions and points
- F1 news feed from the official Formula 1 RSS feed
- Save, view, and remove favorite drivers and races
- User profile management (update username, email, password)
- Admin dashboard for managing users, roles, and account status
- Centralized logging — all production events routed through RabbitMQ to a persistent log file
- SSH-based deployment pipeline enforcing dev→QA→production promotion with automated backups and SHA-256 verification

## Technologies

- **Backend:** Python, pika (RabbitMQ), MySQL Connector
- **Frontend:** PHP, PhpAmqpLib
- **Message Broker:** RabbitMQ with direct exchanges, dead letter queues
- **Database:** MySQL
- **Infrastructure:** Ubuntu Linux, Multipass, Tailscale VPN, SSH
- **API:** OpenF1 REST API (free tier, 2025 historic data)
- **Deployment:** Custom SSH-based promotion tool with inventory config

## My Contributions

- Designed and implemented the RabbitMQ message contract and queue topology used by all services
- Built the F1 data consumer handling schedule, standings, driver, race results, and news feed requests
- Integrated centralized logging into the production API consumer
- Built the admin dashboard backend PHP pages and admin queue setup
- Designed and built the SSH-based promotion tool supporting single-file and bulk release promotion
- Set up all three API lane VMs (dev, QA, production) with Tailscale networking and SSH key auth
- Wrote CSS styling for the entire application

## Deployment Pipeline

Files are promoted through lanes using a custom SSH-based tool:

```bash
python3 promote.py dev qa f1_consumer.py REL-001
python3 promote.py qa prod --manifest release_manifest.json
```
Direct dev→production promotion is blocked. Each promotion creates a release-linked backup and verifies SHA-256 checksums before and after transfer.

## Team

Built by Racing Devs — NJIT IT490 Summer 2026
