from fastapi import APIRouter, Depends, HTTPException, Request
from ..aspects.auth_aspect import authenticated, authenticate_user
from ..aspects.log_aspect import log_access
from ..services import bank_service
from .. import schemas

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.post("", response_model=schemas.Transaction)
async def create_transaction(
    request: Request,
    sender_account_id: int,
    transaction: schemas.TransactionCreate, 
    current_user: schemas.User = Depends(authenticate_user)
):
    account = bank_service.get_account_by_id(current_user.id, sender_account_id)
    if not account:
        raise HTTPException(status_code=400, detail="User has no accounts")

    return await bank_service.create_transaction(
        request,
        sender_account_id,
        {
            "amount": transaction.amount,
            "receiver_account_id": transaction.receiver_account_id
        }
    )

@router.get("/{account_id}", response_model=list[schemas.Transaction])
@log_access("get_transactions")
async def get_transactions(request: Request, account_id: int, current_user: schemas.User = Depends(authenticate_user)):
    account = bank_service.get_account_by_id(current_user.id, account_id)
    if not account:
        return []
    return bank_service.get_account_transactions(account.id)

@router.post("/deposit", response_model=schemas.Transaction)
@authenticated
async def deposit_funds(
    request: Request,
    deposit: schemas.Deposit,
    current_user: schemas.User = Depends(authenticate_user)
):
    vault_account = bank_service.get_vault_account()
    return await bank_service.create_transaction(
        request,
        vault_account.id,
        {
            "amount": deposit.amount,
            "receiver_account_id": deposit.receiver_account_id
        }
    )

@router.post("/withdraw", response_model=schemas.Transaction)
@authenticated
async def withdraw_funds(
    request: Request,
    withdraw: schemas.Withdraw,
    current_user: schemas.User = Depends(authenticate_user)
):
    vault_account = bank_service.get_vault_account()
    return await bank_service.create_transaction(
        request,
        withdraw.sender_account_id,
        {
            "amount": withdraw.amount,
            "receiver_account_id": vault_account.id
        }
    )