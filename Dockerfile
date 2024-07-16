FROM python:3.12.2-alpine

ADD main.py .
ADD banner.png .

RUN pip install discord.py

CMD ["python", "./main.py"]

