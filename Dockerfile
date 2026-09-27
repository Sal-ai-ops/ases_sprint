FROM ubuntu:24.04
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.12 python3.12-venv python3-pip \
    git curl jq make build-essential \
    ca-certificates gnupg \
    && rm -rf /var/lib/apt/lists/*
RUN userdel -r ubuntu || true
RUN useradd -m -u 1000 ases
USER ases
WORKDIR /home/ases