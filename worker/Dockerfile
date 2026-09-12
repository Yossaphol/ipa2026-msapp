FROM python

WORKDIR /app

COPY requirement.txt .

RUN pip install -r requirement.txt

COPY consumer.py .

CMD ["python", "consumer.py"]