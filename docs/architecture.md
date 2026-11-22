
# ACEest Fitness & Gym – Application Architecture

## 1. Introduction

ACEest Fitness & Gym is a Flask-based web application developed to manage gym operations. It provides functionality for managing clients, selecting fitness programs, calculating calories, and tracking fitness-related information.

The application is enhanced with DevOps practices, including automated testing, continuous integration, containerization, Kubernetes deployment, and multiple deployment strategies.

## 2. Technology Stack

| Component | Technology |
|---|---|
| Backend | Python Flask |
| Frontend | HTML, CSS |
| Database | SQLite |
| Testing | Pytest |
| Code Coverage | Pytest-cov |
| Code Quality | SonarQube |
| CI/CD | Jenkins |
| Version Control | Git and GitHub |
| Containerization | Docker |
| Container Registry | Docker Hub |
| Orchestration | Kubernetes |
| Traffic Management | Istio |

## 3. High-Level Architecture

The application follows a layered architecture.

### Presentation Layer
- Provides the user interface using HTML and CSS.
- Allows users to interact with the fitness management application.
- Displays client information and fitness program details.

### Application Layer
- Implemented using Flask.
- Handles HTTP requests and application routing.
- Performs client validation and calorie calculations.
- Provides REST API endpoints.

### Data Layer
- Uses SQLite for storing application data.
- Manages client records and related application information.

### DevOps and Deployment Layer
- GitHub maintains source code and version history.
- Jenkins automates build, test, and deployment activities.
- Pytest validates application functionality.
- SonarQube performs static code analysis.
- Docker packages the application into containers.
- Kubernetes manages application deployment and scaling.
- Istio manages advanced traffic routing strategies.

## 4. Application Components

| Component | Responsibility |
|---|---|
| `app.py` | Flask application, routes, database initialization |
| `services.py` | Business logic, validation, calorie calculations |
| `templates/index.html` | Application user interface |
| `static/styles.css` | Frontend styling |
| `tests/test_app.py` | Automated application tests |
| `requirements.txt` | Application dependencies |
| `requirements-dev.txt` | Development and testing dependencies |
| `Dockerfile` | Container image definition |
| `Jenkinsfile` | CI/CD pipeline definition |
| `sonar-project.properties` | SonarQube project configuration |

## 5. Application Workflow

1. A user accesses the ACEest Fitness & Gym application through a browser.
2. Flask receives and processes the HTTP request.
3. Application logic validates the request and performs the required operation.
4. SQLite stores or retrieves the relevant information.
5. Flask returns the response to the user.

## 6. CI/CD Architecture

The CI/CD process follows these stages:

1. Developer pushes source code to GitHub.
2. Jenkins detects changes through SCM polling or a configured webhook.
3. Jenkins checks out the latest source code.
4. Python dependencies are installed.
5. Pytest executes automated tests.
6. Docker builds a test image and executes tests inside the container.
7. SonarQube performs static code analysis and evaluates the quality gate.
8. Jenkins builds the production Docker image.
9. The image is pushed to Docker Hub.
10. Kubernetes deploys the selected image version.

## 7. Deployment Architecture

The application is deployed using Kubernetes.

- Deployments manage application pods.
- Services expose application pods.
- ConfigMaps manage non-sensitive configuration.
- Secrets manage sensitive configuration.
- Readiness and liveness probes monitor application health.
- Istio manages traffic routing for advanced deployment strategies.

## 8. Security and Reliability

The implementation includes:

- Non-root Docker container execution.
- Separation of application and development dependencies.
- Kubernetes Secrets for sensitive configuration.
- Kubernetes health probes.
- Automated testing before deployment.
- Rollback support for deployment failures.

## 9. Conclusion

The architecture combines a Flask-based application with modern DevOps practices. It provides an automated workflow for testing, packaging, analyzing, and deploying application versions while supporting multiple Kubernetes deployment strategies.
