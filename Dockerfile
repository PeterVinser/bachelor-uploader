FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -vvv -r requirements.txt

COPY . /app

EXPOSE 5000

ENV NAME World

CMD ["gunicorn", "-b", "0.0.0.0:5000", "run:app"]