from pydantic import BaseModel


class SmsBase(BaseModel):
    """
    Schema for SMS data input.
    """

    sms_text: str  # The SMS message text
    source: str  # The database table to fetch phone numbers from
