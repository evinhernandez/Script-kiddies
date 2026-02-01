"""
SK Framework — Structured Logger
Wraps structlog. Import get_logger() anywhere to get a typed logger.
"""

import sys
import structlog
from src.core.config import config


def _configure_structlog():
    """One-time structlog configuration based on SK config."""
    shared_processors = [
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
    ]

    if config.log.log_format == "json":
        renderer = structlog.processors.JSONRenderer()
    else:
        renderer = structlog.dev.ConsoleRenderer(colors=True)

    structlog.configure(
        processors=shared_processors + [
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.PrintLoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # Also configure stdlib logging so FastAPI/uvicorn logs go through structlog
    formatter = structlog.stdlib.ProcessorFormatter(
        processor=renderer,
        foreign_pre_chain=shared_processors,
    )
    handler = structlog.stdlib.ProcessorFormatter.wrap_for_formatter
    root_logger = __import__("logging").getLogger()
    root_logger.setLevel(getattr(__import__("logging"), config.log.log_level))


_configure_structlog()


def get_logger(name: str = "sk") -> structlog.stdlib.BoundLogger:
    """
    Get a structured logger instance.

    Usage:
        from src.utils.logger import get_logger
        log = get_logger("my_module")
        log.info("attack started", module="prompt_injection", target="gpt-4o")
    """
    return structlog.get_logger(name)
