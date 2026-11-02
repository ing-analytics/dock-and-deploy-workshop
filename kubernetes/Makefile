# Shortcuts for the Kubernetes demos. Run `make` (or `make help`) in this
# directory to list them.
#
# All targets are .PHONY: they run commands and don't create files, so make
# should always run them, even if a file with the same name exists.

K8S_DEMO_1 := demos/demo-1
K8S_DEMO_2 := demos/demo-2

.DEFAULT_GOAL := help

.PHONY: help
help: ## Show this help
	@grep -E '^[a-zA-Z0-9_-]+:.*## ' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*## "}; {printf "  %-28s %s\n", $$1, $$2}'

.PHONY: lint
lint: ## Lint the Dockerfile of demo 2 with hadolint
	hadolint $(K8S_DEMO_2)/Dockerfile

# --- Kubernetes demo 1: pod, init container, deployment, service ----------

.PHONY: k8s-demo-1-pod
k8s-demo-1-pod: ## Create a single nginx pod
	kubectl apply -f $(K8S_DEMO_1)/1-pod.yaml

.PHONY: k8s-demo-1-pod-with-init
k8s-demo-1-pod-with-init: ## Replace the pod with one that has an init container
	kubectl delete pod my-pod --ignore-not-found
	kubectl apply -f $(K8S_DEMO_1)/2-pod-with-init.yaml

.PHONY: k8s-demo-1-deployment
k8s-demo-1-deployment: ## Create the deployment (2 pods) and its service
	kubectl apply -f $(K8S_DEMO_1)/3-deployment.yaml -f $(K8S_DEMO_1)/service.yaml

.PHONY: k8s-demo-1-port-forward
k8s-demo-1-port-forward: ## Open the service on http://localhost:8080 (Ctrl+C stops it)
	kubectl port-forward service/nginx-service 8080:80

.PHONY: k8s-demo-1-clean
k8s-demo-1-clean: ## Delete everything from Kubernetes demo 1
	kubectl delete pod my-pod --ignore-not-found
	kubectl delete -f $(K8S_DEMO_1)/3-deployment.yaml -f $(K8S_DEMO_1)/service.yaml --ignore-not-found

# --- Kubernetes demo 2: counter API with a volume and a job ----------------
# Note: demo 1 and demo 2 both name their deployment `my-deployment`,
# so run `make k8s-demo-1-clean` before deploying demo 2.

.PHONY: k8s-demo-2-build
k8s-demo-2-build: ## Build the counter API image (counter-api:v1)
	docker build -t counter-api:v1 $(K8S_DEMO_2)
	@echo "Using kind? Also run: kind load docker-image counter-api:v1"

.PHONY: k8s-demo-2-deploy
k8s-demo-2-deploy: ## Deploy the counter API and its service
	kubectl apply -f $(K8S_DEMO_2)/1-deploy.yaml

.PHONY: k8s-demo-2-job
k8s-demo-2-job: ## Run a job that increments the counter 3 times, then show its output
	kubectl delete job api-request-job --ignore-not-found
	kubectl apply -f $(K8S_DEMO_2)/2-job.yaml
	kubectl wait --for=condition=complete job/api-request-job --timeout=60s
	kubectl logs job/api-request-job

.PHONY: k8s-demo-2-port-forward
k8s-demo-2-port-forward: ## Open the counter API on http://localhost:8080/counter (Ctrl+C stops it)
	kubectl port-forward service/counter-service 8080:80

.PHONY: k8s-demo-2-clean
k8s-demo-2-clean: ## Delete everything from Kubernetes demo 2
	kubectl delete -f $(K8S_DEMO_2)/2-job.yaml -f $(K8S_DEMO_2)/1-deploy.yaml --ignore-not-found
