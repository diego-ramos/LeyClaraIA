#!/bin/bash
set -e

# Configuration
PROJECT_ID="your-gcp-project-id"  # CHANGE THIS
VM_NAME="leyclara-ia-vm"
ZONE="us-central1-a"
MACHINE_TYPE="e2-micro"  # 0.25-2 vCPU, 1GB RAM - Free tier eligible
BOOT_DISK_SIZE="30GB"
IMAGE_FAMILY="debian-11"
IMAGE_PROJECT="debian-cloud"

echo "=== LeyClara.IA GCE Deployment Script ==="
echo "Project: $PROJECT_ID"
echo "VM Name: $VM_NAME"
echo "Zone: $ZONE"
echo "Machine Type: $MACHINE_TYPE"
echo ""

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "Error: gcloud CLI is not installed"
    echo "Install from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Set project
echo "Setting GCP project..."
gcloud config set project $PROJECT_ID

# Enable required APIs
echo "Enabling required APIs..."
gcloud services enable compute.googleapis.com

# Create firewall rules if they don't exist
echo "Creating firewall rules..."
gcloud compute firewall-rules create allow-http \
    --allow tcp:80 \
    --source-ranges 0.0.0.0/0 \
    --target-tags http-server \
    --description "Allow HTTP traffic" \
    2>/dev/null || echo "Firewall rule 'allow-http' already exists"

gcloud compute firewall-rules create allow-https \
    --allow tcp:443 \
    --source-ranges 0.0.0.0/0 \
    --target-tags https-server \
    --description "Allow HTTPS traffic" \
    2>/dev/null || echo "Firewall rule 'allow-https' already exists"

# Create VM instance
echo "Creating VM instance..."
gcloud compute instances create $VM_NAME \
    --zone=$ZONE \
    --machine-type=$MACHINE_TYPE \
    --image-family=$IMAGE_FAMILY \
    --image-project=$IMAGE_PROJECT \
    --boot-disk-size=$BOOT_DISK_SIZE \
    --boot-disk-type=pd-standard \
    --tags=http-server,https-server \
    --metadata=startup-script='#!/bin/bash
        apt-get update
        apt-get install -y git
    '

echo "Waiting for VM to be ready..."
sleep 30

# Get VM external IP
VM_IP=$(gcloud compute instances describe $VM_NAME --zone=$ZONE --format='get(networkInterfaces[0].accessConfigs[0].natIP)')
echo "VM External IP: $VM_IP"

# Copy setup script to VM
echo "Copying setup script to VM..."
gcloud compute scp deployment/vm-setup.sh $VM_NAME:/tmp/vm-setup.sh --zone=$ZONE

# Run setup script
echo "Running setup script on VM..."
gcloud compute ssh $VM_NAME --zone=$ZONE --command="chmod +x /tmp/vm-setup.sh && /tmp/vm-setup.sh"

# Copy application files
echo "Copying application files to VM..."
gcloud compute scp --recurse backend frontend docker-compose.prod.yml .env.example $VM_NAME:/opt/leyclara-ia/ --zone=$ZONE

# Create .env file reminder
echo ""
echo "=== IMPORTANT: Next Steps ==="
echo "1. SSH into the VM:"
echo "   gcloud compute ssh $VM_NAME --zone=$ZONE"
echo ""
echo "2. Create .env file with your API keys:"
echo "   cd /opt/leyclara-ia"
echo "   nano .env"
echo ""
echo "   Add these lines:"
echo "   GOOGLE_API_KEY=your_key_here"
echo "   YOUTUBE_API_KEY=your_key_here"
echo "   VITE_API_URL=http://$VM_IP:8000"
echo ""
echo "3. Start the application:"
echo "   sudo systemctl start leyclara-ia"
echo ""
echo "4. Check status:"
echo "   sudo systemctl status leyclara-ia"
echo "   docker ps"
echo ""
echo "5. Access your application at:"
echo "   http://$VM_IP"
echo ""
echo "=== Deployment Complete ==="
