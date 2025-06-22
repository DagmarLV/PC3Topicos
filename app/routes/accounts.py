from fastapi import APIRouter, Depends, Request
from .. import schemas
from ..aspects.auth_aspect import authenticated, authenticate_user
from ..services.bank_service import create_bank_account, get_user_accounts, create_account_number, remove_bank_account
from ..aspects.log_aspect import log_access

router = APIRouter(prefix="/accounts", tags=["accounts"])

@router.post("", response_model=schemas.BankAccount)
@log_access("create_account")
async def create_account(request: Request, current_user: schemas.User = Depends(authenticate_user)):
    account_number = create_account_number()
    return create_bank_account(account_number, current_user.id)

@router.delete("/{account_id}", response_model=schemas.Message)
@authenticated
@log_access("delete_account")
async def delete_account(request: Request, account_id: int, current_user: schemas.User = Depends(authenticate_user)):
    return remove_bank_account(account_id)

@router.get("", response_model=list[schemas.BankAccount])
@log_access("get_accounts")
async def get_accounts(request: Request, current_user: schemas.User = Depends(authenticate_user)):
    return get_user_accounts(current_user.id)