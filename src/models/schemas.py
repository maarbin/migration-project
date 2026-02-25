from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import date


class CustomerRecord(BaseModel):
    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    first_name: str
    last_name: str
    email: str
    phone_number: str | None
    registration_date: date | None
    is_active: bool
    source_system_id: int | None = Field(alias="_source_system_id")

    @field_validator("email")
    @classmethod
    def check_mail(cls, value):
        if "@" not in value:
            raise ValueError("Email does not contain @.")
        return value
