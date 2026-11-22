# ACEest Fitness & Gym — DevOps Assignment 2

A Flask-based fitness-management application enhanced with DevOps automation, containerization, code-quality analysis, Kubernetes orchestration, and advanced deployment strategies.

This project extends the original ACEest Fitness & Gym application from Assignment 1. It demonstrates how a Flask application can be developed, tested, packaged, analyzed, deployed, and managed using modern DevOps tools and practices.

> **Project Scope:** The assignment carries forward the fitness-programme and client-management functionality from Assignment 1 and extends it with CI/CD automation, Docker, Jenkins, SonarQube, Kubernetes, and Istio-based deployment strategies.

## Features

### Application Features
- Four fitness programmes: Fat Loss (3-day), Fat Loss (5-day), Muscle Gain (PPL), and Beginner.
- Add, list, and delete client profiles.
- Input validation and case-insensitive duplicate-name prevention.
- SQLite database persistence.
- Calorie estimation based on programme-specific multipliers.
- Dashboard statistics and weekly adherence information.
- Health endpoint at `/healthz`.
- Version endpoint at `/version`.
- JSON endpoints at `/api/programs` and `/api/clients`.
- Responsive interface using HTML and CSS.

### DevOps Features
- Git and GitHub for source-code version control.
- Pytest for automated application testing.
- Pytest-cov for code coverage reporting.
- Docker multi-stage builds for production and testing.
- Non-root production container.
- Jenkins Declarative Pipeline for CI/CD automation.
- GitHub Actions for automated build and test validation.
- SonarQube for static code analysis and quality-gate validation.
- Docker Hub for container image storage.
- Kubernetes for application deployment and orchestration.
- ConfigMaps and Secrets for application configuration.
- Readiness and liveness probes for application health monitoring.
- Istio for advanced traffic management.

## Technology Stack

| Component | Technology |
|---|---|
| Backend | Python Flask |
| Frontend | HTML, CSS |
| Database | SQLite |
| Testing | Pytest |
| Code Coverage | Pytest-cov |
| Static Analysis | SonarQube |
| Version Control | Git and GitHub |
| CI/CD | Jenkins, GitHub Actions |
| Containerization | Docker |
| Container Registry | Docker Hub |
| Orchestration | Kubernetes |
| Local Kubernetes Cluster | Minikube |
| Traffic Management | Istio |

## Quick Start – Local Application

### Prerequisites

- Python 3.11 or later
- Git

### Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

### Create a Virtual Environment

```bash
python3 -m venv venv
```

Activate it on macOS/Linux:

```bash
source venv/bin/activate
```

For Windows PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

### Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Run the Application

```bash
python app.py
```

Open the application:

**http://127.0.0.1:5000**

The SQLite database is created automatically. By default, it is stored under `instance/aceest_fitness.db`. Set `DATABASE_PATH` to use another location.

### Application Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | Main application dashboard |
| `/healthz` | GET | Application health check |
| `/version` | GET | Application version information |
| `/api/programs` | GET | Fitness programme information |
| `/api/clients` | GET | Client information |
| `/clients` | POST | Add a client |
| `/clients/<id>/delete` | POST | Delete a client |

These endpoints are intended for an educational project. The application does not provide authentication for the JSON endpoints and should not be exposed publicly without additional security controls.

## Automated Testing

The application uses Pytest to validate application routes, business logic, client management, and input validation.

Run tests:

```bash
pytest -v
```

Generate coverage reports:

```bash
pytest --cov=app --cov=services --cov-report=term-missing --cov-report=html --cov-report=xml
```

Reports are generated in:
- `htmlcov/` – HTML coverage report.
- `coverage.xml` – XML coverage report.

Tests use temporary SQLite databases so that the test suite does not modify the normal application database.

## Docker Containerization

The project uses a multi-stage Dockerfile with separate runtime and testing targets.

### Build the Production Image

```bash
docker build --target runtime \
  --build-arg APP_VERSION=1.0.0 \
  -t aceest-fitness:1.0.0 .
```

### Run the Container

```bash
docker run -d \
  -p 5000:5000 \
  --name aceest-container \
  aceest-fitness:1.0.0
```

Open:

**http://127.0.0.1:5000**

### Build and Run the Test Image

```bash
docker build --target test -t aceest-fitness-test .
docker run --rm aceest-fitness-test
```

