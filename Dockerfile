# Use the official Python 3.12 image as the base image
FROM python:3.12-slim

# Maintainer information
LABEL maintainer="Valentin Castillo <valentincc94m@gmail.com>"

# Set an environment variable for the target environment
ARG target_env="local"
ENV TARGET_ENV=$target_env

# Create and set the working directory
WORKDIR /foundever-webapp

# Install necessary system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-dev \
    musl-dev \
    libxmlsec1-dev \
    pkg-config \
    libnss3 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Copy the requirements files to the container
COPY ./requirements/ /foundever-webapp/requirements/

# Install Python dependencies
RUN pip install --no-cache-dir -r /foundever-webapp/requirements/${TARGET_ENV}.txt

# Copy the application code to the working directory
COPY . /foundever-webapp

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

# Create a non-root user and adjust permissions
RUN addgroup --gid 1000 docker \
    && adduser --gid 1000 --uid 1000 --disabled-password --gecos "" --quiet docker \
    && chown -R docker:docker /foundever-webapp

# Switch to the non-root user
USER docker

# Expose the default application port
EXPOSE 8000