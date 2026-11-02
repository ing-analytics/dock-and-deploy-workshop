# Exercise 1: Containerize a Streamlit App

This is a simple app using [Streamlit](https://streamlit.io/) for workshop and demo use.
It shows a table with the participants from `data.csv`.

## Your task

Create a [Dockerfile](https://docs.docker.com/build/concepts/dockerfile/) to containerize the Streamlit app.

### Hints

Your Dockerfile needs to:

- start from a Python base image, for example `python:3.14-slim`
- install the packages from `requirements.txt`
- copy `app.py` and `data.csv` into the image
- document that Streamlit listens on port `8501`
- start the app with this command:

  ```sh
  streamlit run app.py --server.address=0.0.0.0 --browser.gatherUsageStats=false
  ```

  `--server.address=0.0.0.0` makes the app reachable from outside the container.
  `--browser.gatherUsageStats=false` stops Streamlit from sending usage statistics.

### Building the Image

```sh
docker build -t my-streamlit-app .
```

### Running the Docker Container

```sh
docker run -d -p 8501:8501 my-streamlit-app
```

### Check the application

Open http://localhost:8501 to see the webapp.

### Stopping the container

`-d` runs the container in the background. To stop it:

```sh
docker ps                      # find the CONTAINER ID
docker stop <CONTAINER ID>
```

## Bonus: environment variables

The app reads the environment variable `N_PARTICIPANTS` to decide how many
participants it shows (default: 5). Start the container with only 3:

```sh
docker run -d -p 8501:8501 -e N_PARTICIPANTS=3 my-streamlit-app
```
