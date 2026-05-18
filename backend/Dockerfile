FROM python:3.12-slim AS builder

RUN pip install -U pdm
ENV PDM_CHECK_UPDATE=false

WORKDIR /app
COPY pyproject.toml pdm.lock ./

RUN pdm install --prod --no-editable --no-self

COPY . .
RUN pdm install --prod --no-editable

FROM python:3.12-slim

COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app
COPY . .

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]