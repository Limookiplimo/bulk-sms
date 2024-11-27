from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """
    Application configuration class. Reads environment variables for sensitive data.
    """

    cr_db_username: str = Field(..., env="CR_DB_USERNAME")
    cr_db_password: str = Field(..., env="CR_DB_PASSWORD")
    cr_db_host: str = Field(..., env="CR_DB_HOST")
    cr_db_port: int = Field(..., env="CR_DB_PORT")
    cr_db_name: str = Field(..., env="CR_DB_NAME")
    africastalking_username: str = Field(..., env="AFRICASTALKING_USERNAME")
    africastalking_sender: str = Field(..., env="AFRICASTALKING_SENDER")
    africastalking_api_key: str = Field(..., env="AFRICASTALKING_API_KEY")

    model_config = SettingsConfigDict(
        env_file=".env"
    )  # Specify the location of the environment file
