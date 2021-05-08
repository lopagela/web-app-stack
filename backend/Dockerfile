FROM python:3.9-slim
WORKDIR /app/

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install uvicorn[standard]==0.13.4 gunicorn==20.1.0

COPY api.py .

EXPOSE 8000

# TODO it should use guvicorn for production use.
# Note that the bind option *have to* be in the form 0.0.0.0:PORT
# https://www.uvicorn.org/deployment/#gunicorn
ENTRYPOINT [ "gunicorn", "--worker-class=uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000" ]
CMD [ "api:app"]