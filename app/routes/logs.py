from fastapi import APIRouter, Depends, HTTPException, Request
from .. import schemas, models
from ..database import SessionLocal
from ..aspects.notify_aspect import notify_on_failed_access
from ..aspects.auth_aspect import authenticate_user
from ..aspects.log_aspect import log_access

router = APIRouter(prefix="/access-logs", tags=["logs"])

@router.get("", response_model=list[schemas.AccessLog])
@log_access("get_access_logs")
async def get_access_logs(request: Request, current_user: schemas.User = Depends(authenticate_user)):
    db = SessionLocal()
    try:
        return (
            db.query(models.AccessLog)
            .filter(models.AccessLog.user_id == current_user.id)
            .order_by(models.AccessLog.created_at.desc())
            .all()
        )
    finally:
        db.close()

@router.get("/all", response_model=list[schemas.AccessLog])
@notify_on_failed_access
@log_access("get_all_access_logs")
async def get_all_access_logs(request: Request, current_user: schemas.User = Depends(authenticate_user)):
    db = SessionLocal()
    try:
        if current_user.role != "admin":
            raise HTTPException(status_code=403, detail="Access denied")
        return (
            db.query(models.AccessLog)
            .order_by(models.AccessLog.created_at.desc())
            .all()
        )
    finally:
        db.close()