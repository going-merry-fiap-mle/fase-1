from app.domain.models.health_domain_model import Health
from app.infrastructure.repository.health_repository import HealthRepository
from app.port.health_port import IHealthRepository


class HealthAdapter(IHealthRepository):

    def __init__(self) -> None:
        self._repository = HealthRepository()

    def check_health(self) -> Health:
        return self._repository.check_health()
