
pipeline {
    agent any

    triggers {
        pollSCM('H/5 * * * *')
    }

    environment {
        IMAGE_NAME = 'aceest-fitness'
        VERSION = "1.0.${BUILD_NUMBER}"
        DOCKERHUB_CREDENTIALS = 'dockerhub-credentials'
        SONARQUBE_SERVER = 'SonarQube'
        KUBERNETES_CREDENTIALS = 'kubeconfig'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements-dev.txt
                '''
            }
        }

        stage('Run Pytest') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest -v \
                        --cov=app \
                        --cov=services \
                        --cov-report=term-missing \
                        --cov-report=xml:coverage.xml \
                        --junitxml=test-results.xml
                '''
            }

            post {
                always {
                    junit allowEmptyResults: true,
                          testResults: 'test-results.xml'

                    archiveArtifacts allowEmptyArchive: true,
                                     artifacts: 'coverage.xml'
                }
            }
        }

        stage('Docker Test Build') {
            steps {
                sh '''
                    docker build \
                        --target test \
                        -t aceest-fitness-test:${BUILD_NUMBER} .
                '''
            }
        }

        stage('Run Tests Inside Docker') {
            steps {
                sh '''
                    docker run --rm \
                        -v "$WORKSPACE:/app" \
                        aceest-fitness-test:${BUILD_NUMBER} \
                        pytest -v --cov=app --cov=services \
                        --cov-report=term-missing
                '''
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv("${SONARQUBE_SERVER}") {
                    sh '''
                        sonar-scanner \
                            -Dsonar.projectVersion=${VERSION} \
                            -Dsonar.python.coverage.reportPaths=coverage.xml
                    '''
                }
            }
        }

        stage('SonarQube Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Build Production Docker Image') {
            steps {
                sh '''
                    docker build \
                        --target runtime \
                        --build-arg APP_VERSION=${VERSION} \
                        -t ${IMAGE_NAME}:${VERSION} \
                        -t ${IMAGE_NAME}:latest .
                '''
            }
        }

        stage('Push Image to Docker Hub') {
            when {
                branch 'main'
            }

            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: "${DOCKERHUB_CREDENTIALS}",
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login \
                            -u "$DOCKER_USER" --password-stdin

                        docker tag ${IMAGE_NAME}:${VERSION} \
                            ${DOCKER_USER}/${IMAGE_NAME}:${VERSION}

                        docker tag ${IMAGE_NAME}:latest \
                            ${DOCKER_USER}/${IMAGE_NAME}:latest

                        docker push ${DOCKER_USER}/${IMAGE_NAME}:${VERSION}
                        docker push ${DOCKER_USER}/${IMAGE_NAME}:latest

                        docker logout
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            when {
                branch 'main'
            }

            steps {
                withCredentials([
                    file(
                        credentialsId: "${KUBERNETES_CREDENTIALS}",
                        variable: 'KUBECONFIG'
                    ),
                    usernamePassword(
                        credentialsId: "${DOCKERHUB_CREDENTIALS}",
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {
                    sh '''
                        export KUBECONFIG="$KUBECONFIG"

                        kubectl apply -f kubernetes/

                        kubectl set image deployment/aceest-fitness \
                            aceest-fitness=${DOCKER_USER}/${IMAGE_NAME}:${VERSION}

                        kubectl rollout status deployment/aceest-fitness \
                            --timeout=120s || {
                                kubectl rollout undo deployment/aceest-fitness
                                exit 1
                            }
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "ACEest Fitness build ${VERSION} completed successfully."
        }

        failure {
            echo "Build failed. Check Jenkins console output."
        }

        always {
            sh 'docker image prune -f || true'
            cleanWs()
        }
    }
}
