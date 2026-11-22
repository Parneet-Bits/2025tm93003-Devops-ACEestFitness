
# ACEest Fitness & Gym – Setup and Deployment Guide

## 1. Introduction

This guide explains how to configure, test, containerize, and deploy the ACEest Fitness & Gym application using Docker, Jenkins, SonarQube, and Kubernetes.

## 2. Prerequisites

Install or configure the following tools:

| Tool | Purpose |
|---|---|
| Python 3.12+ | Run the Flask application |
| Git | Version control |
| GitHub | Source code repository |
| Docker | Containerization |
| Docker Hub | Container image registry |
| Jenkins | CI/CD automation |
| SonarQube | Static code analysis |
| Kubernetes | Application orchestration |
| Minikube | Local Kubernetes cluster |
| kubectl | Kubernetes management |
| Istio | Advanced traffic management |

## 3. Clone the Repository

Clone the GitHub repository:

```bash
git clone https://github.com/Parneet-Bits/2025tm93003-Devops-ACEestFitness.git
```

Navigate to the project directory:

```bash
cd 2025tm93003-Devops-ACEestFitness
```

## 4. Set Up the Python Environment

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate the environment on macOS/Linux:

```bash
source venv/bin/activate
```

Install application dependencies:

```bash
pip install -r requirements.txt
```

Install development and testing dependencies:

```bash
pip install -r requirements-dev.txt
```

## 5. Run the Application

Start the Flask application:

```bash
python app.py
```

Open the application in a browser using the local address configured by Flask.

Verify the health endpoint:

```bash
curl http://localhost:5000/healthz
```

Verify the application version:

```bash
curl http://localhost:5000/version
```

## 6. Run Automated Tests

Execute the Pytest suite:

```bash
pytest -v
```

Generate a test coverage report:

```bash
pytest --cov=app --cov=services --cov-report=term-missing --cov-report=html --cov-report=xml
```

The HTML coverage report is generated in the `htmlcov/` directory, and the XML report is generated as `coverage.xml`.

## 7. Build and Run Docker Image

Build the production image:

```bash
docker build --target runtime \
  --build-arg APP_VERSION=1.0.0 \
  -t aceest-fitness:1.0.0 .
```

Run the application container:

```bash
docker run -d \
  -p 5000:5000 \
  --name aceest-container \
  aceest-fitness:1.0.0
```

Check running containers:

```bash
docker ps
```

Test the container health endpoint:

```bash
curl http://localhost:5000/healthz
```

Run automated tests inside the Docker test image:

```bash
docker build --target test -t aceest-fitness-test .
docker run --rm aceest-fitness-test
```

## 8. Push Docker Image to Docker Hub

Log in to Docker Hub:

```bash
docker login
```

Tag the image:

```bash
docker tag aceest-fitness:1.0.0 YOUR_DOCKERHUB_USERNAME/aceest-fitness:1.0.0
```

Push the image:

```bash
docker push YOUR_DOCKERHUB_USERNAME/aceest-fitness:1.0.0
```

Replace `YOUR_DOCKERHUB_USERNAME` with your Docker Hub username.

## 9. Set Up SonarQube

Navigate to the SonarQube directory:

```bash
cd sonarqube
```

Start SonarQube and PostgreSQL:

```bash
docker compose up -d
```

Open SonarQube:

```text
http://localhost:9000
```

Log in using the initial administrator credentials and change the password when prompted.

Create a project with the project key configured in `sonar-project.properties`.

Generate a SonarQube token and configure it securely in Jenkins.

Generate coverage data from the project root:

```bash
pytest --cov=app --cov=services --cov-report=xml
```

Run the SonarScanner from the project root:

```bash
sonar-scanner
```

Review the analysis results and quality gate in the SonarQube dashboard.

## 10. Configure Jenkins

1. Install and start Jenkins.
2. Install the required plugins:
   - Pipeline
   - Git
   - Docker Pipeline
   - SonarQube Scanner
   - JUnit
   - Workspace Cleanup
3. Configure the GitHub repository in Jenkins.
4. Create a Pipeline job.
5. Configure the job to use the repository's `Jenkinsfile`.
6. Configure Docker Hub credentials with the ID `dockerhub-credentials`.
7. Configure SonarQube with the server name `SonarQube`.
8. Configure the SonarQube authentication token.
9. Configure Kubernetes credentials with the ID `kubeconfig`.
10. Enable SCM polling or configure a GitHub webhook.

The Jenkins pipeline automates source checkout, testing, Docker image creation, SonarQube analysis, image publishing, and Kubernetes deployment.

