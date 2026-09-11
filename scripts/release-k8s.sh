#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

IMAGE=system-health-dashboard:1.0.0
CLUSTER=sre-prep
KCFG=/tmp/sre-prep.kubeconfig

docker build -t "$IMAGE" --build-arg APP_VERSION=1.0.0 .
kind load docker-image "$IMAGE" --name "$CLUSTER"
kind get kubeconfig --name "$CLUSTER" > "$KCFG"
kubectl --kubeconfig "$KCFG" apply -f k8s/configmap.yaml -f k8s/deployment.yaml -f k8s/service.yaml
kubectl --kubeconfig "$KCFG" -n student-11 rollout status deploy/health-dashboard --timeout=90s
kubectl --kubeconfig "$KCFG" -n student-11 get pods,svc