The production image uses `python:3.12-slim`, runs as a non-root user, and includes a container health check.

The test image includes development dependencies and executes the automated test suite.

### Docker Hub Publishing

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

Docker Hub Repository:

[Add your Docker Hub repository URL here]

## GitHub Actions CI

Workflow file: `.github/workflows/main.yml`

The GitHub Actions workflow automates application validation when code is pushed or a pull request is created.

The workflow includes:
1. Checking out the source code.
2. Setting up Python.
3. Installing application and development dependencies.
4. Compiling Python source files.
5. Running automated Pytest tests.
6. Building the production Docker target.
7. Building the Docker test target.
8. Uploading test reports when configured.

The workflow can also be triggered manually if `workflow_dispatch` is configured.

Check the **Actions** tab in the GitHub repository to view actual workflow execution results.

## Jenkins CI/CD Pipeline

The root-level `Jenkinsfile` defines the Jenkins Declarative Pipeline.

### Pipeline Stages

1. **Checkout:** Retrieves application source code from GitHub.
2. **Environment Setup:** Creates a Python virtual environment and installs dependencies.
3. **Unit Testing:** Executes Pytest and publishes test results.
4. **Docker Testing:** Builds the test image and executes tests inside the container.
5. **SonarQube Analysis:** Performs static code analysis.
6. **Quality Gate:** Checks whether the SonarQube quality gate passes.
7. **Docker Build:** Creates a versioned production image.
8. **Docker Hub Push:** Publishes the image to Docker Hub.
9. **Kubernetes Deployment:** Applies the deployment configuration and updates the application image.
10. **Cleanup:** Removes temporary build resources.

### Jenkins Configuration Requirements

Configure the following in Jenkins:

- Git and Pipeline plugins.
- Docker Pipeline plugin.
- SonarQube Scanner integration.
- JUnit plugin.
- Workspace Cleanup plugin if `cleanWs()` is used.
- Docker CLI and daemon access.
- Python and SonarScanner on the build agent.
- Kubernetes CLI (`kubectl`).

Configure the credentials and server details expected by the Jenkinsfile:

| Configuration | Expected ID / Name |
|---|---|
| Docker Hub credentials | `dockerhub-credentials` |
| Kubernetes kubeconfig | `kubeconfig` |
| SonarQube server | `SonarQube` |

The Jenkins pipeline also requires the configured Kubernetes cluster and Docker Hub repository to be accessible from the Jenkins agent.

SCM polling or a GitHub webhook can be used to trigger builds automatically.

## SonarQube Static Code Analysis

SonarQube is used to analyze application source code and evaluate code quality.

Configuration file:

`sonar-project.properties`

The project uses:
- Project key: `aceest-fitness`
- Project name: `ACEest Fitness & Gym`
- Source code: Python application files.
- Test framework: Pytest.
- Coverage input: `coverage.xml`.

### Start SonarQube

From the project root:

```bash
docker compose -f sonarqube/docker-compose.yml up -d
```

Open:

**http://localhost:9000**

Log in using the initial administrator credentials and change the password when prompted.

Generate the coverage report:

```bash
pytest --cov=app --cov=services --cov-report=xml
```

Run SonarScanner from the project root:

```bash
sonar-scanner
```

Review the analysis results and quality gate in the SonarQube dashboard.

The Jenkins pipeline is configured to stop if the quality gate fails.

## Kubernetes Deployment

The application is deployed using Kubernetes resources.

### Kubernetes Resources

| File | Purpose |
|---|---|
| `namespace.yml` | Creates the application namespace |
| `configmap.yml` | Stores application configuration |
| `secret.yml` | Stores sensitive configuration |
| `deployment.yml` | Defines the application deployment |
| `service.yml` | Exposes the application |
| `blue-deployment.yml` | Deploys the Blue version |
| `green-deployment.yml` | Deploys the Green version |
| `blue-green-service.yml` | Controls Blue-Green traffic |
| `canary-service.yml` | Creates stable and canary Services |
| `canary-routing.yml` | Configures canary traffic distribution |
| `shadow-deployment.yml` | Deploys the shadow version |
| `shadow-service.yml` | Exposes the shadow version internally |
| `shadow-routing.yml` | Configures traffic mirroring |
| `ab-routing.yml` | Configures A/B traffic routing |
| `istio-gateway.yml` | Configures the Istio ingress gateway |

