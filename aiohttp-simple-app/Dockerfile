FROM python:3.6.3

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:4000", "main:app", \
     "--worker-class", "aiohttp.worker.GunicornWebWorker"]

