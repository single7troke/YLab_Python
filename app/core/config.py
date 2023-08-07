from pydantic_settings import BaseSettings, SettingsConfigDict


class Postgres(BaseSettings):
    user: str
    password: int
    db: str
    host: str = 'db'
    port: int = 5432

    def url(self):
        return f'postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}'

    model_config = SettingsConfigDict(env_prefix='postgres_')


class RedisSettings(BaseSettings):
    host: str = 'localhost'
    port: int = 6379
    proto: str = 'redis'
    expire: int = 60

    class Config:
        env_prefix = 'redis_'

    def url(self):
        return f'{self.proto}://{self.host}:{str(self.port)}'


class Config(BaseSettings):
    app_name: str = 'Menu Service'
    postgres: Postgres = Postgres()
    redis: RedisSettings = RedisSettings()
