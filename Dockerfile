FROM python:3.11.3-slim

RUN apt-get update && apt-get install -y --no-install-recommends build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir /freelancer_platform

WORKDIR /freelancer_platform

COPY ./src ./src
COPY ./Pipfile ./Pipfile
COPY ./Pipfile.lock ./Pipfile.lock
COPY ./commands ./commands


RUN python -m pip install --upgrade pip
RUN pip install pipenv

ENV PIPENV_VENV_IN_PROJECT=1
ARG PIPENV_DEV=""

RUN pipenv install ${PIPENV_DEV}

RUN chmod +x /freelancer_platform/commands/start_server_dev.sh

EXPOSE 8000

CMD ["bash"]
