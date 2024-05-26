FROM python:3.11.3-slim

RUN apt-get update && apt-get install -y --no-install-recommends build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir /freelancer_platform

WORKDIR /freelancer_platform

COPY ./src ./src
COPY ./Pipfile ./Pipfile
COPY ./Pipfile.lock ./Pipfile.lock

RUN python -m pip install --upgrade pip
RUN pip install pipenv

ENV PIPENV_VENV_IN_PROJECT=1

RUN pipenv install --dev

ENV PYTHONPATH="/freelancer_platform/src"

CMD ["pipenv", "run", "python", "src/manage.py", "runserver", "0.0.0.0:8000"]