"""
Column mapping definitions for legacy -> crm.customers migration.
"""

COLUMN_MAPPING = {
    "client_id": "_source_system_id",
    "email": "email",
    "phone": "phone_number",
    "registration_date": "registration_date",
    "account_status": "is_active",
}

SPLIT_COLUMNS = {"full_name": ("first_name", "last_name")}
