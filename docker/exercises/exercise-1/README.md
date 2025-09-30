# Demo APP

This is a simple app using Streamlit for workshop and demo use.

## Exercise 1

Create a [Dockerfile](https://docs.docker.com/build/concepts/dockerfile/) to containerize the Streamlit app.

### Building the Image

```sh
docker build -t my-streamlit-app .
```

### Running the Docker Container

```sh
docker run -d -p 8501:8501 my-streamlit-app
```

### Check the application

Open http://localhost:8051 to see the webapp.
