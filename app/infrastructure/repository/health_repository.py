from http import HTTPStatus

from sqlalchemy import text

from app.domain.models.health_domain_model import Health
from app.infrastructure.session_manager import get_session
from app.port.health_port import IHealthRepository
from app.utils.logger import AppLogger


class HealthRepository(IHealthRepository):

    def __init__(self) -> None:
        self._logger = AppLogger("HealthRepository")

    def check_health(self) -> Health:
        try:
            with get_session() as session:
                result = session.execute(text("SELECT 1")).scalar()
                if result != 1:
                    raise ValueError("Resposta inesperada do banco de dados")

            return Health(
                status="ok", message="API operacional", data_connectivity=True
            )
        except Exception as e:
            self._logger.exception(
                f"Health check falhou ao conectar com o banco de dados, {str(e)}",
                HTTPStatus.INTERNAL_SERVER_ERROR,
            )
            return Health(
                status="error",
                message=f"Erro ao conectar com o banco: {e}",
                data_connectivity=False,
            )
