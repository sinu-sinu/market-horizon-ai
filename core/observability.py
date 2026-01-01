"""
Langfuse Observability Module (v2 API)

Provides centralized tracing utilities for the Market Horizon AI pipeline.
Integrates with Langfuse for LLM observability, debugging, and cost tracking.
"""

from functools import wraps
from typing import Optional, Dict, Any, Callable
from datetime import datetime
import logging
import uuid

from core.config import config

logger = logging.getLogger(__name__)

# Global Langfuse client instance
_langfuse_client = None

# Store active trace IDs for span creation
_active_trace_ids: Dict[str, Any] = {}


def get_langfuse_client():
    """
    Get or initialize the Langfuse client using v2 API.
    Returns None if Langfuse is disabled or not configured.
    """
    global _langfuse_client

    if not config.LANGFUSE_ENABLED:
        return None

    if _langfuse_client is not None:
        return _langfuse_client

    if not config.LANGFUSE_PUBLIC_KEY or not config.LANGFUSE_SECRET_KEY:
        logger.warning(
            "Langfuse enabled but credentials not configured. "
            "Set LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY environment variables."
        )
        return None

    try:
        from langfuse import Langfuse

        _langfuse_client = Langfuse(
            public_key=config.LANGFUSE_PUBLIC_KEY,
            secret_key=config.LANGFUSE_SECRET_KEY,
            host=config.LANGFUSE_HOST,
        )
        logger.info(f"Langfuse client initialized (host: {config.LANGFUSE_HOST})")
        return _langfuse_client

    except ImportError:
        logger.warning("Langfuse package not installed. Run: pip install langfuse")
        return None
    except Exception as e:
        logger.error(f"Failed to initialize Langfuse client: {e}")
        return None


def get_langfuse_callback_handler(trace_id: Optional[str] = None):
    """
    Get LangChain callback handler for Langfuse integration (v2 API).

    NOTE: Due to langchain version compatibility issues, this may return None.
    Use log_llm_call() instead for reliable token tracking.

    Args:
        trace_id: Optional trace ID to link LLM calls to a parent trace

    Returns:
        CallbackHandler instance or None if Langfuse is not available
    """
    if not config.LANGFUSE_ENABLED:
        return None

    if not config.LANGFUSE_PUBLIC_KEY or not config.LANGFUSE_SECRET_KEY:
        return None

    try:
        from langfuse.callback import CallbackHandler

        handler = CallbackHandler(
            public_key=config.LANGFUSE_PUBLIC_KEY,
            secret_key=config.LANGFUSE_SECRET_KEY,
            host=config.LANGFUSE_HOST,
            trace_id=trace_id,
        )
        return handler

    except (ImportError, ModuleNotFoundError):
        logger.debug("Langfuse callback handler not available - use log_llm_call() instead")
        return None
    except Exception as e:
        logger.debug(f"Langfuse callback handler failed: {e} - use log_llm_call() instead")
        return None


def _normalize_model_name(model: str) -> str:
    """
    Normalize model names by removing date suffixes.
    e.g., 'gpt-4.1-mini-2025-04-14' -> 'gpt-4.1-mini'
    """
    import re
    # Remove date suffix pattern like -2025-04-14
    return re.sub(r'-\d{4}-\d{2}-\d{2}$', '', model)


def log_llm_call(
    trace_id: str,
    name: str,
    model: str,
    input_text: str,
    output_text: str,
    input_tokens: int = 0,
    output_tokens: int = 0,
    metadata: Optional[Dict[str, Any]] = None
):
    """
    Log an LLM generation call with token usage to Langfuse.

    Use this instead of callback handler for reliable token tracking.

    Args:
        trace_id: The trace ID to attach this generation to
        name: Name of the generation (e.g., "competitor-extraction")
        model: Model name (e.g., "gpt-4.1-mini")
        input_text: The prompt sent to the LLM
        output_text: The response from the LLM
        input_tokens: Number of input tokens
        output_tokens: Number of output tokens
        metadata: Optional metadata dict
    """
    if trace_id not in _active_trace_ids:
        return

    trace = _active_trace_ids.get(trace_id)
    if not trace:
        return

    # Normalize model name (remove date suffix)
    normalized_model = _normalize_model_name(model)

    try:
        generation = trace.generation(
            name=name,
            model=normalized_model,
            input=input_text[:5000],  # Truncate to avoid huge payloads
            output=output_text[:5000],
            usage={
                "input": input_tokens,
                "output": output_tokens,
            },
            metadata=metadata or {}
        )
        generation.end()
        logger.debug(f"Logged LLM call: {name} ({input_tokens}+{output_tokens} tokens)")
    except Exception as e:
        logger.debug(f"Failed to log LLM call: {e}")


