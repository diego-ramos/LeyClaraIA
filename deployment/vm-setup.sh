#!/bin/bash
set -e

echo "=== LeyClara.IA VM Setup Script ==="
echo "This script will install Docker, Docker Compose, and configure the system"

# Update system
echo "Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# Install Docker
echo "Installing Docker..."
sudo apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# Add Docker's official GPG key
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Set up the repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Add current user to docker group
sudo usermod -aG docker $USER

# Install Docker Compose standalone (for compatibility)
echo "Installing Docker Compose..."
sudo curl -L "https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Create application directory
echo "Creating application directory..."
sudo mkdir -p /opt/leyclara-ia
sudo chown $USER:$USER /opt/leyclara-ia

# Create persistent data directories
echo "Creating persistent data directories..."
mkdir -p /opt/leyclara-ia/data/chroma
mkdir -p /opt/leyclara-ia/data/uploads
mkdir -p /opt/leyclara-ia/data/documents

# Configure firewall
echo "Configuring firewall..."
sudo apt-get install -y ufw
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw --force enable

# Enable Docker to start on boot
echo "Enabling Docker service..."
sudo systemctl enable docker
sudo systemctl start docker

# Create systemd service for auto-start
echo "Creating systemd service..."
sudo tee /etc/systemd/system/leyclara-ia.service > /dev/null <<EOF
[Unit]
Description=LeyClara.IA Application
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/leyclara-ia
ExecStart=/usr/local/bin/docker-compose -f docker-compose.prod.yml up -d
ExecStop=/usr/local/bin/docker-compose -f docker-compose.prod.yml down
User=$USER

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable leyclara-ia.service

echo "=== Setup Complete ==="
echo "Please log out and log back in for Docker group changes to take effect"
echo "Application directory: /opt/leyclara-ia"
echo ""
echo "Next steps:"
echo "1. Copy your application files to /opt/leyclara-ia"
echo "2. Create .env file with your API keys"
echo "3. Run: sudo systemctl start leyclara-ia"
