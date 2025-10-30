from sqlalchemy import text

from app.domain.models.health_domain_model import Health
from app.infrastructure.session_manager import get_session
from app.port.health_port import IHealthRepository


class HealthRepository(IHealthRepository):

    def check_health(self) -> Health:
        try:
            with get_session() as session:
                result = session.execute(text("SELECT 1"))
                result.scalar()
                session.commit()
                return Health(
                    status="ok",
                    message="API operacional",
                    data_connectivity=True
                )
        except Exception as e:
            return Health(
                status="error",
                message=f"Erro ao conectar com o banco: {str(e)}",
                data_connectivity=False
            )
