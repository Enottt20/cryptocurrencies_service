FROM python:3.11-slim

WORKDIR /src

COPY requirements.txt /src/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /src/app

ENV PYTHONPATH "${PYTHONPATH}:/src"

CMD ["python3", "app/main.py"]
