"""Application-specific exceptions and their FastAPI handlers."""

import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


class PhishGuardError(Exception):
    """Base class for all domain-level errors raised by PhishGuard."""

    def __init__(self, message: str, status_code: int = 400) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class ScanNotFoundError(PhishGuardError):
    """Raised when a requested scan does not exist."""

    def __init__(self, scan_id: int) -> None:
        super().__init__(f"Scan with id {scan_id} was not found.", status_code=404)


class EmptyEmailContentError(PhishGuardError):
    """Raised when the submitted email content has no usable text."""

    def __init__(self) -> None:
        super().__init__("Email content must not be empty.", status_code=422)


class ReportGenerationError(PhishGuardError):
    """Raised when a report fails to generate."""

    def __init__(self, reason: str) -> None:
        super().__init__(f"Failed to generate report: {reason}", status_code=500)


def register_exception_handlers(app: FastAPI) -> None:
    """Attach global exception handlers to the FastAPI app."""

    @app.exception_handler(PhishGuardError)
    async def handle_phishguard_error(request: Request, exc: PhishGuardError) -> JSONResponse:
        logger.warning("Handled error on %s: %s", request.url.path, exc.message)
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})

    @app.exception_handler(Exception)
    async def handle_unexpected_error(request: Request, exc: Exception) -> JSONResponse:
        logger.exception("Unhandled error on %s", request.url.path)
        return JSONResponse(status_code=500, content={"detail": "Internal server error."})
