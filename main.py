from config import Config, load_config
from bot import BotBybit

from os import path

import logging
import logging.handlers

def main():

    logger = logging.getLogger("parser")
    logger.setLevel(logging.INFO)

    handler = logging.handlers.TimedRotatingFileHandler('parser_tg_bot.log', when="W0", interval=1, backupCount=1)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    
    logger.addHandler(handler)

    try:
        config: Config = load_config(path.join('.env'))
    except:
        config: Config = load_config(path.join('bots', '.env'))

    bot = BotBybit(config=config)

    bot.run()


if __name__ == '__main__':
    main()