class Tracer:
    """
    Context manager for creating Langfuse traces using v2 API.

    Usage:
        with Tracer("pipeline", metadata={"query": "CRM tools"}) as trace:
            # trace.id contains the trace ID
            # Pass trace.id to agents for span creation
    """

    def __init__(
        self,
        name: str,
        metadata: Optional[Dict[str, Any]] = None,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
    ):
        self.name = name
        self.metadata = metadata or {}
        self.user_id = user_id
        self.session_id = session_id
        self.trace = None
        self.id = None
        self.start_time = None

    def __enter__(self):
        self.start_time = datetime.now()
        client = get_langfuse_client()

        if client:
            try:
                self.trace = client.trace(
                    name=self.name,
                    user_id=self.user_id,
                    session_id=self.session_id,
                    metadata=self.metadata,
                )
                self.id = self.trace.id
                _active_trace_ids[self.id] = self.trace
                logger.debug(f"Created Langfuse trace: {self.name} (id: {self.id})")
            except Exception as e:
                logger.warning(f"Failed to create Langfuse trace: {e}")
                self.id = str(uuid.uuid4())
        else:
            self.id = str(uuid.uuid4())

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        duration_ms = (datetime.now() - self.start_time).total_seconds() * 1000

        if self.trace:
            try:
                output_data = {"duration_ms": duration_ms}
                if exc_type:
                    output_data["error"] = str(exc_val)
                    output_data["error_type"] = exc_type.__name__

                self.trace.update(output=output_data)

                if self.id in _active_trace_ids:
                    del _active_trace_ids[self.id]
            except Exception as e:
                logger.warning(f"Failed to end Langfuse trace: {e}")

        return False


class Span:
    """
    Context manager for creating Langfuse spans within a trace using v2 API.

    Usage:
        with Span(trace_id, "research_agent", metadata={"sources": 3}) as span:
            # Execute agent logic
            span.update(output={"competitors": [...]})
    """

    def __init__(
        self,
        trace_id: str,
        name: str,
        metadata: Optional[Dict[str, Any]] = None,
        input_data: Optional[Any] = None,
    ):
        self.trace_id = trace_id
        self.name = name
        self.metadata = metadata or {}
        self.input_data = input_data
        self.span = None
        self.start_time = None
        self._output = None

    def __enter__(self):
        self.start_time = datetime.now()

        if self.trace_id not in _active_trace_ids:
            return self

        trace = _active_trace_ids.get(self.trace_id)
        if trace:
            try:
                self.span = trace.span(
                    name=self.name,
                    input=self.input_data,
                    metadata=self.metadata,
                )
                logger.debug(f"Created Langfuse span: {self.name}")
            except Exception as e:
                logger.warning(f"Failed to create Langfuse span: {e}")

        return self

    def update(self, output: Any = None, metadata: Optional[Dict[str, Any]] = None):
        """Update span with output data"""
        if output is not None:
            self._output = output
        if metadata:
            self.metadata.update(metadata)

    def __exit__(self, exc_type, exc_val, exc_tb):
        duration_ms = (datetime.now() - self.start_time).total_seconds() * 1000

        if self.span:
            try:
                output_data = self._output or {}
                if isinstance(output_data, dict):
                    output_data["duration_ms"] = duration_ms
                    if exc_type:
                        output_data["error"] = str(exc_val)
                        output_data["error_type"] = exc_type.__name__

                self.span.end(output=output_data, metadata=self.metadata)
            except Exception as e:
                logger.warning(f"Failed to end Langfuse span: {e}")

        return False


def create_span(trace_id: str, name: str, input_data: Optional[Dict] = None) -> Optional[Any]:
    """
    Create a manual span for API call tracing (v2 API).

    Args:
        trace_id: The trace ID to attach this span to
        name: Name of the span
        input_data: Optional input data to log

    Returns:
        Span object or None if tracing unavailable
    """
    if trace_id not in _active_trace_ids:
        return None

    trace = _active_trace_ids.get(trace_id)
    if not trace:
        return None

    try:
        span = trace.span(name=name, input=input_data)
        return span
    except Exception as e:
        logger.debug(f"Failed to create manual span {name}: {e}")
        return None


def end_span(span: Any, output_data: Optional[Dict] = None):
    """
    End a manually created span.

    Args:
        span: The span object from create_span()
        output_data: Optional output data to log
    """
    if span is None:
        return

    try:
        span.end(output=output_data)
    except Exception as e:
        logger.debug(f"Failed to end span: {e}")


def traced(name: Optional[str] = None):
    """
    Decorator to trace a function execution using v2 API.

    Usage:
        @traced("my_function")
        def my_function(arg1, arg2):
            return result
    """

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            trace_name = name or func.__name__
            client = get_langfuse_client()

            if not client:
                return func(*args, **kwargs)

            try:
                trace = client.trace(name=trace_name)
                start_time = datetime.now()

                try:
                    result = func(*args, **kwargs)
                    duration_ms = (datetime.now() - start_time).total_seconds() * 1000
                    trace.update(
                        output=str(result)[:1000],
                        metadata={"duration_ms": duration_ms},
                    )
                    return result
                except Exception as e:
                    duration_ms = (datetime.now() - start_time).total_seconds() * 1000
                    trace.update(
                        output={"error": str(e), "error_type": type(e).__name__},
                        metadata={"duration_ms": duration_ms},
                    )
                    raise

            except Exception as trace_error:
                logger.warning(f"Tracing failed for {trace_name}: {trace_error}")
                return func(*args, **kwargs)

        return wrapper

    return decorator


def flush():
    """Flush any pending Langfuse events"""
    client = get_langfuse_client()
    if client:
        try:
            client.flush()
        except Exception as e:
            logger.warning(f"Failed to flush Langfuse events: {e}")


def shutdown():
    """Shutdown Langfuse client gracefully"""
    global _langfuse_client
    if _langfuse_client:
        try:
            _langfuse_client.flush()
            _langfuse_client.shutdown()
            logger.info("Langfuse client shutdown complete")
        except Exception as e:
            logger.warning(f"Error during Langfuse shutdown: {e}")
        finally:
            _langfuse_client = None
