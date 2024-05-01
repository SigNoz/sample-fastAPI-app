from fastapi import FastAPI, HTTPException, Request
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from custom_exporter import FilterErrorEventsSpanProcessor
import traceback
from opentelemetry.trace.status import StatusCode
from fastapi.responses import JSONResponse

# Initialize your tracer provider
provider = TracerProvider()

# Set the provider in global configuration
trace.set_tracer_provider(provider)

# Initialize the default exporter
otlp_exporter = OTLPSpanExporter()

# Add the OTLP exporter to a BatchSpanProcessor
provider.add_span_processor(BatchSpanProcessor(otlp_exporter))

# Add the custom SpanProcessor to the tracer provider
provider.add_span_processor(FilterErrorEventsSpanProcessor())
# FastAPI app instance
app = FastAPI()

# Instrument FastAPI
FastAPIInstrumentor.instrument_app(app)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/error")
async def error():
    try:
        raise ValueError("This is an intentional error")
    except Exception as e:
        # Get the current span
        current_span = trace.get_current_span()
        # Log the exception manually
        current_span.record_exception(
            exception=e,
            attributes={"exception.stacktrace": traceback.format_exc()}
        )
        # Set the span status to ERROR
        current_span.set_status(StatusCode.ERROR, description=str(e))
        # Return a response without stack trace details
        return JSONResponse(
            status_code=500,
            content={"message": "An internal error occurred"}
        )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    response = JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )
    # Log the HTTP exception similarly if needed
    current_span = trace.get_current_span()
    current_span.record_exception(
        exception=exc,
        attributes={"http.exception_detail": exc.detail}
    )
    current_span.set_status(StatusCode.ERROR, description=exc.detail)
    return response