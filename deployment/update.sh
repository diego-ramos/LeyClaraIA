#!/bin/bash
set -e

# Configuration
VM_NAME="leyclara-ia-vm"
ZONE="us-central1-a"

echo "=== LeyClara.IA Update Script ==="
echo "This script will update the application on the VM without losing data"
echo ""

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "Error: gcloud CLI is not installed"
    exit 1
fi

# Get VM IP
VM_IP=$(gcloud compute instances describe $VM_NAME --zone=$ZONE --format='get(networkInterfaces[0].accessConfigs[0].natIP)' 2>/dev/null)

if [ -z "$VM_IP" ]; then
    echo "Error: VM '$VM_NAME' not found in zone '$ZONE'"
    echo "Make sure the VM is running and you have the correct zone"
    exit 1
fi

echo "VM IP: $VM_IP"
echo ""

# Copy updated files
echo "Copying updated application files..."
gcloud compute scp --recurse backend frontend docker-compose.prod.yml $VM_NAME:/opt/leyclara-ia/ --zone=$ZONE

# Run update commands on VM
echo "Updating application on VM..."
gcloud compute ssh $VM_NAME --zone=$ZONE --command="
    cd /opt/leyclara-ia
    echo 'Stopping services...'
    docker-compose -f docker-compose.prod.yml down
    
    echo 'Rebuilding containers...'
    docker-compose -f docker-compose.prod.yml build --no-cache
    
    echo 'Starting services...'
    docker-compose -f docker-compose.prod.yml up -d
    
    echo 'Cleaning up old images...'
    docker image prune -f
    
    echo 'Checking status...'
    docker ps
"

echo ""
echo "=== Update Complete ==="
echo "Application is now running with the latest code"
echo "Access at: http://$VM_IP"
echo ""
echo "To check logs:"
echo "  gcloud compute ssh $VM_NAME --zone=$ZONE"
echo "  cd /opt/leyclara-ia"
echo "  docker-compose -f docker-compose.prod.yml logs -f"
