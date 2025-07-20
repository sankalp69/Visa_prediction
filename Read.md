# 🚀 Step-by-Step GCP CI/CD Deployment Guide

## Prerequisites Checklist

- [ ] Google Cloud Platform account
- [ ] GitHub repository with your code
- [ ] Google Cloud SDK installed locally
- [ ] Docker installed locally (for testing)

---

## Step 1: GCP Project Setup

### 1.1 Create/Select GCP Project
```bash
# List existing projects
gcloud projects list

# Create new project (if needed)
gcloud projects create YOUR_PROJECT_ID --name="US Visa Prediction"

# Set the project
gcloud config set project YOUR_PROJECT_ID
```

### 1.2 Enable Billing
- Go to [GCP Console](https://console.cloud.google.com/)
- Navigate to Billing
- Link a billing account to your project

### 1.3 Enable Required APIs
```bash
# Enable Cloud Build API
gcloud services enable cloudbuild.googleapis.com

# Enable Cloud Run API
gcloud services enable run.googleapis.com

# Enable Container Registry API
gcloud services enable containerregistry.googleapis.com

# Enable Cloud Resource Manager API
gcloud services enable cloudresourcemanager.googleapis.com

# Enable Secret Manager API (optional, for secrets)
gcloud services enable secretmanager.googleapis.com
```

---

## Step 2: Service Account Setup

### 2.1 Create Service Account
```bash
# Create service account for GitHub Actions
gcloud iam service-accounts create github-actions \
    --description="Service account for GitHub Actions CI/CD" \
    --display-name="GitHub Actions"
```

### 2.2 Grant Required Permissions
```bash
# Grant Cloud Run Admin role
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:github-actions@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/run.admin"

# Grant Storage Admin role (for Container Registry)
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:github-actions@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/storage.admin"

# Grant Cloud Build Service Account role
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:github-actions@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/cloudbuild.builds.builder"

# Grant Service Account User role
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:github-actions@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/iam.serviceAccountUser"
```

### 2.3 Create and Download Service Account Key
```bash
# Create service account key
gcloud iam service-accounts keys create key.json \
    --iam-account=github-actions@YOUR_PROJECT_ID.iam.gserviceaccount.com

# Display the key content (copy this for GitHub secrets)
cat key.json
```

---

## Step 3: GitHub Repository Setup

### 3.1 Add GitHub Secrets
Go to your GitHub repository → Settings → Secrets and variables → Actions

Add the following secrets:

| Secret Name | Value |
|-------------|-------|
| `GCP_PROJECT_ID` | Your GCP project ID |
| `GCP_SA_KEY` | Entire content of `key.json` file |
| `MONGODB_URL` | Your MongoDB connection string |
| `AWS_ACCESS_KEY_ID` | Your AWS access key |
| `AWS_SECRET_ACCESS_KEY` | Your AWS secret key |
| `AWS_DEFAULT_REGION` | Your AWS region (e.g., us-east-1) |

### 3.2 Verify Repository Structure
Ensure your repository has these files:
```
├── .github/workflows/gcp-deploy.yaml
├── Dockerfile.gcp
├── requirements.txt
├── app.py
├── cloudbuild.yaml (optional)
├── app.yaml (optional)
└── terraform/ (optional)
```

---

## Step 4: Local Testing (Optional)

### 4.1 Test Docker Build Locally
```bash
# Build the Docker image
docker build -f Dockerfile.gcp -t us-visa-app .

# Test the container locally
docker run -p 8080:8080 \
  -e MONGODB_URL="your-mongodb-url" \
  -e AWS_ACCESS_KEY_ID="your-aws-key" \
  -e AWS_SECRET_ACCESS_KEY="your-aws-secret" \
  -e AWS_DEFAULT_REGION="us-east-1" \
  us-visa-app
```

### 4.2 Test Application
```bash
# Test health endpoint
curl http://localhost:8080/health

# Test main application
curl http://localhost:8080/
```

---

## Step 5: Deploy to GCP

### 5.1 Trigger Deployment
```bash
# Push to main branch to trigger GitHub Actions
git add .
git commit -m "Initial GCP deployment setup"
git push origin main
```

### 5.2 Monitor Deployment
1. Go to your GitHub repository
2. Click on "Actions" tab
3. Monitor the "Deploy to Google Cloud Platform" workflow
4. Check for any errors in the build logs

### 5.3 Verify Deployment
```bash
# List Cloud Run services
gcloud run services list --region=us-central1

# Get service URL
gcloud run services describe us-visa-prediction \
    --region=us-central1 \
    --format='value(status.url)'

# Test the deployed application
curl https://your-service-url/health
```

---

## Step 6: Post-Deployment Setup

### 6.1 Set Up Custom Domain (Optional)
```bash
# Map custom domain to Cloud Run service
gcloud run domain-mappings create \
    --service us-visa-prediction \
    --domain your-domain.com \
    --region us-central1
```

### 6.2 Configure Monitoring
```bash
# Create alerting policy
gcloud alpha monitoring policies create \
    --policy-from-file=monitoring-policy.yaml
```

### 6.3 Set Up Logging
```bash
# View application logs
gcloud logging read "resource.type=cloud_run_revision" \
    --limit=50 \
    --format="table(timestamp,severity,textPayload)"
```

---

## Step 7: Continuous Deployment

### 7.1 Automatic Deployments
- Every push to `main` branch triggers deployment
- Pull requests trigger testing only
- Failed builds are reported in GitHub

### 7.2 Manual Deployments
```bash
# Manual deployment using gcloud
gcloud run deploy us-visa-prediction \
    --image gcr.io/YOUR_PROJECT_ID/us-visa-app:latest \
    --region us-central1 \
    --platform managed \
    --allow-unauthenticated
```

---

## Troubleshooting

### Common Issues and Solutions

#### 1. Build Failures
```bash
# Check build logs
gcloud builds list --limit=10

# View specific build
gcloud builds describe BUILD_ID
```

#### 2. Permission Errors
```bash
# Verify service account permissions
gcloud projects get-iam-policy YOUR_PROJECT_ID \
    --flatten="bindings[].members" \
    --format="table(bindings.role)" \
    --filter="bindings.members:github-actions"
```

#### 3. Application Errors
```bash
# Check Cloud Run logs
gcloud logging read "resource.type=cloud_run_revision" \
    --limit=100 \
    --format="table(timestamp,severity,textPayload)"
```

#### 4. Environment Variables
```bash
# Update environment variables
gcloud run services update us-visa-prediction \
    --region=us-central1 \
    --set-env-vars="MONGODB_URL=new-url"
```

---

## Cost Optimization

### 7.1 Resource Limits
- CPU: 1 vCPU (minimum)
- Memory: 2GB (adequate for ML models)
- Max instances: 10 (prevents cost spikes)

### 7.2 Scaling Configuration
```bash
# Update scaling configuration
gcloud run services update us-visa-prediction \
    --region=us-central1 \
    --min-instances=0 \
    --max-instances=5 \
    --concurrency=80
```

---

## Security Best Practices

### 7.1 Secret Management
```bash
# Store secrets in Secret Manager
echo -n "your-secret" | gcloud secrets create mongodb-url --data-file=-

# Use secrets in Cloud Run
gcloud run services update us-visa-prediction \
    --region=us-central1 \
    --set-env-vars="MONGODB_URL=projects/YOUR_PROJECT_ID/secrets/mongodb-url/versions/latest"
```

### 7.2 Network Security
```bash
# Restrict access to specific IPs (if needed)
gcloud run services update us-visa-prediction \
    --region=us-central1 \
    --ingress=internal
```

---

## Success Checklist

- [ ] GCP project created and billing enabled
- [ ] Required APIs enabled
- [ ] Service account created with proper permissions
- [ ] GitHub secrets configured
- [ ] Code pushed to main branch
- [ ] GitHub Actions workflow completed successfully
- [ ] Application accessible via Cloud Run URL
- [ ] Health check endpoint responding
- [ ] Application functionality tested
- [ ] Monitoring and logging configured

---

## Next Steps

1. **Set up monitoring alerts** for application health
2. **Configure custom domain** for production use
3. **Implement blue-green deployments** for zero-downtime updates
4. **Set up backup and disaster recovery** procedures
5. **Optimize performance** based on usage patterns

Your US Visa prediction application is now successfully deployed on Google Cloud Platform with automated CI/CD! 🎉 