from Telegram import TelegramBot
import asyncio


if __name__ == '__main__':
    Bot = TelegramBot.TelegramBot()
    asyncio.run(Bot.main())
