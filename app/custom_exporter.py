from opentelemetry.sdk.trace import SpanProcessor, Span
from opentelemetry.trace import SpanContext
from opentelemetry.trace.status import StatusCode

class FilterErrorEventsSpanProcessor(SpanProcessor):
    def on_start(self, span: Span, parent_context: SpanContext):
        # This method is called when a span starts.
        pass

    def on_end(self, span: Span):
        # This method is called when a span ends.
        if span.status.status_code == StatusCode.ERROR:
            # Clear all events if the span's status code indicates an error.
            span._events = []

    def shutdown(self):
        # This method is called when the SpanProcessor is shutting down.
        pass

    def force_flush(self, timeout_millis: int = 30000) -> bool:
        # This method is called to force flushing of the spans.
        return True
