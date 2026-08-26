FROM python:3.12-slim
ARG SERVICE_PATH=.
WORKDIR /app
COPY ${SERVICE_PATH}/pyproject.toml .
COPY shared/python-common-lib/pyproject.toml shared/python-common-lib/
RUN pip install --no-cache-dir --editable shared/python-common-lib
RUN pip install --no-cache-dir --editable .
COPY ${SERVICE_PATH}/. .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
