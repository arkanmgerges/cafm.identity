"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import inspect
import json
import os
from contextlib import contextmanager

from opentelemetry import trace
from opentelemetry.context import attach, detach
from opentelemetry.exporter import jaeger
from opentelemetry.sdk.trace import TracerProvider, Tracer
from opentelemetry.sdk.trace.export import BatchExportSpanProcessor
from opentelemetry.trace.span import SpanContext


class OpenTelemetry:
    def __init__(self):
        trace.set_tracer_provider(TracerProvider())
        self._tracer = trace.get_tracer(__name__)
        self._trace = trace
        self._contexts = {}

        jaegerExporter = jaeger.JaegerSpanExporter(
            service_name=os.getenv("CAFM_IDENTITY_SERVICE_NAME", "cafm-identity"),
            # configure agent
            agent_host_name=os.getenv("JAEGER_HOST", "localhost"),
            agent_port=int(os.getenv("JAEGER_THRIFT_AGENT_PORT", 6831)),
            # optional: configure also collector
            # collector_host_name='localhost',
            # collector_port=14268,
            # collector_endpoint='/api/traces?format=jaeger.thrift',
            # collector_protocol='http',
            # username=xxxx, # optional
            # password=xxxx, # optional
        )

        # Create a BatchExportSpanProcessor and add the exporter to it
        spanProcessor = BatchExportSpanProcessor(jaegerExporter)

        # add to the tracer
        trace.get_tracer_provider().add_span_processor(spanProcessor)

        # trace.get_tracer_provider().add_span_processor(
        #     SimpleExportSpanProcessor(ConsoleSpanExporter())
        # )

    def tracer(self, name: str = __name__) -> Tracer:
        return self.trace().get_tracer(name)

    def trace(self) -> trace:
        return self._trace

    def setContext(self, context: SpanContext, name: str):
        self._contexts[name] = {
            "trace_id": context.trace_id,
            "span_id": context.span_id,
            "is_remote": context.is_remote,
            "trace_flags": context.trace_flags,
            "trace_state": context.trace_state,
        }

    def serializedContext(self, name: str) -> str:
        return json.dumps(self.context(name))

    def context(self, name: str) -> dict:
        return self._contexts[name] if name in self._contexts else {}

    def contextDataFromGrpcContext(self, context) -> dict:
        from src.resource.logging.logger import logger

        logger.info("grpccontext-1")
        logger.info(context)
        metadata = context.invocation_metadata()
        if "opentel" in metadata[1]:
            return json.loads(metadata[1].value)
        return {}

    @contextmanager
    def setRemoteContext(self, contextData):
        trace = self.trace()
        options = 0
        token = None
        # The b3 spec provides no defined behavior for both sample and
        # flag values set. Since the setting of at least one implies
        # the desire for some form of sampling, propagate if either
        # header is set to allow.
        if "trace_flags" in contextData and contextData["trace_flags"] == 1:
            options |= trace.TraceFlags.SAMPLED
        if "trace_id" in contextData and "span_id" in contextData:
            ctx = trace.set_span_in_context(
                trace.DefaultSpan(
                    trace.SpanContext(
                        # trace an span ids are encoded in hex, so must be converted
                        trace_id=contextData["trace_id"],
                        span_id=contextData["span_id"],
                        is_remote=contextData["is_remote"],
                        trace_flags=trace.TraceFlags(options),
                        trace_state=trace.TraceState(contextData["trace_state"]),
                    )
                )
            )
            token = attach(ctx)
        try:
            yield
        finally:
            if token is not None:
                detach(token)

    @classmethod
    def grpcTraceOTel(cls, f):
        import inspect
        import os

        if os.getenv("OPEN_TELEMETRY_IS_RUNNING", True):

            def wrapper(*args, **kwargs):
                import src.port_adapter.AppDi as AppDi

                openTelemetry = AppDi.instance.get(OpenTelemetry)
                tracer: Tracer = openTelemetry.tracer(f.__name__)
                grpcServicerContext = cls._grpcServicerContext(args)
                if grpcServicerContext is not None:
                    contextData = openTelemetry.contextDataFromGrpcContext(
                        grpcServicerContext
                    )
                    with openTelemetry.setRemoteContext(contextData):
                        return cls._startCurrentSpan(
                            args, kwargs, openTelemetry, tracer, f
                        )
                else:
                    return cls._startCurrentSpan(args, kwargs, openTelemetry, tracer, f)

            wrapper.__signature__ = inspect.signature(f)
            wrapper.__name__ = f.__name__
            wrapper.__qualname__ = f.__qualname__
            return wrapper
        else:
            return f

    @classmethod
    def _grpcServicerContext(cls, args):
        from grpc._server import _Context

        try:
            for arg in args:
                if isinstance(arg, _Context):
                    return arg
        except:
            pass
        return None

    @classmethod
    def _startCurrentSpan(cls, args, kwargs, openTelemetry, tracer, f):
        with tracer.start_as_current_span(name=f.__name__) as span:
            span.set_attribute("module", str(inspect.getmodule(f)))
            span.set_attribute("function_name", f.__name__)
            span.set_attribute(
                "function_args", f"args = {str(args)}, kwargs = {str(kwargs)}"
            )

            ctx: SpanContext = span.get_span_context()
            # Important: the decorated method that uses this decorator, needs to use __qualname__ for its method
            openTelemetry.setContext(
                ctx, f.__qualname__
            )  # ex. class name and method like User.userAge
            return f(*args, **kwargs)
