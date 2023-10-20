FROM python:3.10.12
WORKDIR /app

COPY app/ /app

RUN pip install -r requirements.txt

EXPOSE 80

CMD ["python", "principal.py"]
