import random
from datetime import datetime
from ..models import BankAccount, Transaction
from ..database import SessionLocal
from ..aspects.notify_aspect import notify_on_transaction
from ..aspects.log_aspect import log_access
from fastapi import HTTPException, status, Request

def create_bank_account(account_number: str, owner_id: int):
    db = SessionLocal()
    try:
        account = BankAccount(account_number=account_number, owner_id=owner_id)
        db.add(account)
        db.commit()
        db.refresh(account)
        return account
    finally:
        db.close()

def remove_bank_account(account_id: int):
    db = SessionLocal()
    try:
        account = db.query(BankAccount).filter(BankAccount.id == account_id).first()
        if not account:
            return {"detail": "Account not found"}
        db.delete(account)
        db.commit()
        return {"detail": "Account deleted successfully"}
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

def get_vault_account():
    db = SessionLocal()
    try:
        vault_account = db.query(BankAccount).filter(BankAccount.account_number == "0000-0000-0000-0000").first()
        if not vault_account:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vault account not found")
        return vault_account
    finally:
        db.close()

@notify_on_transaction("sender")
@notify_on_transaction("receiver")
@log_access("create_transaction")
async def create_transaction(request: Request, sender_account_id: int, transaction_data: dict):
    db = SessionLocal()
    try:
        print(f"Creating transaction from account {sender_account_id} with data: {transaction_data}")
        sender_account = db.query(BankAccount).filter(BankAccount.id == sender_account_id).first()
        if not sender_account:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sender account not found")
        
        receiver_account = db.query(BankAccount).filter(BankAccount.id == transaction_data["receiver_account_id"]).first()
        if not receiver_account:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Receiver account not found")
        
        if sender_account.balance < transaction_data["amount"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient funds"
            )
        
        sender_account.balance -= transaction_data["amount"]
        receiver_account.balance += transaction_data["amount"]
        
        transaction = Transaction(
            amount=transaction_data["amount"],
            sender_account_id=sender_account_id,
            receiver_account_id=transaction_data["receiver_account_id"],
            status="completed"
        )
        
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        return transaction
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

def get_user_accounts(user_id: int):
    db = SessionLocal()
    try:
        return db.query(BankAccount).filter(BankAccount.owner_id == user_id).all()
    finally:
        db.close()

def get_account_by_id(user_id: int, account_id: int):
    db = SessionLocal()
    try:
        account = db.query(BankAccount).filter(BankAccount.id == account_id, BankAccount.owner_id == user_id).first()
        if not account:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
        return account
    finally:
        db.close()

def get_account_transactions(account_id: int):
    db = SessionLocal()
    try:
        return db.query(Transaction).filter(
            (Transaction.sender_account_id == account_id) | 
            (Transaction.receiver_account_id == account_id)
        ).order_by(Transaction.created_at.desc()).all()
    finally:
        db.close()

def create_account_number():
    db = SessionLocal()
    try:
        max_attempts = 1000
        while max_attempts > 0:
            digits = [str(random.randint(0, 9)) for _ in range(16)]
            account_number = '-'.join(''.join(digits[i:i+4]) for i in range(0, 16, 4))
            if db.query(BankAccount).filter(BankAccount.account_number == account_number).first() is None:
                return account_number
            max_attempts -= 1
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to generate unique account number")
    except Exception as e:
        raise e
    finally:
        db.close()