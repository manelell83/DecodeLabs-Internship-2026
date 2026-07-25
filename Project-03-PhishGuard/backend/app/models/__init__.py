"""ORM model registry — import all models so Base.metadata sees them."""

from app.models.indicator import Indicator
from app.models.report import Report
from app.models.scan import Scan

__all__ = ["Scan", "Indicator", "Report"]
