# Demo API

This is a simple API using FastAPI and PostgreSQL for workshop/demo use.

## About the API

### Environment Variables

| Variable | Description         | Sample Value   |
|----------|---------------------|----------------|
| APP_HOST | hostname of the app | 0.0.0.0        |
| APP_PORT | port of the app     | 8000           |
| SERVER   | database server     | localhost:5432 |
| DATABASE | database            | workshop       |
| USERNAME | database username   | workshop       |
| PASSWORD | database password   | workshop       |

The database is [PostgreSQL](https://www.postgresql.org/). The app connects on the first
request that needs the database, so it does not matter whether the app or the database starts first.

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

### Running the API with PostgreSQL

The database endpoints need a PostgreSQL database. We run it in a second container.
Both containers join the same Docker network, so the API can reach the database
by its container name (`demo-1-db`).

```sh
# 1. Create a network for the two containers
docker network create demo-1

# 2. Start PostgreSQL
docker run -d --name demo-1-db --network demo-1 \
  -e POSTGRES_USER=workshop -e POSTGRES_PASSWORD=workshop \
  -e POSTGRES_DB=workshop \
  postgres:17

# 3. Start the API; SERVER=demo-1-db:5432 points to the container named demo-1-db
docker run -d --name demo-1-api --network demo-1 -p 8000:8000 \
  -e SERVER=demo-1-db:5432 -e DATABASE=workshop \
  -e USERNAME=workshop -e PASSWORD=workshop \
  my-api:v1

# 4. Try it
curl http://localhost:8000/db-health
curl -X POST http://localhost:8000/current-user -d '{"username":"workshop_user"}' -H "Content-Type: application/json"
curl http://localhost:8000/current-user

# 5. Clean up
docker rm -f demo-1-api demo-1-db
docker network rm demo-1
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