import os
import pandas as pd
from faker import Faker
import random
from loguru import logger

fake = Faker()
RECORDS_COUNT = 1_000
OUTPUT_FILE = "data/raw/customers_dump.csv"


def generate_dirty_date():
    # Generate random date format with 1% chance of None
    date_format = random.choice(["%Y-%m-%d", "%d/%m/%Y", "%d.%m.%Y"])

    if random.random() < 0.01:
        return None

    return fake.date(pattern=date_format)


def generate_dirty_phone():
    # Generate phone number with 5% chance of None
    if random.random() < 0.05:
        return None

    return fake.basic_phone_number()


if __name__ == "__main__":
    os.makedirs("data/raw", exist_ok=True)
    logger.info(f"Generating {RECORDS_COUNT} records...")

    generated_data = []
    emails_cache = []

    for x in range(RECORDS_COUNT):
        # Create email duplicates
        if (len(emails_cache) > 0) and (random.random() < 0.1):
            email = random.choice(emails_cache)
        else:
            email = fake.email()
            emails_cache.append(email)

        record = {
            "client_id": x + 1000,
            "full_name": fake.name(),
            "email": email,
            "phone": generate_dirty_phone(),
            "date": generate_dirty_date(),
            "account_status": random.choice([0, 1, "Y", "N", "Active"]),
        }

        generated_data.append(record)

        df = pd.DataFrame(generated_data)

        df.to_csv(OUTPUT_FILE, index=False, sep=",")
        logger.success(f"Done: {OUTPUT_FILE}")