### Start Minikube

```bash
minikube start
```

Verify the cluster:

```bash
kubectl get nodes
kubectl cluster-info
```

### Apply Base Kubernetes Resources

Apply the namespace first:

```bash
kubectl apply -f kubernetes/namespace.yml
```

Apply application configuration:

```bash
kubectl apply -f kubernetes/configmap.yml
kubectl apply -f kubernetes/secret.yml
```

Update the Docker image name in the deployment manifest to your Docker Hub repository.

Apply the application deployment and Service:

```bash
kubectl apply -f kubernetes/deployment.yml
kubectl apply -f kubernetes/service.yml
```

Check the resources:

```bash
kubectl get all -n aceest-fitness
```

### Access the Application

```bash
minikube service aceest-fitness-service -n aceest-fitness --url
```

Open the returned URL in a browser.

## Advanced Kubernetes Deployment Strategies

The project demonstrates five deployment strategies.

### 1. Rolling Update

Gradually replaces old application pods with new pods while maintaining availability.

Configuration:
- `kubernetes/deployment.yml`

Commands:

```bash
kubectl apply -f kubernetes/deployment.yml

kubectl rollout status deployment/aceest-fitness -n aceest-fitness
```

Rollback:

```bash
kubectl rollout undo deployment/aceest-fitness -n aceest-fitness
```

### 2. Blue-Green Deployment

Maintains two application versions simultaneously.

- Blue: Current stable version.
- Green: New application version.

Files:
- `blue-deployment.yml`
- `green-deployment.yml`
- `blue-green-service.yml`

Switch traffic to Green:

```bash
kubectl patch service aceest-fitness-blue-green \
  -n aceest-fitness \
  -p '{"spec":{"selector":{"app":"aceest-fitness","version":"green"}}}'
```

Rollback to Blue:

```bash
kubectl patch service aceest-fitness-blue-green \
  -n aceest-fitness \
  -p '{"spec":{"selector":{"app":"aceest-fitness","version":"blue"}}}'
```

### 3. Canary Deployment

Gradually releases a new version to a small percentage of traffic.

Initial traffic distribution:
- Stable version: 90%.
- Canary version: 10%.

Files:
- `blue-deployment.yml`
- `green-deployment.yml`
- `canary-service.yml`
- `canary-routing.yml`
- `istio-gateway.yml`

Apply the routing configuration after the deployments and Services are ready:

```bash
kubectl apply -f kubernetes/canary-routing.yml
```

Traffic weights can be adjusted to promote or roll back the canary version.

### 4. Shadow Deployment

Duplicates incoming requests and sends them to a shadow application version.

- Stable version handles normal user requests.
- Shadow version receives mirrored requests.
- Shadow responses are not returned to users.

Files:
- `shadow-deployment.yml`
- `shadow-service.yml`
- `shadow-routing.yml`

Apply:

```bash
kubectl apply -f kubernetes/shadow-deployment.yml
kubectl apply -f kubernetes/shadow-service.yml
kubectl apply -f kubernetes/shadow-routing.yml
```

Shadow testing should use read-only requests or an isolated database to prevent duplicate database writes and other side effects.

### 5. A/B Testing

Routes requests to different application versions based on the `x-user-group` HTTP header.

| User Group | Header | Destination |
|---|---|---|
| A | `x-user-group: A` | Stable version |
| B | `x-user-group: B` | Canary version |
| Default | No matching header | Stable version |

Files:
- `ab-routing.yml`
- `canary-service.yml`
- `istio-gateway.yml`

Test Group A:

```bash
curl -H "x-user-group: A" http://YOUR_INGRESS_IP/
```

Test Group B:

```bash
curl -H "x-user-group: B" http://YOUR_INGRESS_IP/
```

The client or gateway must supply the user-group header; the routing configuration does not automatically assign users to groups.

## Istio Setup

Istio is required for Canary, Shadow, and A/B testing.

Install Istio using the Istio CLI:

```bash
istioctl install --set profile=demo -y
```

Verify Istio components:

```bash
kubectl get pods -n istio-system
```

Apply the application Gateway:

```bash
kubectl apply -f kubernetes/istio-gateway.yml
```

Apply the relevant VirtualService manifest only after the required Deployments and Services exist.

## Monitoring and Rollback

Check application pods:

```bash
kubectl get pods -n aceest-fitness
```

Check deployments:

