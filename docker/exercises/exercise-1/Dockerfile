FROM python:3.11-bullseye

COPY requirements.txt /tmp

RUN pip install -r "/tmp/requirements.txt"

COPY . /app

WORKDIR /app

CMD ["streamlit", "run", "app.py"]
