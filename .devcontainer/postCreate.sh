#!/bin/bash
set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

log() {
  echo -e "${CYAN}$(date '+%Y-%m-%d %H:%M:%S')${NC} - ${2:-$GREEN}$1${NC}"
}

log_section() {
  echo -e "\n${BLUE}════════════════════════════════════════════════════════════════${NC}"
  log "$1" "${YELLOW}"
  echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}\n"
}

log_success() {
  log "$1" "${GREEN}"
}

log_error() {
  log "$1" "${RED}"
}

trap 'log_error "An error occurred during setup! See above for details."' ERR

log_section "Installing root npm dependencies"
npm install
log_success "Root npm dependencies installed successfully"

log_section "Installing backend Python dependencies"

log "Installing base requirements..."
pip install -r backend/requirements.txt

log "Installing development requirements..."
pip install -r backend/requirements-dev.txt

log_success "Backend Python dependencies installed successfully"

log_section "Installing frontend dependencies"
cd frontend && npm install
log_success "Frontend dependencies installed successfully"

log_section "Setup complete! Your development environment is ready."