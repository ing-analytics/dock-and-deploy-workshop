# Exercise 1

The goal of this exercise is to learn how to create a pod with an init container, upgrade it to a deployment and scale it.

1. Create a configuration file `exercise.yaml` defining a pod with:
   - An init container that wait for a specific file to be available before the main container starts.
   - A main container that serves a simple web application
2. Convert the pod into a deployment
   - Modify the configuration to turn the pod into a deployment
3. Scale the deployment
   - Use `kubectl scale` to increase and decrease the number of replicas.
   - Observe how Kubernetes handles the scheduling of the pods.
