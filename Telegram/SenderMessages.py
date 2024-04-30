import aiogram
from aiogram.client import bot

class SendMessange:
    def __init__(self):
        self.__Bot = None

    def SetBot(self, Bot: aiogram.client.bot):
        self.__Bot = Bot

    async def SendMessageFromPeople(self, mes: str, ID):
        await self.__Bot.send_message(chat_id=ID, text=mes)
