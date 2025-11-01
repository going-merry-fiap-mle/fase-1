"""create_admin_user

Revision ID: ea4adf35f20d
Revises: abc740b20a1e
Create Date: 2025-10-23 20:20:37.670991

"""
from typing import Sequence, Union
import uuid
import hashlib
from datetime import datetime, timezone

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from app.utils.logger import AppLogger

# Setup logger
logger = AppLogger(__name__)


# revision identifiers, used by Alembic.
revision: str = 'ea4adf35f20d'
down_revision: Union[str, Sequence[str], None] = 'dfc9d0632cdc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create admin user."""
    # Get database connection
    connection = op.get_bind()
    
    # Check if admin user already exists
    result = connection.execute(sa.text(
        "SELECT COUNT(*) FROM users WHERE username = 'admin'"
    )).scalar()
    
    if result == 0:
        # Create admin user with simple hash (temporary)
        admin_id = str(uuid.uuid4())
        # Simple hash for migration - will be updated by create_admin.py script
        simple_hash = hashlib.sha256("admin123".encode()).hexdigest()
        created_at = datetime.now(timezone.utc)
        
        connection.execute(sa.text(
            "INSERT INTO users (id, username, password, role, created_at, updated_at) "
            "VALUES (:id, :username, :password, :role, :created_at, :updated_at)"
        ), {
            'id': admin_id,
            'username': 'admin',
            'password': simple_hash,
            'role': 'admin',
            'created_at': created_at,
            'updated_at': created_at
        })

        logger.info("Admin user created successfully! Use create_admin.py script to set proper bcrypt password.")
    else:
        logger.info("Admin user already exists, skipping creation.")


def downgrade() -> None:
    """Remove admin user."""
    connection = op.get_bind()
    
    # Remove admin user
    connection.execute(sa.text(
        "DELETE FROM users WHERE username = 'admin'"
    ))
    
    logger.info("Admin user removed.")
