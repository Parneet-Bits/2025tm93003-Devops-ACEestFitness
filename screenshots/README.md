# Screenshot and verification evidence

These images are supplementary visuals; the assignment brief itself specifies the public repository, Flask source, pytest suite, Dockerfile, GitHub Actions workflow and README.

- `01-dashboard-preview.png` — browser-rendered dashboard template preview in its empty state.
- `02-client-added-preview.png` — browser-rendered template preview with a sample client and success message.
- `03-local-validation.png` — designed summary of what was and was not executable in the authoring environment. The exact command output is in `reports/local-validation.txt`.

**Evidence limitation:** the first two images are template previews rendered with sample data, not live-server screenshots. The environment did not have Flask installed, outbound package downloads were blocked, and Docker was not installed. The standalone business-rule suite and Python syntax checks passed, but the Flask route suite and Docker build are not claimed as passed. GitHub Actions and Jenkins proof must be captured after this repository is pushed to GitHub and the corresponding service is configured.
