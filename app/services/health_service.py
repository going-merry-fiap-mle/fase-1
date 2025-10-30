from app.domain.models.health_domain_model import Health
from app.port.health_port import IHealthRepository


class HealthService:

    def __init__(self, health_repository: IHealthRepository) -> None:
        self._health_repository = health_repository

    def check_health(self) -> Health:
        return self._health_repository.check_health()
