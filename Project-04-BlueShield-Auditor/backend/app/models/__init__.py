"""ORM model registry — import all models so Base.metadata sees them."""

from app.models.audit_run import AuditRun
from app.models.finding import Finding

__all__ = ["AuditRun", "Finding"]
