# Demo API

This is a simple API using FastAPI for workshop/demo use.

## About the API

### Environment Variables

| Variable | Description         | Sample Value                    |
|----------|---------------------|---------------------------------|
| APP_HOST | hostname of the app | 0.0.0.0                         |
| APP_PORT | port of the app     | 8000                            |
| SERVER   | database server     | localhost:1433                  |
| DATABASE | database            |                                 |
| USERNAME | database username   |                                 |
| PASSWORD | database password   |                                 |
| DRIVER   | database driver     | {ODBC Driver 18 for SQL Server} |


### Endpoints

| Endpoint      | Method | Description               |
|---------------|--------|---------------------------|
| /healthz      | GET    | health check              |
| /hello        | GET    | hello world               |
| /db-health    | GET    | checks if DB is connected |
| /current-user | GET    | gets current user         |
| /current-user | POST   | update current user       |

Sample Post Request:

```curl
curl -X POST http://localhost:8000/current-user -d '{"username":"workshop_user"}' -H "Content-Type: application/json"
```

## Running the API Locally

Install requirements:

```sh
pip install -r requirements.txt
```

```sh
python main.py
```

### Building the Image

```sh
docker build -t my-api:v1 .
```

### Running the Container

```sh
docker run --rm -p 8000:8000 my-api:v1
```

Then open http://localhost:8000/hello.

To use the database endpoints, pass the connection settings as environment variables:

```sh
docker run --rm -p 8000:8000 \
  -e SERVER=my-db-server:1433 \
  -e DATABASE=my_db \
  -e USERNAME=my_user \
  -e PASSWORD=my_password \
  my-api:v1
```

### Deploying to Kubernetes

If using kind locally, run this first:

```sh
kind load docker-image my-api:v1
```

Then deploy:

```sh
kubectl create deployment my-app --image=my-api:v1
```