FROM tiangolo/uvicorn-gunicorn:python3.7

ENV PORT=$PORT

COPY ./src /app/src
COPY ./requirements.txt /app

WORKDIR /app

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE $PORT

CMD uvicorn src.main:app --host 0.0.0.0 --port $PORT
