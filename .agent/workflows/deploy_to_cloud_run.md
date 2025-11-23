---
description: How to deploy the TeLoExplico application to Google Cloud Run
---

# Deploying to Google Cloud Run

This guide explains how to deploy your application to Google Cloud Run.

## Prerequisites

1.  **Google Cloud Project**: Ensure you have a project with billing enabled.
2.  **gcloud CLI**: Installed and authenticated (`gcloud auth login`).
3.  **APIs Enabled**: Run the following command to enable necessary services:
    ```bash
    gcloud services enable run.googleapis.com containerregistry.googleapis.com cloudbuild.googleapis.com
    ```

## Step 1: Deploy the Backend

1.  Navigate to the project root directory.
2.  Submit the backend image to Google Container Registry:
    ```bash
    gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/teloexplico-backend ./backend
    ```
    *(Replace `YOUR_PROJECT_ID` with your actual project ID)*

3.  Deploy the backend service:
    ```bash
    gcloud run deploy teloexplico-backend \
      --image gcr.io/YOUR_PROJECT_ID/teloexplico-backend \
      --platform managed \
      --region us-central1 \
      --allow-unauthenticated \
      --set-env-vars GOOGLE_API_KEY=YOUR_API_KEY,YOUTUBE_API_KEY=YOUR_YOUTUBE_KEY
    ```
    *   Replace `YOUR_API_KEY` and `YOUR_YOUTUBE_KEY` with your real keys.
    *   **Note the URL**: The command will output a URL (e.g., `https://teloexplico-backend-xyz.a.run.app`). Copy this.

## Step 2: Prepare the Frontend

**Important**: The frontend currently points to `http://localhost:8000`. You must update this to point to your new backend URL.

1.  Open `frontend/src/components/ChatInterface.jsx`.
2.  Find line 6: `const API_URL = 'http://localhost:8000';`
3.  Change it to your backend URL:
    ```javascript
    const API_URL = 'https://teloexplico-backend-xyz.a.run.app'; // Your actual backend URL
    ```

## Step 3: Deploy the Frontend

1.  Submit the frontend image:
    ```bash
    gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/teloexplico-frontend ./frontend
    ```

2.  Deploy the frontend service:
    ```bash
    gcloud run deploy teloexplico-frontend \
      --image gcr.io/YOUR_PROJECT_ID/teloexplico-frontend \
      --platform managed \
      --region us-central1 \
      --allow-unauthenticated
    ```

3.  **Done!** Visit the URL provided by the frontend deployment command to use your app.

## Important Notes

*   **Data Persistence**: Cloud Run is stateless. Files uploaded to the `uploads/` directory and the `chroma_db` index will be **lost** if the backend service restarts (which happens frequently).
*   **Production Fix**: For a real production app, you should use Google Cloud Storage for files and a persistent database (or a managed ChromaDB instance).
