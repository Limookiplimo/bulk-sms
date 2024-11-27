from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import db_connection
import schemas
import crud

app = FastAPI()

# Allow CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/send/sms", response_model=dict)
def send_promotional_message(
    sms_data: schemas.SmsBase, db: Session = Depends(db_connection)
):
    """
    Endpoint to send promotional SMS messages.

    Args:
        sms_data (schemas.SmsBase): SMS content and source table.
        db (Session): Database session.

    Returns:
        dict: Status of the operation.
    """
    crud.send_sms(db, sms_data)
    return {"status": "success", "message": "SMS sent successfully"}
