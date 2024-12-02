from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """
    Application configuration class. Reads environment variables for sensitive data.
    """

    db_username: str = Field(..., env="DB_USERNAME")
    db_password: str = Field(..., env="DB_PASSWORD")
    db_host: str = Field(..., env="DB_HOST")
    db_port: int = Field(..., env="DB_PORT")
    db_name: str = Field(..., env="DB_NAME")
    africastalking_username: str = Field(..., env="AFRICASTALKING_USERNAME")
    africastalking_sender: str = Field(..., env="AFRICASTALKING_SENDER")
    africastalking_api_key: str = Field(..., env="AFRICASTALKING_API_KEY")

    model_config = SettingsConfigDict(
        env_file=".env"
    )  # Specify the location of the environment file
