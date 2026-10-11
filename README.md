# ACEest Fitness & Gym — DevOps Assignment 1

A small, container-ready Flask fitness-management application built around the supplied ACEest programme concepts. It includes client onboarding, four training programmes, a simple calorie-estimation rule, weekly adherence, SQLite persistence, automated tests, Docker build targets, GitHub Actions CI, and a Jenkins Declarative Pipeline.

> **Scope note:** The assignment brief explicitly asks for a Flask web app. The provided versions are Tkinter desktop apps, so this project carries forward the fitness-programme/client-management ideas into Flask rather than requiring a desktop GUI. The calorie number is a simple demo estimate using the multipliers in the supplied versions (22, 24, 35 and 26); it is not medical or nutritional advice.

## Features

- Four programme cards: Fat Loss (3-day), Fat Loss (5-day), Muscle Gain (PPL) and Beginner.
- Add, list and delete client profiles; input validation and case-insensitive duplicate-name prevention.
- SQLite persistence with parameterised SQL queries.
- Dashboard totals, average weekly adherence, `/healthz` health endpoint, and read-only JSON endpoints at `/api/programs` and `/api/clients`.
- Mobile-responsive interface; no JavaScript framework or external database required.
- Pytest tests; non-root production Docker image and separate container test target.
- GitHub Actions on every `push` and `pull_request`; Jenkinsfile for secondary build validation.

## Quick start (Python)

Requires Python 3.11+ (CI uses Python 3.12).

```bash
git clone <YOUR_PUBLIC_GITHUB_REPOSITORY_URL>
cd aceest-devops-assignment
python3 -m venv .venv
source .venv/bin/activate       # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt -r requirements-dev.txt
python app.py
```

Open **http://127.0.0.1:5000**. The SQLite database is created automatically. By default it is stored under `instance/aceest_fitness.db`; set `DATABASE_PATH` to choose another location. Stop the development server with `Ctrl+C`.

Available JSON endpoints are `GET /api/programs` (programme and workout/nutrition catalog) and `GET /api/clients` (saved local client rows). They are intended for this local educational project and do not include authentication; do not expose this demo unchanged to the public internet.

For a quick health check:

```bash
curl http://127.0.0.1:5000/healthz
# {"service":"aceest-fitness","status":"ok"}
```

## Run tests manually

```bash
python -m compileall -q app.py services.py tests
python -m pytest -q
```

The test suite verifies the dashboard, health endpoint, client creation, programme-dependent estimate, field validation, duplicate prevention, deletion and safe handling of SQL-like input. Tests use temporary SQLite databases so they do not modify your personal app database.

## Docker

Install Docker Desktop (or Docker Engine) first, then run from the repository root:

```bash
# Build the lightweight runtime image
docker build --target runtime -t aceest-fitness:latest .

# Start the application and keep the database in a named volume
docker volume create aceest-fitness-data
docker run --rm -p 5000:5000 -v aceest-fitness-data:/app/data aceest-fitness:latest

# Build the test target; its Docker build executes pytest and fails on test errors
docker build --target test -t aceest-fitness-test:latest .
```

Open **http://127.0.0.1:5000**. The runtime image uses `python:3.12-slim`, does not install pytest, runs as a non-root user, and includes a `/healthz` Docker health check. The `test` stage adds the development test dependency and runs tests during the image build.

## GitHub Actions CI

Workflow: [`.github/workflows/main.yml`](.github/workflows/main.yml).

On every push and pull request, GitHub Actions checks out the code, sets up Python 3.12, installs the pinned requirements, compiles the Python sources, runs pytest, builds the production Docker target and builds the test target (which runs pytest inside the container). A JUnit XML report is uploaded as an artifact when available. A failed command marks the job as failed. `workflow_dispatch` also permits a manual run.

### Create a public repository and push

1. On GitHub, create a **public, empty** repository. Do not add an initial README or license; this project already has both.
2. Open a terminal in this project folder and initialise Git. Stage the files in logical groups to demonstrate meaningful commit history:

