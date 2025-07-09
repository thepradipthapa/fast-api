from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database configuration
    db_host: str 
    db_port: int 
    db_user: str 
    db_password: str 
    db_name: str 

    access_token_expire_minutes: int 
    jwt_secret_key: str
    algorithm: str 

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

settings = Settings()