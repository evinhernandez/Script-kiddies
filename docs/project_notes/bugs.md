# Bug Log

## 2026-03-06 - Pydantic v2 Migration
- **Issue**: `ImportError: BaseSettings has been moved to pydantic-settings`
- **Root Cause**: Project was using Pydantic v2 but attempting to import `BaseSettings` from the core `pydantic` package.
- **Solution**: Installed `pydantic-settings` and updated `src/core/config.py` to use `pydantic_settings.BaseSettings`.
- **Prevention**: Always check migration guides when using major version bumps of core libraries.

## 2026-03-06 - Structlog Keyword Argument Conflict
- **Issue**: `TypeError: PrintLogger.msg() got an unexpected keyword argument 'extra'`
- **Root Cause**: Misconfiguration of `structlog` where a `BoundLogger` was wrapping a `PrintLogger` that doesn't support the `extra` kwarg natively in the way it was being called.
- **Solution**: Refactored `src/utils/logger.py` to use `structlog.make_filtering_bound_logger` and properly configured the processor pipeline.

## 2026-03-06 - Textual Property Conflict
- **Issue**: `AttributeError: property 'tree' of 'ThreatGraph' object has no setter`
- **Root Cause**: Used the name `self.tree` in a Textual `Static` subclass, which conflicted with an internal Textual property.
- **Solution**: Renamed the internal variable to `self._tree`.
- **Prevention**: Use underscores for internal widget state in Textual to avoid shadow conflicts with the framework.

## 2026-03-06 - SQLAlchemy Reserved Keyword
- **Issue**: `sqlalchemy.exc.InvalidRequestError: Attribute name 'metadata' is reserved`
- **Root Cause**: Named a column `metadata` in the `AttackSession` ORM model. SQLAlchemy uses `metadata` for its own internal registry.
- **Solution**: Renamed the column to `extra_metadata`.
- **Prevention**: Avoid using `metadata`, `table`, or `query` as column names in SQLAlchemy models.

## 2026-03-07 - LiteLLM Compliance Error
- **Issue**: `litellm.exceptions.InternalServerError: OpenAIException - Invalid response object`
- **Root Cause**: The local ACME lab app returned a response that was missing required OpenAI fields (`usage`, `model`, etc.) or had invalid `finish_reason` values.
- **Solution**: Refactored `src/labs/acme_app.py` to use a helper that generates strictly compliant OpenAI response objects.
- **Prevention**: Always verify that custom target proxies adhere to the target API specification (e.g., OpenAI spec).

## 2026-03-07 - Console Prompt Corruption
- **Issue**: Prompt looked like `pt)> sk(prom` instead of `sk(prompt)>`.
- **Root Cause**: A blind string replacement of the letter `m` in ANSI color codes was accidentally matching characters in the module names themselves.
- **Solution**: Used a precise regular expression to wrap only the ANSI escape sequences with readline ignore characters (`\001` and `\002`).
- **Prevention**: Never perform global string replacements on strings containing both UI text and ANSI control codes.
