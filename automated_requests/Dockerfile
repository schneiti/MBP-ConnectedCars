FROM python:3.8-slim-buster
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN apt-get update && apt-get install -y curl
COPY . .
EXPOSE 8000
CMD ["python3", "-m", "src.api.py"]