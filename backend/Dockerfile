FROM python:3.12-slim

WORKDIR /app

RUN pip install pdm

COPY pyproject.toml pdm.lock ./
RUN pdm install --prod --no-lock --no-editable

COPY . .

EXPOSE 8000