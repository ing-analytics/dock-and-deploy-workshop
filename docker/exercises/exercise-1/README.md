# Demo APP

This is a simple app using Streamlit for workshop and demo use.

## About the API

## Running the APP

```sh
streamlit run app.py
```

### Building the Image

```sh
docker build -t my-streamlit-app .
```

### Running the Docker Container

```sh
docker run -d -p 8501:8501 my-streamlit-app
```

### Check the application

Open localhost:8051 to see the webapp.