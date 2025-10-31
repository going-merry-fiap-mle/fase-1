from app.infrastructure.adapters.health_adapter import HealthAdapter
from app.schemas.health_schema import HealthResponse
from app.services.health_service import HealthService
from app.usecases.health.health_check_use_case import HealthCheckUseCase


class HealthController:

    def call_controller(self) -> HealthResponse:
        health_adapter = HealthAdapter()
        health_service = HealthService(health_adapter)
        use_case = HealthCheckUseCase(health_service)
        health = use_case.execute()

        return HealthResponse(
            status=health.status,
            message=health.message,
            data_connectivity=health.data_connectivity
        )
