from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    datebase_hostname: str
    datebase_port: str
    datebase_passoword: str
    datebase_name: str
    datebase_username: str
    secret_key: str
    algorihm: str
    expire: int

    class Config:
        env_file = ".env"


settings = Settings()
