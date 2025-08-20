"""ApiResponse"""

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class ApiResponse:
    """API Response Dataclass for Service Responses"""

    response: List | Dict[str, Any]
    status_code: int
