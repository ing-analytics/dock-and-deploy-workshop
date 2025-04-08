# Exercise 1

The goal of this exercise is to learn how to create a pod with an init container, upgrade it to a deployment and scale it.

1. Complete the configuration file `exercise.yaml` to define a pod with:
   - An init container that downloads a specific file from the web before the main container starts.
     - The init container should download the file in <https://raw.githubusercontent.com/ing-analytics/dock-and-deploy-workshop/refs/heads/main/assets/ex_static_site.html>
     into a volume mounted in the directory `/usr/share/nginx/html/index.html`
   - A main container that serves a simple web application with `nginx`
2. Convert the pod into a deployment
   - Modify the configuration to turn the pod into a deployment
3. Scale the deployment
   - Use `kubectl scale` to increase and decrease the number of replicas.
   - Observe how Kubernetes handles the scheduling of the pods.

## References

- [Kubernetes Pods](https://kubernetes.io/docs/concepts/workloads/pods/)
- [Init Containers](https://kubernetes.io/docs/concepts/workloads/pods/init-containers/)
- [Kubernetes Volumes](https://kubernetes.io/docs/concepts/storage/volumes/)
- [wget command](https://www.gnu.org/software/wget/manual/wget.html#Examples)
- [kubectl port-forward command](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_port-forward/)
- [Kubernetes deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#creating-a-deployment)
- [kubectl scale command](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_scale/)
