# Exercise 2

The goal of this exercise is to understand how to expose applications using services and run batch processing with jobs.

1. Check the deployment for the streamlit application on `app.py`
2. Expose the application via a Service
    - Define a `NodePort` Service to allow communication
    - Verify accessibility using `kubectl port-forward`
3. Create a job
   - Write a YAML file for a Job that:
     - Runs a simple batch task that downloads the data 
     - Completes after a single execution
4. Convert the job into a Cron Job
   - Modify the job to run periodically (eg. every 5 minutes)
   - Observe how Kubernetes schedules and runs the job.
