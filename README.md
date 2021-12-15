# FastAPI with SigNoz observability integration
## Prerequisite
SigNoz should be installed in your local machine or any server. To install SigNoz follow the instructions at https://signoz.io/docs/deployment/docker/


## Run instructions for sending data to SigNoz

```
cd app
```

```
pip3 install -r requirements.txt
```

```
opentelemetry-bootstrap --action=install
```

```
OTEL_RESOURCE_ATTRIBUTES=service.name=pythonApp OTEL_EXPORTER_OTLP_ENDPOINT="http://<IP of SigNoz>:4317" opentelemetry-instrument uvicorn main:app
```

For example:
`<IP of SigNoz>` will be `localhost` if you are running SigNoz in your localhost. For other installations you can use the same IP where SigNoz is accessible.

Our web server is running in the port 5002 by default. Browse `http://localhost:5002` to send requests to this flask server and check the metrics and trace data at `http://<IP of SigNoz>:3000`


## Run with docker
Build docker image
```
docker build -t sample-fastapi-app .
```

Run fast api app
```
# If you have your SigNoz IP Address, replace <IP of SigNoz> with your IP Address. 

docker run -d --name fastapi-container \
-e OTEL_METRICS_EXPORTER='none' \
-e OTEL_RESOURCE_ATTRIBUTES='service.name=fastapiApp' \
-e OTEL_EXPORTER_OTLP_ENDPOINT='http://<IP of SigNoz>:4317' \
-p 5000:5000 sample-fastapi-app


# If you are running signoz through official docker-compose setup, run `docker network ls` and find clickhouse network id. It will be something like this clickhouse-setup_default 
# and pass network id by using --net <network ID>

docker run -d --name fastapi-container \ 
--net clickhouse-setup_default  \ 
--link clickhouse-setup_otel-collector_1 \
-e OTEL_METRICS_EXPORTER='none' \
-e OTEL_RESOURCE_ATTRIBUTES='service.name=fastapiApp' \
-e OTEL_EXPORTER_OTLP_ENDPOINT='http://clickhouse-setup_otel-collector_1:4317' \
-p 5000:5000 sample-fastapi-app

```


## Send Traffic 
```
pip3 install locust
```

```
locust -f locust.py --headless --users 10 --spawn-rate 1 -H http://localhost:5000
```


## Trobleshooting
Don't run app in reloader mode as it breaks instrumentation.

If you face any problem in instrumenting with OpenTelemetry, refer to docs at 
https://signoz.io/docs/instrumentation/python


_Credit for this sample app goes to our contributor [sureshdsk](https://github.com/sureshdsk)._
