# Assignment deliverables checklist

| Brief requirement | Project file(s) | Verification status in this authoring environment |
|---|---|---|
| Flask fitness management app | `app.py`, `services.py`, `templates/index.html`, `static/styles.css` | Python syntax and Jinja template render checked; live Flask route tests remain to run after dependency installation. |
| Version control strategy | Commands in `README.md` | Meaningful commit messages are documented; initialize/push using your own GitHub account. |
| Pytest test suite | `tests/test_services.py`, `tests/test_app.py` | 18 pure business-rule tests passed. Flask route tests are included but were not runnable here because Flask could not be installed. |
| Docker image | `Dockerfile`, `.dockerignore` | Multi-stage runtime/test build defined; not built locally because Docker is unavailable. |
| Jenkins BUILD and quality gate | `Jenkinsfile` | Declarative pipeline defined; must run on a Jenkins agent with Python, package access and Docker. |
| GitHub Actions on push/PR | `.github/workflows/main.yml` | Workflow definition included; a genuine remote run is only available after pushing to GitHub. |
| Setup and test documentation | `README.md` | Includes Python, tests, Docker, GitHub Actions and Jenkins instructions. |
| Screenshot/evidence request | `screenshots/`, `reports/local-validation.txt` | UI previews and transparent local validation evidence included; they are not presented as remote CI screenshots. |

## Before final submission

- Create a **public** GitHub repository and push this project.
- Open **Actions** and save a screenshot of the successful `ACEest CI` run after it passes.
- Configure the Jenkins Pipeline from the repository's `Jenkinsfile`, run it, and save a screenshot of the successful build stages.
- If any step fails, fix it and repeat the pipeline before submitting.
