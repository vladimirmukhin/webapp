from python:latest

COPY main.py .

RUN python3 -m pip install requests

CMD python3 main.py