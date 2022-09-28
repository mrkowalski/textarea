FROM python:3.10-bullseye

RUN apt update
WORKDIR /usr/src/textarea
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
COPY main.py .
#CMD ["tail", "-f", "/dev/null"]
CMD ["sh", "-c", "gunicorn --bind :$PORT main:application"]
