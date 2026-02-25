from pathlib import Path
import pandas as pd
import numpy as np
import random
from faker import Faker
from loguru import logger


# ------------------------

SEED = 42
RECORDS_COUNT = 5_000
CWD = Path.cwd()
DIR = CWD / Path("data/raw")
FILE_NAME = "customer_dump.csv"
OUTPUT = DIR / FILE_NAME

ACCOUNT_STATUS_OPTIONS = [0, 1, "Y", "N", "Active"]
ACCOUNT_STATUS_PROBS = [0.15, 0.5, 0.05, 0.2, 0.1]


# ------------------------

random.seed(SEED)
np.random.seed(SEED)
fake = Faker()
fake.seed_instance(SEED)

DIR.mkdir(exist_ok=True)

# ------------------------


def generate_dirty_date() -> str | None:
    """
    Generate random date format with 1% chance of None
    """
    date_format = random.choice(["%Y-%m-%d", "%d/%m/%Y", "%d.%m.%Y"])

    if random.random() < 0.01:
        return None

    return fake.date(pattern=date_format, end_datetime="+80w")


def generate_dirty_phone() -> str | None:
    """
    Generate phone number with 5% chance of None
    """
    if random.random() < 0.05:
        return None

    return fake.basic_phone_number()


_emails_cache = []


def generate_email_with_duplicates() -> str:
    """
    Create random email with chance of duplicates
    """
    if (len(_emails_cache) > 0) and (random.random() < 0.1):
        return random.choice(_emails_cache)
    email = fake.email()
    _emails_cache.append(email)
    return email


def generate_account_status() -> str | int:
    return np.random.choice(ACCOUNT_STATUS_OPTIONS, p=ACCOUNT_STATUS_PROBS)


# ------------------------


def main(n: int) -> None:
    logger.info(f"Generating {n} records...")
    customers = []

    for i in range(n):
        record = {
            "client_id": i + 1000,
            "full_name": fake.name(),
            "email": generate_email_with_duplicates(),
            "phone": generate_dirty_phone(),
            "registration_date": generate_dirty_date(),
            "account_status": generate_account_status(),
        }

        customers.append(record)

    df = pd.DataFrame(customers)
    df.to_csv(OUTPUT, index=False, sep=";")
    logger.success(f"Done: {OUTPUT}")


if __name__ == "__main__":
    main(RECORDS_COUNT)
