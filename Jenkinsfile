pipeline {
    agent any

    environment {
        APP_ENV = 'ci'
        IMAGE = 'system-health-dashboard'
        APP_VERSION = "1.0.${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install') {
            steps {
                sh '''
                    docker run --rm -v "$PWD":/app -w /app python:3.12-slim \
                      sh -c "python -m venv .venv && .venv/bin/pip install -r requirements.txt"
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    docker run --rm -v "$PWD":/app -w /app python:3.12-slim \
                      sh -c ".venv/bin/pytest -q"
                '''
            }
        }

        stage('Build') {
            steps {
                sh 'docker build -t ${IMAGE}:${BUILD_NUMBER} --build-arg APP_VERSION=${APP_VERSION} .'
            }
        }

        stage('Tag') {
            steps {
                sh 'docker tag ${IMAGE}:${BUILD_NUMBER} ${IMAGE}:1.0.${BUILD_NUMBER}'
                sh 'docker images ${IMAGE}'
            }
        }

        stage('Health check') {
            steps {
                sh '''
                    cid=$(docker run -d --rm -e APP_ENV=ci -e APP_VERSION=${APP_VERSION} ${IMAGE}:${BUILD_NUMBER})
                    ip=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' "$cid")
                    i=0
                    until curl -fsS "http://${ip}:5000/health"; do
                      i=$((i+1))
                      if [ "$i" -gt 15 ]; then
                        docker logs "$cid" || true
                        docker stop "$cid" || true
                        exit 1
                      fi
                      sleep 2
                    done
                    curl -fsS "http://${ip}:5000/ready"
                    curl -fsS "http://${ip}:5000/slo"
                    curl -fsS "http://${ip}:5000/info"
                    docker stop "$cid"
                '''
            }
        }
    }

    post {
        always {
            sh 'docker ps -a --filter name=system-health || true'
        }
    }
}
