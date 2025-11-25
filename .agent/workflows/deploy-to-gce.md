---
description: How to deploy the LeyClara.IA application to Google Compute Engine VM
---

# Deploying to Google Compute Engine (GCE)

This guide explains how to deploy LeyClara.IA to a Google Compute Engine VM with persistent storage.

## Why GCE Instead of Cloud Run?

**Cloud Run** is stateless - data stored in containers (ChromaDB, uploaded files) is lost on restart.

**GCE VM** provides:
- ✅ Persistent disk storage
- ✅ Full control over the server
- ✅ Predictable costs (~$15-30/month)
- ✅ No cold starts

## Prerequisites

1. **Google Cloud Project** with billing enabled
2. **gcloud CLI** installed and authenticated:
   ```bash
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   ```
3. **API Keys**:
   - Google API Key (for Gemini)
   - YouTube API Key (optional)

## Initial Deployment

### Step 1: Configure Project ID

Edit `deployment/deploy.sh` and change line 4:
```bash
PROJECT_ID="your-gcp-project-id"  # CHANGE THIS to your actual project ID
```

### Step 2: Run Deployment Script

From the project root:
```bash
chmod +x deployment/deploy.sh
./deployment/deploy.sh
```

This script will:
- Create a VM instance (e2-small, 2GB RAM, 30GB disk)
- Configure firewall rules (ports 80, 443)
- Install Docker and Docker Compose
- Copy application files to the VM
- Set up auto-start service

**Note**: The script will take 5-10 minutes to complete.

### Step 3: Configure Environment Variables

SSH into the VM:
```bash
gcloud compute ssh leyclara-ia-vm --zone=us-central1-a
```

Create `.env` file:
```bash
cd /opt/leyclara-ia
nano .env
```

Add your API keys:
```env
GOOGLE_API_KEY=your_google_api_key_here
YOUTUBE_API_KEY=your_youtube_api_key_here
VITE_API_URL=http://YOUR_VM_IP:8000
```

**Replace `YOUR_VM_IP`** with the external IP shown at the end of the deployment script.

### Step 4: Create Frontend Environment File

```bash
nano frontend/.env
```

Add:
```env
VITE_API_URL=http://YOUR_VM_IP:8000
```

### Step 5: Start the Application

```bash
sudo systemctl start leyclara-ia
```

Check status:
```bash
sudo systemctl status leyclara-ia
docker ps
```

You should see two containers running: `leyclara-backend` and `leyclara-frontend`.

### Step 6: Access Your Application

Open your browser and navigate to:
```
http://YOUR_VM_IP
```

## Updating the Application

When you make code changes and want to deploy them:

```bash
chmod +x deployment/update.sh
./deployment/update.sh
```

This will:
- Copy updated files to the VM
- Rebuild containers
- Restart services
- **Preserve all data** (uploaded documents, ChromaDB index)

## Useful Commands

### View Logs

```bash
gcloud compute ssh leyclara-ia-vm --zone=us-central1-a
cd /opt/leyclara-ia
docker-compose -f docker-compose.prod.yml logs -f
```

### Restart Services

```bash
gcloud compute ssh leyclara-ia-vm --zone=us-central1-a
sudo systemctl restart leyclara-ia
```

### Stop Services

```bash
gcloud compute ssh leyclara-ia-vm --zone=us-central1-a
sudo systemctl stop leyclara-ia
```

### Check Disk Usage

```bash
gcloud compute ssh leyclara-ia-vm --zone=us-central1-a
df -h
du -sh /opt/leyclara-ia/data/*
```

### Backup Data

```bash
# From your local machine
gcloud compute scp --recurse leyclara-ia-vm:/opt/leyclara-ia/data ./backup-$(date +%Y%m%d) --zone=us-central1-a
```

## Cost Optimization

### Current Configuration
- **Machine Type**: e2-small (2 vCPU, 2GB RAM)
- **Disk**: 30GB standard persistent disk
- **Estimated Cost**: ~$15-20/month

### To Reduce Costs

Use e2-micro (free tier eligible):
```bash
# Edit deployment/deploy.sh, change line 7:
MACHINE_TYPE="e2-micro"  # 0.25-2 vCPU, 1GB RAM - Free tier
```

**Note**: e2-micro may be slower with large documents.

### To Increase Performance

Use e2-medium for more traffic:
```bash
MACHINE_TYPE="e2-medium"  # 1-2 vCPU, 4GB RAM - ~$30/month
```

## Troubleshooting

### Application Not Starting

Check logs:
```bash
gcloud compute ssh leyclara-ia-vm --zone=us-central1-a
journalctl -u leyclara-ia -n 50
docker-compose -f /opt/leyclara-ia/docker-compose.prod.yml logs
```

### Cannot Access Application

1. Check VM is running:
   ```bash
   gcloud compute instances list
   ```

2. Verify firewall rules:
   ```bash
   gcloud compute firewall-rules list
   ```

3. Check if containers are running:
   ```bash
   gcloud compute ssh leyclara-ia-vm --zone=us-central1-a
   docker ps
   ```

### Out of Disk Space

Increase disk size:
```bash
gcloud compute disks resize leyclara-ia-vm --size=50GB --zone=us-central1-a
```

Then resize filesystem:
```bash
gcloud compute ssh leyclara-ia-vm --zone=us-central1-a
sudo resize2fs /dev/sda1
```

## Deleting the Deployment

To remove everything and stop charges:

```bash
gcloud compute instances delete leyclara-ia-vm --zone=us-central1-a
```

**Warning**: This will delete all data permanently.

## Next Steps: Adding SSL/HTTPS

For production use with a custom domain, see the SSL setup guide (coming soon).
