from .models import *


def get_all_chat():
    return Chat.select()


def add_new_chat(chat):
    Chat.create(**chat.__dict__)


def add_new_message(messages):
    Message.create(**messages.__dict__)
