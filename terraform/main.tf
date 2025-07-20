terraform {
  required_version = ">= 0.13"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# Enable required APIs
resource "google_project_service" "required_apis" {
  for_each = toset([
    "cloudbuild.googleapis.com",
    "run.googleapis.com",
    "containerregistry.googleapis.com",
    "cloudresourcemanager.googleapis.com"
  ])
  
  project = var.project_id
  service = each.value
  
  disable_dependent_services = true
  disable_on_destroy         = false
}

# Cloud Run service
resource "google_cloud_run_service" "us_visa_service" {
  name     = "us-visa-prediction"
  location = var.region

  template {
    spec {
      containers {
        image = "gcr.io/${var.project_id}/us-visa-app:latest"
        
        ports {
          container_port = 8080
        }
        
        resources {
          limits = {
            cpu    = "1000m"
            memory = "2Gi"
          }
        }
        
        env {
          name  = "MONGODB_URL"
          value = var.mongodb_url
        }
        
        env {
          name  = "GCP_PROJECT_ID"
          value = var.project_id
        }
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

# IAM policy to allow unauthenticated access
resource "google_cloud_run_service_iam_member" "public_access" {
  location = google_cloud_run_service.us_visa_service.location
  project  = google_cloud_run_service.us_visa_service.project
  service  = google_cloud_run_service.us_visa_service.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}

# Cloud Build trigger
resource "google_cloudbuild_trigger" "build_trigger" {
  name        = "us-visa-build-trigger"
  description = "Build trigger for US Visa prediction app"
  
  github {
    owner = var.github_owner
    name  = var.github_repo
    push {
      branch = "main"
    }
  }
  
  filename = "cloudbuild.yaml"
  
  substitutions = {
    _MONGODB_URL    = var.mongodb_url
    _GCP_PROJECT_ID = var.project_id
  }
} 