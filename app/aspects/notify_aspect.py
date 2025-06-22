from functools import wraps
from fastapi import Request, HTTPException, Depends
from ..services.email_service import send_email
from ..database import SessionLocal
from .. import models, schemas
from ..aspects.auth_aspect import authenticate_user

def notify_on_transaction(email_type: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            result = await func(*args, **kwargs)

            if isinstance(result, models.Transaction):
                db = SessionLocal()
                try:
                    transaction = db.query(models.Transaction).filter(models.Transaction.id == result.id).first()
                    print(f"Transaction found: {str(transaction)}")
                    if transaction:
                        sender = db.query(models.User).filter(models.User.id == transaction.sender_account.owner_id).first()
                        receiver = db.query(models.User).filter(models.User.id == transaction.receiver_account.owner_id).first()

                        if email_type == "sender":
                            send_email(
                                recipient=sender.email,
                                subject="Transaction Sent",
                                body=f"You have sent {transaction.amount} to account {transaction.receiver_account.account_number}"
                            )
                        elif email_type == "receiver":
                            send_email(
                                recipient=receiver.email,
                                subject="Transaction Received",
                                body=f"You have received {transaction.amount} from account {transaction.sender_account.account_number}"
                            )
                finally:
                    db.close()
            
            return result
        return wrapper
    return decorator

def notify_on_failed_access(func):
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        try:
            return await func(request, *args, **kwargs)
        except Exception:
            db = SessionLocal()
            try:
                current_user = kwargs.get('current_user')
                if current_user:
                    body = f"Usuario {current_user.email} intentó acceder a {request.url.path}."
                else:
                    body = f"Alguien intentó acceder a {request.url.path}."
                
                admins = db.query(models.User).filter(models.User.role == "admin").all()
                for admin in admins:
                    send_email(
                        recipient=admin.email,
                        subject="Intento de acceso no autorizado",
                        body=body
                    )
            finally:
                db.close()
            raise
    return wrapper