# Kubernetes

- `demos/`: what the presenter shows live
- `exercises/`: hands-on exercises, each with its own README
- `samples/`: reference manifests to copy from

## Demo 1: Pod, init container, Deployment

Apply the files in order: `1-pod.yaml`, `2-pod-with-init.yaml`, `3-deployment.yaml`, plus `service.yaml`.

- `1-pod.yaml` and `2-pod-with-init.yaml` both create a Pod called `my-pod`.
  You can't add an init container to a Pod that already exists, so delete the
  first one before applying the second:
  `kubectl delete pod my-pod`.
- Delete `my-pod` before applying `3-deployment.yaml` too. The Deployment
  selects pods by the label `run: kubernetes-demo`, which `my-pod` also has.
  If `my-pod` is still running, the Deployment takes it over and creates only
  one new pod instead of two.

## Demo 2: Counter API with a volume and a Job

The image `counter-api:v1` is built from `demos/demo-2/Dockerfile`.
It isn't published to any registry, so build it before deploying. From the
repository root:

```sh
make k8s-demo-2-build      # docker build -t counter-api:v1 kubernetes/demos/demo-2
make k8s-demo-2-up         # deploy the counter API and its Service
make k8s-demo-2-job        # run the Job (increments the counter 3 times), show its logs
make k8s-demo-2-down       # clean up
```

On Docker Desktop, Kubernetes can use locally built images directly. kind and
minikube can't: build and load the image with `make k8s-demo-2-load-kind`
or `make k8s-demo-2-load-minikube` instead of `make k8s-demo-2-build`.

If you change the tag, change it in both the `Makefile` (`COUNTER_API_IMAGE`)
and `demos/demo-2/1-deploy.yaml` (`image:`).

Tear down demo 1 before starting demo 2. Both demos use the Deployment
name `my-deployment`, the Service name `nginx-service` and the label
`run: kubernetes-demo`. If you run them together, they overwrite each other
and the Service sends traffic to pods from both demos.

The counter is kept in an `emptyDir` volume. It survives a container
restart but is lost when the pod is deleted.

## Samples

- `config.env` is an env file, not a manifest. Use it to create a ConfigMap
  or Secret:
  `kubectl create configmap sample-config --from-env-file=kubernetes/samples/config.env`
- `sample-deploy.yaml`, `sample-deploy-multi.yaml` and
  `sample-deploy-scale.yaml` are variants of the same Deployment
  (`sample-deploy`). Applying one replaces the previous one.
- `sample-sts.yaml` needs a default StorageClass for its volume claims. Its
  `serviceName: sample-sts` refers to a headless Service that isn't included.
  The pods still start, but their per-pod DNS names
  (`sample-sts-0.sample-sts`) only resolve once you create that Service
  (`clusterIP: None`, selector `app: sample-sts`).
