FROM python:3.10

WORKDIR /bot

COPY requirements.txt requirements.txt

RUN apt-get -y update
RUN pip3 install -r requirements.txt

COPY . .

VOLUME /bot

EXPOSE 8081

CMD ["python3", "adventure_bot.py"]
