from dataclasses import dataclass

from environs import Env


@dataclass
class DbConfig:
    user: str
    password: str
    database: str
    host: str
    port: int = 3306

@dataclass
class Config:
    db: DbConfig


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        db=DbConfig(
            user=env.str('DB_USER'),
            password=env.str('DB_PASS'),
            database=env.str('DB_NAME'),
            host=env.str('DB_HOST'),
            port=env.int("DB_PORT")
        )
    )


