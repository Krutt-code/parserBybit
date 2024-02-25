from config import Config, load_config
from bot import BotBybit

from os import path

def main():
    config: Config = load_config(path.join('parserBybit', '.env'))

    bot = BotBybit(config=config)

    bot.run()


if __name__ == '__main__':
    main()