FROM tiangolo/uvicorn-gunicorn:python3.7

# open port
EXPOSE 5000

# add requirements
COPY ./app/requirements.txt /app/requirements.txt

# install requirements
RUN pip install -r /app/requirements.txt

# copy source code
COPY ./app /app/app

# Init command
CMD ["opentelemetry-instrument", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000"]
