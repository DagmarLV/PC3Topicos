from functools import wraps
from fastapi import Request
from ..database import SessionLocal
from ..services.auth_service import get_current_user
from .. import models

def log_access(action: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            db = SessionLocal()
            try:
                token = request.headers.get("Authorization", "").split("Bearer ")[-1]
                user = get_current_user(token, db)

                access_log = models.AccessLog(
                    user_id=user.id if user else None,
                    action=action,
                    ip_address=request.client.host if request.client else "unknown",
                    user_agent=request.headers.get("user-agent", "unknown")
                )
                db.add(access_log)
                db.commit()
            except Exception as e:
                db.rollback()
            finally:
                db.close()
            
            return await func(request, *args, **kwargs)
        return wrapper
    return decorator