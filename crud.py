from phonenumbers import parse, is_valid_number, NumberParseException
from sqlalchemy.orm import Session
from functools import lru_cache
from datetime import datetime
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
    Fetch and validate phone numbers from the specified database table.

    Args:
        db (Session): Database session.
        source (str): Name of the table containing phone numbers.

    Returns:
        list[str]: List of formatted and valid phone numbers.
    """
    phone_numbers = fetch_phone_numbers(db, sms_data.source)

    if not phone_numbers:
        logging.warning("No valid phone numbers found.")
        return

    message = f"{sms_data.sms_text}"
    batch_size = 100  # Send SMS in batches of 100

    response_received_at = datetime.now().strftime("%Y%m%d%H%M%S")
    response_received_at = datetime.now().strftime("%Y%m%d%H%M%S")
    response_code = f"SMS-{response_received_at}"

    for i in range(0, len(phone_numbers), batch_size):
        batch = phone_numbers[i : i + batch_size]

        try:
            response_dict = sms.send(message, batch, sender)
            logging.info("Batch sent successfully: %s", response_dict)
            serialized_response = str(response_dict)
            insert_sms_query = text(
                """
                insert into test_sms (response_code, response_dict, response_received_at)
                values (:response_code, :response_dict, :response_received_at)
                on duplicate key update
                    response_code=values(response_code),
                    response_dict=values(response_dict),
                    response_received_at=values(response_received_at);
                """
            )

            db.execute(
                insert_sms_query,
                {
                    "response_code": response_code,
                    "response_dict": serialized_response,
                    "response_received_at": response_received_at,
                },
            )
            db.commit()

        except Exception as e:
            logging.error("Error sending SMS batch: %s", e)


def sms_report(db: Session):
    """
    Fetch from database table.

    Args:
        db (Session): Database session.

    Returns:
        list[str]: List of sms report.
    """
    fetch_query = text(
        """
        select 
            response_code,
            response_dict,
            response_received_at
        from test_sms
        order by response_received_at desc
        """
    )
    result = db.execute(fetch_query).fetchall()
    if not result:
        logging.info("No SMS reports found.")
        return []

    sms_reports = []
    for row in result:
        response_code = row.response_code
        response_received_at = row.response_received_at
        response_dict = row.response_dict

        # Deserialize the response_dict back into a Python dictionary
        response_data = eval(response_dict)

        # Extract SMS message data
        message_data = response_data.get("SMSMessageData", {})
        message = message_data.get("Message", "No message")
        recipients = message_data.get("Recipients", [])

        # Format recipients' statuses
        recipient_details = []
        total_cost = 0.0

        for recipient in recipients:
            cost = float(recipient.get("cost", "0"))
            total_cost += cost
            recipient_details.append(
                {
                    "number": recipient.get("number", "Unknown"),
                    "status": recipient.get("status", "Unknown"),
                    "statusCode": recipient.get("statusCode", "Unknown"),
                    "cost": f"{cost:.2f}",
                }
            )

        sms_reports.append(
            {
                "response_code": response_code,
                "response_received_at": response_received_at,
                "message": message,
                "total_cost": f"{total_cost:.2f}",
                "recipients": recipient_details,
            }
        )

    return sms_reports
