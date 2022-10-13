from .models import *


def search_author(id_):
    try:
        return Author.select().where(Author.author_id == id_).get()
    except Author.DoesNotExist:
        return None


def add_new_author(author):
    Author.create(**author.__dict__)


def get_all_chat():
    return Chat.select()


def add_new_chat(chat):
    Chat.create(**chat.__dict__)


def add_new_message(messages): ...
    # Message.create(**messages.__dict__)
