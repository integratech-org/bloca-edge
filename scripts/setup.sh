#!/bin/bash

# bloca-edge - Development Environment Setup Script
# This script sets up the development environment for the bloca-edge project.
# It installs necessary dependencies, configures the environment, and prepares the project for development.
#
# Usage:
# ./scripts/setup.sh
# make setup

set -e # Exit on any error

# ===========================================
# Configuration
# ===========================================

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# ===========================================
# Print Functions
# ===========================================

print_header() {
  echo ""
  echo -e "${CYAN}========================================${NC}"
  echo -e "${CYAN}  $1${NC}"
  echo -e "${CYAN}========================================${NC}"
  echo ""
}

print_step() {
  echo -e "${BLUE}[STEP]${NC} $1"
}

print_info() {
  echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
  echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
  echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
  echo -e "${RED}[ERROR]${NC} $1"
}

# ===========================================
# Utility Functions
# ===========================================

command_exists() {
  command -v "$1" >/dev/null 2>&1
}

# ===========================================
# Validation
# ===========================================

check_requirements() {
  print_step "Checking system requirements..."

  local has_errors=false

  # Check Docker
  if ! command_exists docker; then
      print_error "Docker is not installed"
      print_info "Install from: https://www.docker.com/get-started"
      has_errors=true
  elif ! docker info >/dev/null 2>&1; then
      print_error "Docker is not running"
      print_info "Please start Docker Desktop or the Docker daemon"
      has_errors=true
  else
      print_success "Docker is running"
  fi

  # Check Docker Compose
  if command_exists docker-compose; then
      print_success "Docker Compose available"
  elif docker compose version >/dev/null 2>&1; then
      print_success "Docker Compose available (plugin)"
  else
      print_error "Docker Compose not found"
      has_errors=true
  fi

  # Check UV
  if command_exists uv; then
    print_success "UV package manager available"
  else
    print_warning "UV not installed"
    print_info "Install with: curl -LsSf https://astral.sh/uv/install.sh | sh"
    has_errors=true
  fi

  # Check Make (optional)
  if command_exists make; then
    print_success "Make available"
  else
    print_warning "Make not installed (optional)"
  fi

  if [ "$has_errors" = true ]; then
    print_error "Please fix the above issues and try again"
    exit 1
  fi

  print_success "All required tools are available"
}

# ===========================================
# Mosquitto
# ===========================================

setup_mosquitto() {
  print_step "Setting up Mosquitto..."

  mkdir -p mosquitto/config mosquitto/data mosquitto/log

  # The config is committed to git, so it should already exist
  if [ ! -f mosquitto/config/mosquitto.conf ]; then
    print_warning "mosquitto/config/mosquitto.conf not found"
    print_info "Create it before running: docker compose up -d"
  fi

  # The password file is gitignored, but it must exist before the broker starts
  if [ ! -f mosquitto/config/passwd ]; then
    touch mosquitto/config/passwd
    print_info "Created empty mosquitto/config/passwd"
    print_info "Add a user with: docker exec -it mosquitto mosquitto_passwd /mosquitto/config/passwd <username>"
  fi

  # Linux only (Docker Desktop handles this itself).
  # data/log must be owned by UID 1883; passwd must be root-owned, mode 0700.
  if [ "$(uname)" = "Linux" ]; then
    if [ "$(stat -c %u mosquitto/data)" != "1883" ] || [ "$(stat -c %u mosquitto/log)" != "1883" ]; then
      print_info "Setting ownership for mosquitto/data and mosquitto/log (requires sudo)"
      sudo chown -R 1883:1883 mosquitto/data mosquitto/log
    fi

    if [ "$(stat -c %u:%g mosquitto/config/passwd)" != "1883:1883" ] || [ "$(stat -c %a mosquitto/config/passwd)" != "600" ]; then
      print_info "Setting ownership and permissions for mosquitto/config/passwd (requires sudo)"
      sudo chown 1883:1883 mosquitto/config/passwd
      sudo chmod 0600 mosquitto/config/passwd
    fi
  fi

  print_success "Mosquitto directories ready"
}

# ===========================================
# Pre-commit Hooks
# ===========================================

setup_pre_commit() {
  print_step "Setting up pre-commit hooks..."

  if command_exists uv && [ -d .git ]; then
    if [ -f .pre-commit-config.yaml ]; then
      uv run pre-commit install
      print_success "Pre-commit hooks installed"
    else
      print_warning "No .pre-commit-config.yaml found, skipping hooks"
    fi
  else
    print_warning "uv or git not available, skipping pre-commit hooks"
    print_info "Install manually with: make pre-commit-install"
  fi
}

# ===========================================
# Final Summary
# ===========================================
show_summary() {
  print_header "Setup Complete!"

  echo "Your development environment is ready."
  echo ""
  echo "Services:"
  echo -e "  ${GREEN}MQTT broker:${NC}  localhost:1883"
  echo ""
  echo "Next steps:"
  echo -e "  ${CYAN}docker compose up -d${NC}"
  echo -e "  ${CYAN}docker exec -it mosquitto mosquitto_passwd /mosquitto/config/passwd <username>${NC}"
  echo -e "  ${CYAN}docker compose restart mosquitto${NC}"
  echo ""
  echo "Useful commands:"
  echo -e "  ${CYAN}docker compose up -d${NC}                  Start services"
  echo -e "  ${CYAN}docker compose down${NC}                   Stop services"
  echo -e "  ${CYAN}docker compose logs -f mosquitto${NC}      View broker logs"
  echo -e "  ${CYAN}uv run python -m bloca_edge${NC}           Run the app"
  echo ""
  echo -e "${GREEN}Happy coding!${NC}"
  echo ""
}

# ===========================================
# Main Execution
# ===========================================

main() {
  print_header "bloca-edge - Setup"

  check_requirements
  setup_mosquitto
  setup_pre_commit
  show_summary
}

# Run main function
main
