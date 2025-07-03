from mongoengine import Document, StringField, BooleanField, DateTimeField
from datetime import datetime

class ReceiptFile(Document):
    file_name = StringField(required=True)
    file_path = StringField(required=True)
    is_valid = BooleanField(default=False)
    invalid_reason = StringField()
    is_processed = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

class Receipt(Document):
    purchased_at = StringField()
    merchant_name = StringField()
    total_amount = StringField()
    file_path = StringField()
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
