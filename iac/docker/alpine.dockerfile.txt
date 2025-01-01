#
# Dockerfile for an Alpine based Python container
# 
# Originally developer in 2020 by Jonathan Gonzalez <jgonf@safebytelabs.com>
# Licensed under the Mozilla Public License 2.0
#

FROM python:3.12.2-alpine3.19
LABEL maintainer="Jonathan Gonzalez <jgonf@safebytelabs.com>"
ARG GIT_BRANCH

ENV RUN_DEPENDENCIES="python3 py3-pip curl"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONFAULTHANDLER=1

# Let service stop gracefully
STOPSIGNAL SIGQUIT

# Install system dependencies and Poetry
RUN apk add --no-cache $RUN_DEPENDENCIES \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && rm -rf /root/.cache               \
    && rm -rf /var/cache/apk/*           \
    && find /                            \
    \( -type d -a -name test -o -name tests \) \
    -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
    -exec rm -rf '{}' + \
    && ls -tr /opt

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Set the working directory
WORKDIR /opt/app

# Copy project files into /opt/app
COPY ./pyproject.toml ./poetry.lock ./

# Install dependencies
RUN poetry install --no-root --only main \
    && poetry run gunicorn --version

# Copy and configure entrypoint script
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Copy the application source code
COPY ./src/mypkg/ .

# Default port for Gunicorn
ENV GUNIPORT=8000

# Use the script as the entrypoint
ENTRYPOINT ["sh", "/usr/local/bin/entrypoint.sh"]