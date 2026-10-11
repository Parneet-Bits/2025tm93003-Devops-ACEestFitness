# CI/CD architecture

```text
Developer change
      |
      v
   Git push / Pull request
      |
      +-------------------- GitHub Actions --------------------+
      | Checkout -> Python compile -> pytest -> Docker runtime  |
      |                                  -> Docker test target  |
      +---------------------------------------------------------+
      |
      +--------------------- Jenkins Pipeline ------------------+
        Checkout -> virtualenv/dependency build -> compile
                 -> pytest/JUnit report -> Docker runtime build
                 -> Docker test-target quality gate

Local Flask app -> SQLite database -> /healthz health endpoint
```

GitHub Actions provides an automated per-push/per-PR build and test gate. Jenkins is configured as a second pipeline using the same repository and Dockerfile, with test results published in JUnit XML format. Both pipelines deliberately fail if compilation, unit tests or Docker builds fail. The app itself runs without a remote database or third-party runtime service.
