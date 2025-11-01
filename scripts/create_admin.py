from app.infrastructure.session_manager import get_session
from app.infrastructure.models.user import User
from app.infrastructure.models.enums.admin_enum import UserRole
from app.core.security import get_password_hash

def create_admin():
    with get_session() as session:
        # Verificar se admin já existe
        existing_admin = session.query(User).filter(User.username == "admin").first()
        
        if existing_admin:
            print("Admin user already exists!")
            return
        
        admin = User(
            username="admin",
            password=get_password_hash("admin123"),
            role=UserRole.admin
        )
        
        session.add(admin)
        session.commit()
        print("Admin user created!")

if __name__ == "__main__":
    create_admin()