```bash
git init -b main

# Application implementation
git add app.py services.py templates static requirements.txt
git commit -m "feat: add ACEest Flask fitness dashboard"

# Unit and route tests
git add tests requirements-dev.txt
git commit -m "test: cover programme rules and client workflows"

# Infrastructure and automation
git add Dockerfile .dockerignore .github/workflows/main.yml Jenkinsfile
git commit -m "ci: add Docker, GitHub Actions and Jenkins quality gates"

# Documentation and evidence
git add README.md .gitignore .gitattributes docs screenshots reports LICENSE Makefile
git commit -m "docs: add setup instructions and validation evidence"

# Connect and push to your own public repository
git remote add origin https://github.com/<YOUR_USERNAME>/<YOUR_REPOSITORY>.git
git push -u origin main
```

3. Open the repository's **Actions** tab and inspect the `ACEest CI` workflow triggered by the push. Verify that all steps are green. Capture that real run page as evidence if your instructor requests it. Remote proof is only available after the repository has been pushed and the workflow has executed.

The source archive does not include a GitHub remote or claim a remote GitHub Actions/Jenkins run. Replace both placeholders in the remote URL with your own account and repository name.

## Jenkins build and quality gate

The root [`Jenkinsfile`](Jenkinsfile) uses a Declarative Pipeline and assumes a Jenkins agent with Git, Python 3.11+, a working Docker CLI/daemon and access to install pip packages. It checks out the configured repository; creates a clean virtual environment; installs dependencies; compiles the application; runs pytest and publishes the JUnit report; builds the production image; then builds the Docker `test` target. A failed stage fails the build. `cleanWs` requires the Jenkins **Workspace Cleanup** plugin. If it is not installed, remove the `cleanWs` step or install that plugin.

Minimal Jenkins setup:

1. Install a current Jenkins LTS and ensure the agent has Python and Docker available to the Jenkins service account.
2. Add GitHub connectivity/credentials only if required by the repository's access policy (public repository cloning needs no credential).
3. Choose **New Item → Pipeline**, enable **Pipeline script from SCM**, select Git, set your public repository URL and branch `*/main`, and set script path to `Jenkinsfile`.
4. Configure a GitHub webhook to `https://<your-jenkins-host>/github-webhook/` or enable SCM polling for a simple local lab; verify the Jenkins URL is reachable from GitHub before relying on webhooks.
5. Click **Build Now**. Confirm Checkout, Clean Python Build, Unit Tests, Docker Production Build and Containerized Test Quality Gate are successful, and inspect `reports/pytest-results.xml`.

A successful local test run does not prove that your Jenkins server or GitHub Actions remote run has passed; those require running the pipeline in your own configured services.

## Repository structure

```text
.
├── app.py
├── services.py                # reusable programme and validation rules
├── templates/index.html
├── static/styles.css
├── tests/test_app.py
├── requirements.txt
├── requirements-dev.txt
├── Dockerfile
├── .dockerignore
├── Makefile                    # optional command shortcuts
├── .github/workflows/main.yml
├── Jenkinsfile
├── screenshots/              # app and local test evidence
├── docs/                     # architecture / assignment checklist
├── reports/                  # local validation output
└── README.md
```

## Evidence included

See [`screenshots/README.md`](screenshots/README.md) for the contents and limitations. The app images are browser-rendered UI previews generated from the project template and sample data, not screenshots of a live Flask server. The local test report contains the exact checks that were executed. Flask route integration tests and Docker image builds could not be executed in the isolated authoring environment; dependencies could not be downloaded and Docker is not installed. After setup, run the full suite and capture genuine GitHub Actions/Jenkins run pages from your own configured services. Do not describe these previews or local checks as successful remote CI/Jenkins runs.

## Security and deployment notes

This is an educational local/CI assignment, not a production fitness platform. Change `SECRET_KEY` before deployment, use HTTPS behind a production WSGI server, and review data-retention/privacy requirements before storing real client information. The built-in Flask development server is intended only for local assignment use.
