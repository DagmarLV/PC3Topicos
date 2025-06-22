from ..database.config import Base, engine, SessionLocal
from ..services.auth_service import get_password_hash
from .. import models

def init_db():
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        if db.query(models.User).filter(models.User.full_name == "SYSTEM VAULT").first() is None:
            vault_user = models.User(
                email="vault@uni.pe",
                role="admin",
                full_name="SYSTEM VAULT",
                hashed_password=get_password_hash("vault_password")
            )
            db.add(vault_user)
            db.flush()
            print("Usuario de la bóveda creada")

            vault_account = models.BankAccount(
                account_number="0000-0000-0000-0000",
                owner_id=vault_user.id,
                balance=5000000
            )
            db.add(vault_account)
            print("Cuenta bancaria de la bóveda creada")

            db.commit()
        else:
            print("La bóveda ya está inicializada, no se realizaron cambios.")
    except Exception as e:
        db.rollback()
        print(f"❌ Error crítico al inicializar la bóveda: {str(e)}")
    finally:
        db.close()