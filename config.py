from dataclasses import dataclass
from environs import Env

@dataclass
class TgBot:
    token: str
    canal_id: int


@dataclass
class DataManagement:
    period_time: int
    height: str
    data_file_name: str
    negative_change: int


@dataclass
class Config:
    tg_bot: TgBot
    data: DataManagement


def load_config(path: str) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN'),
            canal_id=int(env('CANAL_ID'))
        ),
        data=DataManagement(
            period_time=int(env('TIME')),
            height=int(env('HEIGHT')),
            data_file_name=env('DATA_FILE_NAME'),
            negative_change=int(env('NEGATIVE_CHANGE'))
        )
    )