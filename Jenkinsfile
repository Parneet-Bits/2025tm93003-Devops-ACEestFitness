pipeline {
    agent any

    options {
        skipDefaultCheckout(true)
        timestamps()
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                sh 'git log -1 --oneline'
            }
        }

        stage('Clean Python Build') {
            steps {
                sh '''
                    set -eu
                    python3 --version
                    rm -rf .venv
                    python3 -m venv .venv
                    . .venv/bin/activate
                    python -m pip install --upgrade pip
                    python -m pip install -r requirements.txt -r requirements-dev.txt
                    python -m compileall -q app.py services.py tests
                '''
            }
        }

        stage('Unit Tests') {
            steps {
                sh '''
                    set -eu
                    . .venv/bin/activate
                    mkdir -p reports
                    python -m pytest -q --junitxml=reports/pytest-results.xml
                '''
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'reports/pytest-results.xml'
                    archiveArtifacts allowEmptyArchive: true, artifacts: 'reports/pytest-results.xml'
                }
            }
        }

        stage('Docker Production Build') {
            steps {
                sh 'docker build --pull --target runtime --tag aceest-fitness:${BUILD_NUMBER} .'
            }
        }

        stage('Containerized Test Quality Gate') {
            steps {
                sh 'docker build --pull --target test --tag aceest-fitness-test:${BUILD_NUMBER} .'
            }
        }
    }

    post {
        success {
            echo 'ACEest build, unit tests, production image build and container test quality gate passed.'
        }
        failure {
            echo 'Build or quality gate failed. Review the failing stage and test report.'
        }
        always {
            cleanWs(deleteDirs: true, notFailBuild: true)
        }
    }
}
