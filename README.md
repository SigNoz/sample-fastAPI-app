# FastAPI with SigNoz observability integration
## Prerequisite

SigNoz should be installed in your local machine or any server. To install SigNoz follow the instructions at https://signoz.io/docs/deployment/docker/


## Run instructions for sending data to SigNoz

- Create a virtual environment and activate it

```
python3 -m venv .venv
source .venv/bin/activate
```

- Change directory

```
cd app
```

- Install dependencies

```
pip install -r requirements.txt
```

- Install instrumentation packages

```
opentelemetry-bootstrap --action=install
```

- Run the app

```
OTEL_RESOURCE_ATTRIBUTES=service.name=fastapiApp OTEL_EXPORTER_OTLP_ENDPOINT=http://<IP of SigNoz>:4317 OTEL_EXPORTER_OTLP_PROTOCOL=grpc opentelemetry-instrument uvicorn main:app --host localhost --port 5002
```

`<IP of SigNoz>` will be `localhost` if you are running SigNoz in your localhost. For other installations you can use the same IP where SigNoz is accessible.

Note: set `OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf` and port 4318 in endpoint `OTEL_EXPORTER_OTLP_ENDPOINT=http://<IP of SigNoz>:4318` if you are using OTLP HTTP exporter.

- Generate traffic

Our web server is running in the port 5002 by default. Browse `http://localhost:5002` to send requests to this FastAPI server and check the metrics and trace data at `http://<IP of SigNoz>:3301`


## Run with docker

Build docker image
```
docker build -t sample-fastapi-app .
```

Run fast api app
```
# If you have your SigNoz IP Address, replace <IP of SigNoz> with your IP Address. 

docker run -d --name fastapi-container \
-e OTEL_RESOURCE_ATTRIBUTES='service.name=fastapiApp' \
-e OTEL_EXPORTER_OTLP_ENDPOINT='http://<IP of SigNoz>:4317' \
-e OTEL_EXPORTER_OTLP_PROTOCOL=grpc \
-p 5002:5002 sample-fastapi-app


# If you are running signoz through official docker-compose setup, run `docker network ls` and find clickhouse network id. It will be something like this clickhouse-setup_default 
# and pass network id by using --net <network ID>

docker run -d --name fastapi-container \ 
--net clickhouse-setup_default  \ 
--link clickhouse-setup_otel-collector_1 \
-e OTEL_RESOURCE_ATTRIBUTES='service.name=fastapiApp' \
-e OTEL_EXPORTER_OTLP_ENDPOINT='http://clickhouse-setup_otel-collector_1:4317' \
-e OTEL_EXPORTER_OTLP_PROTOCOL=grpc \
-p 5002:5002 sample-fastapi-app

```


## Send Traffic using Locust

```
pip install locust
```

```
locust -f locust.py --headless --users 10 --spawn-rate 1 -H http://localhost:5002
```


## Trobleshooting

Don't run app in reloader mode as it breaks instrumentation.

If you face any problem in instrumenting with OpenTelemetry, refer to docs at 
https://signoz.io/docs/instrumentation/python


_Credit for this sample app goes to our contributor [sureshdsk](https://github.com/sureshdsk)._
