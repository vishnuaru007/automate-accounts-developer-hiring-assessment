from fastapi import FastAPI
from mongoengine import connect
from routes.receipt_routes import router as receipt_router

# Connect to MongoDB (must be running locally)
connect(
    db="receipts_db",  # name of the database
    host="localhost",
    port=27017,
    alias="default"    # important for mongoengine
)

app = FastAPI(title="Receipt OCR API")
app.include_router(receipt_router)