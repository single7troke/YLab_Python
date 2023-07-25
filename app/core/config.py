from pydantic_settings import BaseSettings, SettingsConfigDict


class Postgres(BaseSettings):
    user: str
    password: int
    db: str
    host: str = "db"
    port: int = 5432

    def url(self):
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"

    model_config = SettingsConfigDict(env_prefix="postgres_")


class Config(BaseSettings):
    app_name: str = "Hello"
    postgres: Postgres = Postgres()
