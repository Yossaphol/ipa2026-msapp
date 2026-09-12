FROM python

WORKDIR /app

COPY requirement.txt .

RUN pip install -r requirement.txt

COPY consumer.py .
COPY callback.py .
COPY database.py .
COPY router_client.py .

CMD ["python", "consumer.py"]