```bash
kubectl get deployments -n aceest-fitness
```

View application logs:

```bash
kubectl logs POD_NAME -n aceest-fitness
```

Check rollout history:

```bash
kubectl rollout history deployment/aceest-fitness -n aceest-fitness
```

Rollback the standard deployment:

```bash
kubectl rollout undo deployment/aceest-fitness -n aceest-fitness
```

For Blue-Green and Canary deployments, traffic can be redirected to the previous stable version.

## Project Structure

```text
.
├── app.py
├── services.py
├── templates/
│   └── index.html
├── static/
│   └── styles.css
├── tests/
│   └── test_app.py
├── requirements.txt
├── requirements-dev.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
├── .github/
│   └── workflows/
│       └── main.yml
├── Jenkinsfile
├── sonar-project.properties
├── sonarqube/
│   └── docker-compose.yml
├── kubernetes/
│   ├── namespace.yml
│   ├── configmap.yml
│   ├── secret.yml
│   ├── deployment.yml
│   ├── service.yml
│   ├── blue-deployment.yml
│   ├── green-deployment.yml
│   ├── blue-green-service.yml
│   ├── canary-service.yml
│   ├── canary-routing.yml
│   ├── shadow-deployment.yml
│   ├── shadow-service.yml
│   ├── shadow-routing.yml
│   ├── ab-routing.yml
│   └── istio-gateway.yml
├── docs/
│   ├── architecture.md
│   ├── deployment-strategies.md
│   └── setup-guide.md
├── reports/
│   ├── README.md
│   ├── test-report.md
│   ├── sonar-report.md
│   └── deployment-report.md
├── screenshots/
└── README.md
```

## Documentation and Reports

Additional project documentation is available in the `docs/` directory.

| Document | Description |
|---|---|
| `architecture.md` | Application and DevOps architecture |
| `deployment-strategies.md` | Explanation of all five deployment strategies |
| `setup-guide.md` | Environment setup and deployment instructions |

The `reports/` directory contains:
- Automated testing report.
- SonarQube analysis report.
- Deployment and CI/CD report.

Actual test results, quality-gate status, Jenkins execution evidence, Docker Hub details, and Kubernetes deployment results should be recorded after running and verifying the corresponding tools.

## Security and Deployment Considerations

- Replace the default Flask secret key with a strong secret before deployment.
- Never commit real credentials, tokens, or passwords to GitHub.
- Use Kubernetes Secrets for sensitive configuration.
- Use HTTPS and a production WSGI server for public deployment.
- The current application uses SQLite. Multiple Kubernetes replicas have separate container-local databases, so they do not share consistent application data. A shared database such as PostgreSQL is recommended for reliable multi-replica deployments.
- Shadow traffic can duplicate writes and should be isolated or restricted to read-only operations.
- Ensure Istio is installed before applying Istio Gateway and VirtualService resources.
- Apply the namespace before other namespaced Kubernetes resources.
- Apply advanced deployment manifests selectively; do not apply every strategy simultaneously because they may configure competing traffic routes.

## Assignment Deliverables

The project includes the following implementation areas:

1. Flask application carried forward from Assignment 1.
2. Git and GitHub source-code management.
3. Automated testing using Pytest.
4. Docker production and test images.
5. Jenkins CI/CD pipeline.
6. SonarQube static code analysis and quality gate.
7. Docker Hub image publishing.
8. Kubernetes deployment and Service configuration.
9. Rolling Update, Blue-Green, Canary, Shadow, and A/B testing manifests.
10. Project architecture, setup, deployment, and testing documentation.

## Repository and Evidence

**GitHub Repository:** [Add your public GitHub repository URL]

**Docker Hub Repository:** [Add your Docker Hub repository URL]

**Jenkins Build Evidence:** [Add Jenkins job/build URL or screenshot]

**SonarQube Evidence:** [Add SonarQube project/dashboard screenshot]

**Kubernetes Application Endpoint:** [Add your verified application endpoint]

**Deployment Evidence:** [Add screenshots of running pods, Services, and deployment strategies]

## Conclusion

ACEest Fitness & Gym demonstrates the integration of software development and DevOps practices through automated testing, CI/CD, static code analysis, containerization, and Kubernetes orchestration.

The project extends the original Flask application with deployment automation and multiple release strategies, providing practical exposure to modern application delivery and infrastructure management.
