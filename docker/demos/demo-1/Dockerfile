# python:3.14-slim is based on Debian 13 (trixie)
FROM python:3.14-slim

# PYTHONDONTWRITEBYTECODE: don't write .pyc files into the image
# PYTHONUNBUFFERED: print logs immediately (no buffering), so `docker logs` shows them
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_HOST=0.0.0.0 \
    APP_PORT=8000

# Install the Microsoft ODBC driver for SQL Server (msodbcsql18).
# We first install Microsoft's repo config package
# (per https://learn.microsoft.com/en-us/linux/packages), which adds their
# package repository and signing key, then install the driver from it.
#
# `set -eux` makes this multi-command RUN step safer and easier to debug:
#   -e  exit immediately if any command fails, so the build stops at the
#       real error instead of carrying on and producing a broken image
#   -u  treat unset variables as an error (catches typos like ${VERSOIN_ID})
#   -x  print each command before running it, so the build log shows
#       exactly which step was executing when something went wrong
# Commands are separated with `;` instead of `&&` because -e already
# stops on the first failure.
#
# We don't pin apt package versions (hadolint rule DL3008): old versions are
# removed from the Debian repos quickly, which would break the build.
# hadolint ignore=DL3008
RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends curl ca-certificates; \
    . /etc/os-release; \
    curl -sSL -o /tmp/packages-microsoft-prod.deb \
        "https://packages.microsoft.com/config/${ID}/${VERSION_ID}/packages-microsoft-prod.deb"; \
    apt-get install -y --no-install-recommends /tmp/packages-microsoft-prod.deb; \
    rm /tmp/packages-microsoft-prod.deb; \
    apt-get update; \
    ACCEPT_EULA=Y apt-get install -y --no-install-recommends msodbcsql18 unixodbc; \
    # Remove curl again, but without --auto-remove: Microsoft advises against
    # it, because it can also remove packages the ODBC driver needs.
    apt-get purge -y curl; \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements.txt on its own first: Docker caches this layer, so
# dependencies are only reinstalled when requirements.txt changes.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY *.py ./

# Run as a non-root user
RUN groupadd --gid 1000 pokemon \
    && useradd --uid 1000 --gid pokemon --create-home pikachu
USER pikachu

# Documents the port the app listens on (publish it with `docker run -p`)
EXPOSE 8000

# main.py reads APP_HOST and APP_PORT and starts uvicorn
CMD ["python", "main.py"]
