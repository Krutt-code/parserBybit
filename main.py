from config import Config, load_config
from bot import BotBybit


def main():
    config: Config = load_config('/home/kukuruzka-vitya/CODE/botBybit/.env')

    bot = BotBybit(config=config)

    bot.run()


if __name__ == '__main__':
    main()