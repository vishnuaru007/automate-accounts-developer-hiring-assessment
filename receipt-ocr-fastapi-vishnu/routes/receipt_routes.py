from fastapi import APIRouter, UploadFile, File, HTTPException
from models.receipt_models import ReceiptFile, Receipt
from utils.ocr_utils import extract_text
from utils.mongo_utils import validate_pdf, process_receipt, get_all_receipts, get_receipt_by_id
import os
import uuid
import shutil

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_receipt(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
    file_id = str(uuid.uuid4())
    file_path = f"{UPLOAD_DIR}/{file_id}.pdf"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    receipt_file = ReceiptFile(file_name=file.filename, file_path=file_path, is_valid=False)
    receipt_file.save()
    return {"id": str(receipt_file.id), "message": "File uploaded"}

@router.post("/validate")
async def validate_file(id: str):
    return validate_pdf(id)

@router.post("/process")
async def process_file(id: str):
    return process_receipt(id)

@router.get("/receipts")
async def list_receipts():
    return get_all_receipts()

@router.get("/receipts/{id}")
async def receipt_detail(id: str):
    return get_receipt_by_id(id)
