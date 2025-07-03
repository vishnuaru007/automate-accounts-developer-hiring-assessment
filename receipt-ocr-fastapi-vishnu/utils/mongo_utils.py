from models.receipt_models import ReceiptFile, Receipt
from utils.ocr_utils import extract_text
from datetime import datetime
from bson import ObjectId
import re

def validate_pdf(file_id: str):
    try:
        receipt_file = ReceiptFile.objects(id=ObjectId(file_id)).first()
    except Exception:
        return {"error": "Invalid ID format"}

    if not receipt_file:
        return {"error": "File not found"}

    if receipt_file.file_path.endswith(".pdf"):
        receipt_file.is_valid = True
        receipt_file.invalid_reason = None
    else:
        receipt_file.is_valid = False
        receipt_file.invalid_reason = "Invalid file format"

    receipt_file.updated_at = datetime.utcnow()
    receipt_file.save()
    return {"id": str(receipt_file.id), "is_valid": receipt_file.is_valid}

def process_receipt(file_id: str):
    try:
        receipt_file = ReceiptFile.objects(id=ObjectId(file_id)).first()
    except Exception:
        return {"error": "Invalid ID format"}

    if not receipt_file or not receipt_file.is_valid:
        return {"error": "File not found or invalid"}

    text = extract_text(receipt_file.file_path)

    date_match = re.search(r"(\d{2}/\d{2}/\d{4})", text)
    amount_match = re.search(r"Total\s*[:]?[\s$]*(\d+\.\d{2})", text, re.IGNORECASE)
    merchant_match = text.split("\n")[0].strip() if text else "Unknown"

    receipt = Receipt(
        purchased_at=date_match.group(1) if date_match else "Unknown",
        merchant_name=merchant_match,
        total_amount=amount_match.group(1) if amount_match else "0.00",
        file_path=receipt_file.file_path
    )
    receipt.save()

    receipt_file.is_processed = True
    receipt_file.updated_at = datetime.utcnow()
    receipt_file.save()

    return {
        "id": str(receipt.id),
        "merchant": receipt.merchant_name,
        "amount": receipt.total_amount,
        "date": receipt.purchased_at
    }

def get_all_receipts():
    receipts = Receipt.objects()
    result = []
    for r in receipts:
        result.append({
            "id": str(r.id),
            "merchant": r.merchant_name,
            "amount": r.total_amount,
            "date": r.purchased_at,
            "file_path": r.file_path,
            "created_at": r.created_at.isoformat(),
            "updated_at": r.updated_at.isoformat(),
        })
    return result

def get_receipt_by_id(id: str):
    try:
        r = Receipt.objects(id=ObjectId(id)).first()
        if not r:
            return {"error": "Not found"}

        return {
            "id": str(r.id),
            "merchant": r.merchant_name,
            "amount": r.total_amount,
            "date": r.purchased_at,
            "file_path": r.file_path,
            "created_at": r.created_at.isoformat(),
            "updated_at": r.updated_at.isoformat(),
        }
    except Exception:
        return {"error": "Invalid ID format"}