## 11. Set Up Kubernetes Using Minikube

Start Minikube:

```bash
minikube start
```

Verify the cluster:

```bash
kubectl cluster-info
kubectl get nodes
```

Create the application namespace:

```bash
kubectl apply -f kubernetes/namespace.yml
```

Apply the ConfigMap and Secret:

```bash
kubectl apply -f kubernetes/configmap.yml
kubectl apply -f kubernetes/secret.yml
```

Update the Docker image in `kubernetes/deployment.yml` with your Docker Hub image name.

Apply the application Deployment and Service:

```bash
kubectl apply -f kubernetes/deployment.yml
kubectl apply -f kubernetes/service.yml
```

Check the deployed resources:

```bash
kubectl get all -n aceest-fitness
```

## 12. Access the Kubernetes Application

Get the Minikube service URL:

```bash
minikube service aceest-fitness-service -n aceest-fitness --url
```

Open the returned URL in a browser.

Check application pods:

```bash
kubectl get pods -n aceest-fitness
```

Check deployment status:

```bash
kubectl rollout status deployment/aceest-fitness -n aceest-fitness
```

## 13. Configure Istio

Istio is required for Canary, Shadow, and A/B testing traffic management.

Install Istio using the Istio CLI and verify the installation:

```bash
istioctl install --set profile=demo -y
```

Verify the Istio components:

```bash
kubectl get pods -n istio-system
```

Ensure that the ingress gateway is running and that its selector labels match the Gateway configuration.

Apply the application Gateway:

```bash
kubectl apply -f kubernetes/istio-gateway.yml
```

The advanced routing configurations can then be applied separately when their corresponding deployments and Services are ready.

## 14. Deployment Strategy Commands

### Rolling Update

```bash
kubectl apply -f kubernetes/deployment.yml
kubectl rollout status deployment/aceest-fitness -n aceest-fitness
```

### Blue-Green Deployment

```bash
kubectl apply -f kubernetes/blue-deployment.yml
kubectl apply -f kubernetes/green-deployment.yml
kubectl apply -f kubernetes/blue-green-service.yml
```

### Canary Deployment

```bash
kubectl apply -f kubernetes/canary-service.yml
kubectl apply -f kubernetes/canary-routing.yml
```

### Shadow Deployment

```bash
kubectl apply -f kubernetes/shadow-deployment.yml
kubectl apply -f kubernetes/shadow-service.yml
kubectl apply -f kubernetes/shadow-routing.yml
```

### A/B Testing

```bash
kubectl apply -f kubernetes/ab-routing.yml
```

These advanced strategies require Istio to be installed and their associated Deployments, Services, and Gateway to be available.

## 15. Rollback

To roll back the standard Kubernetes deployment:

```bash
kubectl rollout undo deployment/aceest-fitness -n aceest-fitness
```

Check deployment history:

```bash
kubectl rollout history deployment/aceest-fitness -n aceest-fitness
```

For Blue-Green deployment, traffic can be switched back by changing the Service selector to the Blue version.

For Canary deployment, update the Istio traffic weights to send 100% of traffic to the stable version.

## 16. Troubleshooting

### Check Pod Status

```bash
kubectl get pods -n aceest-fitness
```

### View Pod Logs

```bash
kubectl logs POD_NAME -n aceest-fitness
```

### Describe a Pod

```bash
kubectl describe pod POD_NAME -n aceest-fitness
```

### Check Deployment Events

```bash
kubectl describe deployment aceest-fitness -n aceest-fitness
```

### Check Services

```bash
kubectl get services -n aceest-fitness
```

### Check Istio Routing

```bash
kubectl get gateways -n aceest-fitness
kubectl get virtualservices -n aceest-fitness
```

## 17. Important Notes

- Replace all Docker Hub username placeholders before deployment.
- Never commit actual passwords, tokens, or production secrets to GitHub.
- Configure Jenkins credentials securely.
- Ensure the Kubernetes cluster can pull the Docker image.
- SQLite uses local container storage in the current application. Container restarts can affect stored data, and multiple replicas do not share a consistent database. Use PostgreSQL or another shared database for a production multi-replica deployment.
- Shadow traffic should use read-only operations or an isolated database to prevent duplicate writes.
- Apply Istio routing manifests only after installing Istio and creating the required Deployments and Services.

## 18. Conclusion

This setup guide provides the steps required to run, test, containerize, analyze, and deploy ACEest Fitness & Gym.

The project demonstrates DevOps automation through GitHub, Jenkins, Pytest, SonarQube, Docker, Kubernetes, and Istio-based deployment strategies.
