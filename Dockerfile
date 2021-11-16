FROM python:3.9.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

WORKDIR /app/bot

EXPOSE 5050

CMD ["python3", "./Main.py"]