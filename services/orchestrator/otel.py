"""OpenTelemetry helpers."""
from __future__ import annotations

from contextlib import contextmanager
import time
from opentelemetry import trace

tracer = trace.get_tracer(__name__)


@contextmanager
def span(name: str):
    with tracer.start_as_current_span(name) as sp:
        start = time.time()
        yield sp
        sp.set_attribute("elapsed_ms", (time.time() - start) * 1000)
