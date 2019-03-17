from concurrent.futures import ThreadPoolExecutor

from dingtalkchatbot.chatbot import DingtalkChatbot
from wxpy import Bot, embed


class Robot:
    def __init__(self):
        pass

    def send_text(self, msg):
        raise NotImplementedError


class DingTalkRobot(Robot):
    def __init__(self, webhook):
        self.bot = DingtalkChatbot(webhook)
        super().__init__()

    def send_text(self, msg):
        self.bot.send_text(msg, is_at_all=True)


class WechatRobot(Robot):
    def __init__(self, chat_names):
        bot = Bot(console_qr=True, cache_path=True)
        self.chats = bot.search(chat_names)
        super().__init__()

    def send_text(self, msg):
        for chat in self.chats:
            chat.send_msg(msg)

    @staticmethod
    def run_embed():
        ThreadPoolExecutor(1).submit(embed)
