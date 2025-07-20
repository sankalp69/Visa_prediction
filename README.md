# MLOPs-Production-Ready-Machine-Learning-Project

Youtube Playlist: https://youtube.com/playlist?list=PLkz_y24mlSJZvJOj1UXiJPVRQrNFdNEXX&si=FRFLpnve9MS6Rii9

- Anaconda: https://www.anaconda.com/
- Vs code: https://code.visualstudio.com/download
- Git: https://git-scm.com/
- Flowchart: https://whimsical.com/
- MLOPs Tool: https://www.evidentlyai.com/
- MongoDB: https://account.mongodb.com/account/login
- Data link: https://www.kaggle.com/datasets/moro23/easyvisa-dataset


## Git commands

```bash
git add .

git commit -m "Updated"

git push origin main
```


## How to run?

```bash
conda create -n visa python=3.8 -y
```

```bash
conda activate visa
```

```bash
pip install -r requirements.txt
```

## Workflow:

1. constants
2. entity
3. components
4. pipeline
5. Main file



### Export the  environment variable
```bash

export MONGODB_URL="mongodb+srv://<username>:<password>...."

export GCP_PROJECT_ID="your-gcp-project-id"

```


# Google-Cloud-CICD-Deployment-with-Github-Actions

## 1. Login to Google Cloud Console.

## 2. Create IAM user for deployment

	#with specific access

	1. Cloud Run: It is serverless container platform

	2. Container Registry: To save your docker image in GCP


	#Description: About the deployment

	1. Build docker image of the source code

	2. Push your docker image to Container Registry

	3. Deploy to Cloud Run

	4. Lauch your docker image in Cloud Run

	#Policy:

	1. Cloud Run Admin

	2. Storage Admin

	
## 3. Create Container Registry repo to store/save docker image
    - Save the URI: gcr.io/YOUR_PROJECT_ID/us-visa-app

	
## 4. Create Cloud Run service

## 5. Open Cloud Run and Install docker in local Machine:
	
	
	#optional

	sudo apt-get update -y

	sudo apt-get upgrade
	
	#required

	curl -fsSL https://get.docker.com -o get-docker.sh

	sudo sh get-docker.sh

	sudo usermod -aG docker ubuntu

	newgrp docker
	
# 6. Configure GitHub Actions:
    Go to repository settings > Secrets and variables > Actions > Add secrets

# 7. Setup github secrets:

   - GCP_PROJECT_ID
   - GCP_SA_KEY
   - MONGODB_URL

    


