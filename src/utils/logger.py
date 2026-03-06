"""
SK Framework — Structured Logger
Wraps structlog. Import get_logger() anywhere to get a typed logger.
"""

import logging
import sys
import structlog
from src.core.config import config


def _configure_structlog():
    """One-time structlog configuration based on SK config."""
    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.format_exc_info,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.UnicodeDecoder(),
    ]

    if config.log.log_format == "json":
        processors = shared_processors + [structlog.processors.JSONRenderer()]
    else:
        processors = shared_processors + [structlog.dev.ConsoleRenderer(colors=True)]

    structlog.configure(
        processors=processors,
        logger_factory=structlog.PrintLoggerFactory(),
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        cache_logger_on_first_use=True,
    )


_configure_structlog()


def get_logger(name: str = "sk") -> structlog.BoundLogger:
    """
    Get a structured logger instance.

    Usage:
        from src.utils.logger import get_logger
        log = get_logger("my_module")
        log.info("attack started", module="prompt_injection", target="gpt-4o")
    """
    return structlog.get_logger(name)
