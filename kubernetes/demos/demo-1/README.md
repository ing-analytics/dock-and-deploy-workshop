# Demo 1 - Learn how to work with Pods and Deployments

# Kubernetes Exercise

Uses the [Demo API](/docker/exercise/README.md)

1. Create a “mssql” statefulset for Microsoft SQL Server 
(hint: need to make updates to `1-db-sts.yaml`)​

   - Find what’s missing using `kubectl describe`
   - If you need to re-apply sts yaml file, you need to delete them first​

1. Create a “mssql” service
(don’t update anything `2-db-svc.yaml`, changes here are intended)​

1. Run the command to check which pods are connected to the svc​

    ```sh
    kubectl get ep mssql -o=jsonpath='{.subsets[*].addresses[*].ip}' | tr ' ' '\n' | xargs -I % kubectl get pods -o=name --field-selector=status.podIP=%​
    ```
    If everything works fine, you should see: `pod/mssql-0​`

1. Connect the “mssql” service to the “exercise” deployment
(hint: need to update server and password environment variables in 3-api-deploy.yaml)

   - to get server: `kubectl exec -it mssql-0 sh then run dnsdomainname​`

1. Port-forward on the “exercise” deployment pod​

1. You can update username using curl for /current-user (POST) endpoint (sample in [API README.md](https://github.com/yugladys/it-class-workshop/blob/main/day-1/api/README.md))

1. Check if http://localhost:8080/current-user (GET) if insert is successful
