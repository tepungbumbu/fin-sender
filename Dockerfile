FROM python:3.12-slim

WORKDIR /app
COPY send_fin.py ./
RUN pip install requests

ENTRYPOINT ["python", "send_fin.py"]
