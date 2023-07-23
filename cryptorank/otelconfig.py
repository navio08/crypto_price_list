from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from config import MY_SERVICE_NAME, HOST_JAEGER

resource = Resource(attributes={
    SERVICE_NAME: MY_SERVICE_NAME
})

jaeger_exporter = JaegerExporter(
    agent_host_name=HOST_JAEGER,
    agent_port=6831,
)


provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(jaeger_exporter)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer_provider().get_tracer(__name__)
