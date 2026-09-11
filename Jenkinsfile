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
                    set -e
                    mkdir -p .tools
                    if [ ! -x .tools/uv ]; then
                      curl -fsSL -o uv.tgz \
                        https://github.com/astral-sh/uv/releases/download/0.6.17/uv-x86_64-unknown-linux-gnu.tar.gz
                      tar -xzf uv.tgz -C .tools --strip-components=1
                    fi
                    export PATH="$PWD/.tools:$PATH"
                    uv python install 3.12
                    uv venv .venv
                    uv pip install --python .venv/bin/python -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    set -e
                    export PATH="$PWD/.tools:$PATH"
                    .venv/bin/python -m pytest -q
                '''
            }
        }

        stage('Build') {
            steps {
                sh '''
                    set -e
                    if command -v docker >/dev/null 2>&1; then
                      docker build -t ${IMAGE}:${BUILD_NUMBER} --build-arg APP_VERSION=${APP_VERSION} .
                    else
                      echo "docker not on this Jenkins agent"
                      echo "tag ${IMAGE}:${BUILD_NUMBER}" > image-tag.txt
                      tar -czf ${IMAGE}-${BUILD_NUMBER}.tar.gz Dockerfile app.py dashboard requirements.txt
                      ls -l ${IMAGE}-${BUILD_NUMBER}.tar.gz
                    fi
                '''
            }
        }

        stage('Tag') {
            steps {
                sh '''
                    set -e
                    if command -v docker >/dev/null 2>&1; then
                      docker tag ${IMAGE}:${BUILD_NUMBER} ${IMAGE}:1.0.${BUILD_NUMBER}
                      docker images ${IMAGE}
                    else
                      echo "${IMAGE}:1.0.${BUILD_NUMBER}" >> image-tag.txt
                      cat image-tag.txt
                    fi
                '''
            }
        }

        stage('Publish') {
            steps {
                sh '''
                    set -e
                    if command -v docker >/dev/null 2>&1; then
                      echo "no container registry on this agent"
                      echo "image ${IMAGE}:1.0.${BUILD_NUMBER} stays local"
                      docker images ${IMAGE} || true
                    else
                      echo "publish skipped: this Jenkins agent has no docker"
                      echo "workstation path: docker build + kind load system-health-dashboard:1.0.0"
                    fi
                '''
            }
        }

        stage('Health check') {
            steps {
                sh '''
                    set -e
                    if command -v docker >/dev/null 2>&1; then
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
                      docker stop "$cid"
                    else
                      export PATH="$PWD/.tools:$PATH"
                      .venv/bin/gunicorn -b 127.0.0.1:5005 app:app > gunicorn.log 2>&1 &
                      echo $! > gunicorn.pid
                      i=0
                      until curl -fsS http://127.0.0.1:5005/health; do
                        i=$((i+1))
                        if [ "$i" -gt 20 ]; then
                          cat gunicorn.log || true
                          kill $(cat gunicorn.pid) || true
                          exit 1
                        fi
                        sleep 2
                      done
                      curl -fsS http://127.0.0.1:5005/ready
                      curl -fsS http://127.0.0.1:5005/slo
                      kill $(cat gunicorn.pid) || true
                    fi
                '''
            }
        }
    }

    post {
        always {
            sh 'command -v docker >/dev/null 2>&1 && docker ps -a --filter name=system-health || true'
        }
    }
}
