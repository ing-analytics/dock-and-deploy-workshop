FROM python:3.12

RUN pip install "fastapi[standard]"
COPY app.py /app/app.py

WORKDIR /app
ENTRYPOINT [ "fastapi", "run", "app.py", "--host", "0.0.0.0", "--port", "8080" ]
