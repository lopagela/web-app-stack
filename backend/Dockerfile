FROM python:3.9
WORKDIR /app/

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install waitress

COPY api.py .

ENTRYPOINT [ "waitress-serve", "--port=8000" ]
CMD [ "api:api" ]