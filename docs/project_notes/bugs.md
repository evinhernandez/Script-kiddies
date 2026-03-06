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
