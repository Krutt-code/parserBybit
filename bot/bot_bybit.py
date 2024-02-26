from aiogram import Bot, Dispatcher
from .manage_data import DataM

import logging
import asyncio



class BotBybit:
    def __init__(self, config) -> None:
        self.config = config
        self.bot = Bot(token=config.tg_bot.token,
                parse_mode='Markdown')
        self.dp = Dispatcher()
        
        self.canal_id = self.config.tg_bot.canal_id
        self.user_task = False

    async def __send_message_to_user(self, data: dict) -> None:
        for mode, item in data.items():

            if not item:
                continue

            message = f'mode {mode}\n'

            for index, item in enumerate(item.items()):
                if index % 10 == 0:
                    message += '```KRIPTA\n'

                name, item = item
                item1, item2 = item.items()
                time1, price1 = item1
                time2, price2 = item2
                change = round(((price2 - price1) / price2) * 100, 1)
                message += f'{name}/USDT {change}%: \n{":".join(time1.split()[:-3:-1][::-1])} = {price1}\n{":".join(time2.split()[:-3:-1][::-1])} = {price2}\n{"#"*30}\n'

                if index % 10 == 9:
                    message += '```'
                    await self.bot.send_message(self.canal_id, message)
            
            if message[:-4:-1] != '```':
                message += '```'
                await self.bot.send_message(self.canal_id, message)

    async def background_task(self):

        logging.basicConfig(filename='telegram_bot.log', level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        while True:
            # Проверяем условие
            if data := DataM(config=self.config).run():
                await self.__send_message_to_user(data=data)
            else:
                pass
                # await self.bot.send_message(self.canal_id, '\[INFO] Нет данных для сравнения')
            await asyncio.sleep(self.config.data.period_time * 60) 

    # Функция конфигурирования и запуска бота
    async def main(self):
        if not self.user_task:
            task = asyncio.create_task(self.background_task())
            self.user_task = True
        # else:
            # await message.answer(text='Бот уже запущен')
        # @self.dp.message(CommandStart())
        # async def process_start_command(message: Message):
        #     await message.answer(text='Начинаю работу')

            await self.bot.delete_webhook(drop_pending_updates=True)
            await self.dp.start_polling(self.bot)

    def run(self):
        asyncio.run(self.main())