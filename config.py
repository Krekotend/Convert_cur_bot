from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str


@dataclass
class Exchange:
    exc_key: str


@dataclass
class Config:
    tg_bot: TgBot
    e_key: Exchange


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(token=env('BOT_TOKEN')),
                  e_key=Exchange(exc_key=env('EXCHENGE_KEY')))
