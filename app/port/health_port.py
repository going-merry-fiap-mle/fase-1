from typing import Protocol

from app.domain.models.health_domain_model import Health


class IHealthRepository(Protocol):

    def check_health(self) -> Health: ...
