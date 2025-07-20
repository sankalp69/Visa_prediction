@echo off
REM GCP Deployment Script for US Visa Prediction Project (Windows)
REM Usage: deploy-gcp.bat PROJECT_ID

setlocal enabledelayedexpansion

if "%1"=="" (
    echo Usage: deploy-gcp.bat PROJECT_ID
    echo Example: deploy-gcp.bat my-visa-project
    exit /b 1
)

set PROJECT_ID=%1

echo 🚀 Starting GCP deployment setup for project: %PROJECT_ID%

REM Step 1: Set project
echo 📋 Setting GCP project...
gcloud config set project %PROJECT_ID%

REM Step 2: Enable required APIs
echo 🔧 Enabling required APIs...
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable cloudresourcemanager.googleapis.com
gcloud services enable secretmanager.googleapis.com

REM Step 3: Create service account
echo 👤 Creating service account...
gcloud iam service-accounts create github-actions --description="Service account for GitHub Actions CI/CD" --display-name="GitHub Actions" 2>nul || echo Service account already exists

REM Step 4: Grant permissions
echo 🔐 Granting permissions...
gcloud projects add-iam-policy-binding %PROJECT_ID% --member="serviceAccount:github-actions@%PROJECT_ID%.iam.gserviceaccount.com" --role="roles/run.admin"
gcloud projects add-iam-policy-binding %PROJECT_ID% --member="serviceAccount:github-actions@%PROJECT_ID%.iam.gserviceaccount.com" --role="roles/storage.admin"
gcloud projects add-iam-policy-binding %PROJECT_ID% --member="serviceAccount:github-actions@%PROJECT_ID%.iam.gserviceaccount.com" --role="roles/cloudbuild.builds.builder"
gcloud projects add-iam-policy-binding %PROJECT_ID% --member="serviceAccount:github-actions@%PROJECT_ID%.iam.gserviceaccount.com" --role="roles/iam.serviceAccountUser"

REM Step 5: Create service account key
echo 🔑 Creating service account key...
gcloud iam service-accounts keys create key.json --iam-account=github-actions@%PROJECT_ID%.iam.gserviceaccount.com

echo ✅ GCP setup completed!
echo.
echo 📋 Next steps:
echo 1. Copy the content of key.json to GitHub secret GCP_SA_KEY
echo 2. Add other required secrets to GitHub:
echo    - GCP_PROJECT_ID: %PROJECT_ID%
echo    - MONGODB_URL: your-mongodb-connection-string
echo.
echo 3. Push your code to GitHub main branch to trigger deployment
echo.
echo 🔍 To view the service account key:
echo type key.json

pause 