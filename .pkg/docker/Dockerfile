FROM python:3.8-slim

COPY . /app
WORKDIR /app

RUN pip install -qr requirements.txt
CMD ["uvicorn", "src.port_adapter.api.rest.main:app"]