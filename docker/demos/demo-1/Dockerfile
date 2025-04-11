FROM python:3.11-bullseye

ENV APP_HOST=0.0.0.0
ENV APP_PORT=8000

WORKDIR /app
ENV PYTHONPATH=/app

# install mssql and unixodbc
RUN apt-get update && \
    apt-get install gnupg -y && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install msodbcsql18 unixodbc-dev -y

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY *.py ./

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
