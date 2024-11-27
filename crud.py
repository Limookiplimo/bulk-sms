from phonenumbers import parse, is_valid_number, NumberParseException
from sqlalchemy.orm import Session
from functools import lru_cache
from sqlalchemy import text
import africastalking
import logging
import config
import schemas

logging.basicConfig(level=logging.INFO)


@lru_cache
def get_settings():
    """
    Retrieve the application settings using an LRU cache for optimization.
    """
    return config.Settings()


# Initialize Africa's Talking SMS service
settings = get_settings()
africastalking.initialize(
    settings.africastalking_username, settings.africastalking_api_key
)
sms = africastalking.SMS
sender = settings.africastalking_sender


def is_valid_kenyan_number(number: str) -> bool:
    """
    Check if a phone number is a valid Kenyan number.

    Args:
        number (str): Phone number to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    try:
        phone = parse(number, "KE")
        return is_valid_number(phone)
    except NumberParseException:
        return False


def format_phone_number(number: str) -> str:
    """
    Format a phone number to international format (+254).

    Args:
        number (str): Phone number to format.

    Returns:
        str: Formatted phone number.
    """
    if number.startswith("+"):
        return number
    return f'+254{number.lstrip("0")}'


def fetch_phone_numbers(db: Session, source: str) -> list[str]:
    """
    Fetch and validate phone numbers from the specified database table.

    Args:
        db (Session): Database session.
        source (str): Name of the table containing phone numbers.

    Returns:
        list[str]: List of formatted and valid phone numbers.
    """
    query = text(f"select phone_number from {source};")
    try:
        users_data = db.execute(query).mappings().all()
        return [
            format_phone_number(user["phone_number"])
            for user in users_data
            if is_valid_kenyan_number(user["phone_number"])
        ]
    except Exception as e:
        logging.error("Error fetching phone numbers: %s", e)
        return []


def send_sms(db: Session, sms_data: schemas.SmsBase):
    """
    Send SMS messages in batches to phone numbers fetched from the database.

    Args:
        db (Session): Database session.
        sms_data (schemas.SmsBase): SMS content and source table.

    Returns:
        None
    """
    phone_numbers = fetch_phone_numbers(db, sms_data.source)

    if not phone_numbers:
        logging.warning("No valid phone numbers found.")
        return

    message = f"{sms_data.sms_text}"
    batch_size = 100  # Send SMS in batches of 100

    for i in range(0, len(phone_numbers), batch_size):
        batch = phone_numbers[i : i + batch_size]
        try:
            response = sms.send(message, batch, sender)
            logging.info("Batch sent successfully: %s", response)
        except Exception as e:
            logging.error("Error sending SMS batch: %s", e)
