# Shortcuts for the Docker and Kubernetes demos. Run `make` (or `make help`) to list them.
#
# All targets are .PHONY: they run commands and don't create files, so make
# should always run them, even if a file with the same name exists.

# Command used to run Docker Compose. If you only have the newer
# `docker compose` (without the dash), override it like this:
#   make docker-demo-2-up DOCKER_COMPOSE_BIN="docker compose"
DOCKER_COMPOSE_BIN := docker-compose

DOCKER_DEMO_1 := docker/demos/demo-1
DOCKER_DEMO_2 := docker/demos/demo-2

.DEFAULT_GOAL := help

.PHONY: help
help: ## Show this help
	@grep -E '^[a-zA-Z0-9_-]+:.*## ' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*## "}; {printf "  %-28s %s\n", $$1, $$2}'

.PHONY: lint
lint: ## Lint all Dockerfiles with hadolint
	hadolint $(DOCKER_DEMO_1)/Dockerfile $(DOCKER_DEMO_2)/Dockerfile \
		docker/exercises/flask_app/web/Dockerfile

# --- Docker demo 1: FastAPI app + PostgreSQL --------------------------------

.PHONY: docker-demo-1-build
docker-demo-1-build: ## Build the FastAPI image (my-api:v1)
	docker build -t my-api:v1 $(DOCKER_DEMO_1)

.PHONY: docker-demo-1-run
docker-demo-1-run: docker-demo-1-build ## Run only the FastAPI app on http://localhost:8000/hello (Ctrl+C stops it)
	docker run --rm -it -p 8000:8000 my-api:v1

.PHONY: docker-demo-1-up
docker-demo-1-up: docker-demo-1-build ## Start FastAPI + PostgreSQL on http://localhost:8000/db-health
	@# The leading `-` tells make to continue if the network already exists
	-docker network create demo-1
	docker run -d --name demo-1-db --network demo-1 \
		-e POSTGRES_USER=workshop -e POSTGRES_PASSWORD=workshop \
		-e POSTGRES_DB=workshop \
		postgres:17
	docker run -d --name demo-1-api --network demo-1 -p 8000:8000 \
		-e SERVER=demo-1-db:5432 -e DATABASE=workshop \
		-e USERNAME=workshop -e PASSWORD=workshop \
		my-api:v1

.PHONY: docker-demo-1-down
docker-demo-1-down: ## Stop and remove FastAPI + PostgreSQL
	-docker rm -f demo-1-api demo-1-db
	-docker network rm demo-1

# --- Docker demo 2: Flask + Redis with Docker Compose ---------------------

.PHONY: docker-demo-2-up
docker-demo-2-up: ## Start Flask + Redis on http://localhost:8000
	$(DOCKER_COMPOSE_BIN) -f $(DOCKER_DEMO_2)/compose.yaml up -d --build

.PHONY: docker-demo-2-logs
docker-demo-2-logs: ## Follow the logs of Flask + Redis (Ctrl+C stops following)
	$(DOCKER_COMPOSE_BIN) -f $(DOCKER_DEMO_2)/compose.yaml logs -f

.PHONY: docker-demo-2-down
docker-demo-2-down: ## Stop and remove Flask + Redis
	$(DOCKER_COMPOSE_BIN) -f $(DOCKER_DEMO_2)/compose.yaml down

# --- Kubernetes demo 2: counter API with a volume and a Job ----------------
#
# The image name must match `image:` in $(K8S_DEMO_2)/1-deploy.yaml. The
# manifest uses imagePullPolicy: IfNotPresent, so the cluster uses the image
# you built locally instead of pulling it from a registry.
#
# Docker Desktop's Kubernetes sees locally built images directly. kind and
# minikube run their own container runtime: load the image into the cluster
# after building it (k8s-demo-2-load-kind / k8s-demo-2-load-minikube).

K8S_DEMO_2 := kubernetes/demos/demo-2
COUNTER_API_IMAGE := counter-api:v1

.PHONY: k8s-demo-2-build
k8s-demo-2-build: ## Build the counter API image (counter-api:v1)
	docker build -t $(COUNTER_API_IMAGE) $(K8S_DEMO_2)

.PHONY: k8s-demo-2-load-kind
k8s-demo-2-load-kind: k8s-demo-2-build ## Build the counter API image and load it into kind
	kind load docker-image $(COUNTER_API_IMAGE)

.PHONY: k8s-demo-2-load-minikube
k8s-demo-2-load-minikube: k8s-demo-2-build ## Build the counter API image and load it into minikube
	minikube image load $(COUNTER_API_IMAGE)

.PHONY: k8s-demo-2-up
k8s-demo-2-up: ## Deploy the counter API and its Service (build/load the image first)
	kubectl apply -f $(K8S_DEMO_2)/1-deploy.yaml

.PHONY: k8s-demo-2-job
k8s-demo-2-job: ## Run the Job that increments the counter 3 times, then show its output
	@# A finished Job can't be re-run: delete the old one first
	-kubectl delete job api-request-job --ignore-not-found
	kubectl apply -f $(K8S_DEMO_2)/2-job.yaml
	kubectl wait --for=condition=complete --timeout=60s job/api-request-job
	kubectl logs job/api-request-job

.PHONY: k8s-demo-2-down
k8s-demo-2-down: ## Remove the counter API, its Service and the Job
	-kubectl delete -f $(K8S_DEMO_2)/2-job.yaml --ignore-not-found
	-kubectl delete -f $(K8S_DEMO_2)/1-deploy.yaml --ignore-not-found
