# SMS Promotion Service
## Overview
The SMS Promotion Service is a FastAPI-based application for sending promotional SMS messages to a list of customers retrieved from a database. It integrates with Africa's Talking SMS API to deliver messages in batches. The application ensures efficient database interaction, phone number validation, and secure configuration management.

## Features
- **Phone Number Validation:** Ensures only valid Kenyan phone numbers are used.
- **Batch SMS Sending:** Sends SMS messages in batches for efficient delivery.
- **Database Integration:** Fetches customer phone numbers from a specified database table.
- **Secure Configuration:** Manages sensitive data like API keys and database credentials using environment variables.
- **REST API Endpoint:** A single API endpoint for sending SMS messages.
- **CORS Support:** Enables cross-origin requests for broader accessibility.

## Tech Stack
- **Backend Framework:** FastAPI
- **Database:** MySQL with SQLAlchemy ORM
- **Messaging API:** Africa's Talking
- **Environment Management:** Pydantic
- **Phone Number Validation:** phonenumbers

## Project Structure
```
├── database.py         # Handles database connection and session management.
├── config.py           # Manages application settings and environment variables.
├── crud.py             # Contains core business logic for SMS sending.
├── schemas.py          # Defines the data models for the application.
├── serving.py          # Defines the FastAPI application and routes.
├── .env                # Environment variables file (not included in version control).
└── README.md           # Project documentation.
```

## Setup Instructions
### Prerequisites
- Python 3.10 or later
- MySQL database
- Africa's Talking account for SMS services

### Installation
1. Clone the Repository
```
git clone <repository_url>
cd sms-promotion-service
```
2. Set Up a Virtual Environment
```
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

3. Install Dependencies
```
pip install -r requirements.txt
```

4. Configure Environment Variables Create a .env file in the project root with the following content:
```
CR_DB_USERNAME=<your_database_username>
CR_DB_PASSWORD=<your_database_password>
CR_DB_HOST=<your_database_host>
CR_DB_PORT=<your_database_port>
CR_DB_NAME=<your_database_name>
AFRICASTALKING_USERNAME=<your_africastalking_username>
AFRICASTALKING_API_KEY=<your_africastalking_api_key>
AFRICASTALKING_SENDER=<your_sms_sender_id>
```

5. Run the Application
```
uvicorn serving:app --reload
```

## Usage
### API Endpoint
**Endpoint:** `/send/sms`
**Method:** `POST`
**Request Body:**
```
{
    "sms_text": "Hello, this is a promotional message!",
    "source": "customers_table"
}
```

**Response:**
```
{
    "status": "success",
    "message": SMS sent successfully
}
```

### Sample Workflow
1. Add phone numbers to your MySQL database in the specified table.
2. Use the `/send/sms`endpoint to send a promotional message to customers.
3. Check the logs for batch SMS delivery results.

## Development Notes
- **Phone Number Validation:** Uses the phonenumbers library to ensure phone numbers are valid and in the correct format.
- **Batch Processing:** Sends SMS messages in chunks of 100 numbers to optimize API usage and reduce latency.
- **Error Handling:** Logs errors during database queries or SMS sending to facilitate debugging.

## Future Enhancements
- **Multi-Country Support:** Add support for validating and formatting phone numbers from other countries.
- **Message Scheduling:** Allow scheduling SMS messages for later delivery.
- **Detailed Reporting:** Include delivery status for each SMS in the response.
- **Frontend Dashboard:** Create a web interface for managing campaigns and tracking performance.

## Contribution Guidelines
1. Fork the repository and create a new branch.
2. Make your changes and test thoroughly.
3. Submit a pull request with a detailed explanation of your changes.

## Support
For any issues or questions, contact me via  [email](devdrice@gmail.com) or [twitter](https://x.com/limoo_kiplimo).
