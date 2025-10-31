from app.domain.models.health_domain_model import Health
from app.services.health_service import HealthService


class HealthCheckUseCase:

    def __init__(self, health_service: HealthService) -> None:
        self._health_service = health_service

    def execute(self) -> Health:
        return self._health_service.check_health()
