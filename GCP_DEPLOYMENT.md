# GCP Deployment Guide for US Visa Prediction Project

This guide provides step-by-step instructions for deploying the US Visa prediction ML application to Google Cloud Platform using CI/CD.

## 🚀 Prerequisites

### 1. GCP Account Setup
- Create a Google Cloud Platform account
- Create a new project or select an existing one
- Enable billing for the project

### 2. Required GCP APIs
Enable the following APIs in your GCP project:
```bash
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable cloudresourcemanager.googleapis.com
```

### 3. Service Account Setup
Create a service account for CI/CD:
```bash
# Create service account
gcloud iam service-accounts create github-actions \
    --description="Service account for GitHub Actions" \
    --display-name="GitHub Actions"

# Grant necessary roles
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:github-actions@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/run.admin"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:github-actions@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/storage.admin"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:github-actions@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/cloudbuild.builds.builder"

# Create and download key
gcloud iam service-accounts keys create key.json \
    --iam-account=github-actions@YOUR_PROJECT_ID.iam.gserviceaccount.com
```

## 🔧 GitHub Secrets Configuration

Add the following secrets to your GitHub repository:

1. **GCP_PROJECT_ID**: Your GCP project ID
2. **GCP_SA_KEY**: The entire content of the `key.json` file (base64 encoded)
3. **MONGODB_URL**: Your MongoDB connection string
4. **AWS_ACCESS_KEY_ID**: Your AWS access key
5. **AWS_SECRET_ACCESS_KEY**: Your AWS secret key
6. **AWS_DEFAULT_REGION**: Your AWS region (e.g., us-east-1)

## 🏗️ Deployment Options

### Option 1: GitHub Actions (Recommended)

1. **Push to main branch** - The workflow will automatically trigger
2. **Monitor deployment** in GitHub Actions tab
3. **Access your application** at the provided Cloud Run URL

### Option 2: Cloud Build

1. **Connect your repository** to Cloud Build
2. **Create a trigger** using the `cloudbuild.yaml` file
3. **Set substitution variables** in the trigger configuration

### Option 3: Terraform (Infrastructure as Code)

1. **Install Terraform** and configure GCP provider
2. **Create terraform.tfvars** file with your variables:
```hcl
project_id = "your-project-id"
region = "us-central1"
mongodb_url = "your-mongodb-url"
aws_access_key_id = "your-aws-key"
aws_secret_access_key = "your-aws-secret"
github_owner = "your-github-username"
github_repo = "your-repo-name"
```

3. **Deploy infrastructure**:
```bash
cd terraform
terraform init
terraform plan
terraform apply
```

### Option 4: App Engine

1. **Deploy using gcloud**:
```bash
gcloud app deploy app.yaml
```

## 🔍 Monitoring and Logging

### Cloud Run Monitoring
- **Metrics**: CPU, memory, request count, latency
- **Logs**: Application logs in Cloud Logging
- **Alerts**: Set up alerting policies

### Application Health Checks
The application includes health checks at `/health` endpoint.

## 🔒 Security Considerations

1. **Service Account**: Use least privilege principle
2. **Environment Variables**: Store sensitive data in Secret Manager
3. **Network Security**: Configure VPC if needed
4. **HTTPS**: Cloud Run provides automatic HTTPS

## 📊 Cost Optimization

1. **Resource Limits**: Set appropriate CPU/memory limits
2. **Scaling**: Configure min/max instances
3. **Region**: Choose cost-effective regions
4. **Monitoring**: Track usage and costs

## 🚨 Troubleshooting

### Common Issues

1. **Build Failures**:
   - Check Dockerfile syntax
   - Verify requirements.txt
   - Check resource limits

2. **Runtime Errors**:
   - Check application logs
   - Verify environment variables
   - Test locally first

3. **Permission Issues**:
   - Verify service account roles
   - Check IAM policies
   - Ensure API enablement

### Useful Commands

```bash
# Check service status
gcloud run services describe us-visa-prediction --region=us-central1

# View logs
gcloud logging read "resource.type=cloud_run_revision" --limit=50

# Update service
gcloud run services update us-visa-prediction --image=gcr.io/PROJECT_ID/us-visa-app:latest

# Delete service
gcloud run services delete us-visa-prediction --region=us-central1
```

## 🔄 CI/CD Pipeline Flow

1. **Code Push** → GitHub repository
2. **GitHub Actions** → Build and test
3. **Docker Build** → Create container image
4. **Push to GCR** → Store in Container Registry
5. **Deploy to Cloud Run** → Update service
6. **Health Check** → Verify deployment

## 📈 Scaling Configuration

The application is configured with:
- **CPU**: 1 vCPU
- **Memory**: 2GB
- **Max Instances**: 10
- **Concurrency**: 80 requests per instance

Adjust these settings based on your requirements.

## 🔗 Useful Links

- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Cloud Build Documentation](https://cloud.google.com/cloud-build/docs)
- [Container Registry Documentation](https://cloud.google.com/container-registry/docs)
- [Terraform GCP Provider](https://registry.terraform.io/providers/hashicorp/google/latest/docs) 