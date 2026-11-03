# Exercise 2

The goal of this exercise is to understand how to expose applications using services and run batch processing with jobs.

## Setup

Run these commands from this directory (`kubernetes/exercises/exercise-2`):

```sh
kubectl apply -f pvc.yaml
# The deployment copies the initial data from this ConfigMap into the volume
kubectl create configmap data-config --from-file=initial_data/
kubectl apply -f deployment.yaml
```

Without the `data-config` ConfigMap the pod stays in `ContainerCreating`
(`kubectl describe pod` shows `configmap "data-config" not found`).

## Steps

1. Check the deployment for a website.
2. Expose the application via a Service
    - Define a `NodePort` Service to allow communication
    - Verify accessibility using `kubectl port-forward`
3. Create a job
   - Write a YAML file for a Job that:
     - Runs a simple batch task that downloads the data
     - Completes after a single execution
4. Convert the job into a Cron Job
   - Modify the job to run periodically (eg. every 1 minutes)
   - Observe how Kubernetes schedules and runs the job.

## Good to know

- Every time the site pod starts, its `copy-data-files` init container copies
  the ConfigMap data into the volume again. This overwrites whatever your
  job wrote, so after a pod restart you see the initial data until the job
  runs again.
- The volume is `ReadWriteOnce`: only pods on the same node can mount it at
  the same time. On a single-node cluster (Docker Desktop, Killercoda) the
  site and the job can share it. On a multi-node cluster the job pod can get
  stuck in `ContainerCreating` if it is scheduled on a different node.
- `kubectl port-forward` connects to the Service directly, so it works for
  any Service type. To see what `NodePort` adds, open
  `http://<node-ip>:<node-port>` instead (`kubectl get svc` shows the port).
