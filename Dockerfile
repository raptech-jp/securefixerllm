FROM ubuntu:22.04

WORKDIR /app

RUN apt update && \
    apt install -y python3.10 python3-pip && \
    pip install openai

COPY main.py .

CMD ["python3", "main.py"]
