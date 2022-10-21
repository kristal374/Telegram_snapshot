from .models import *

Global.db.connect()
with Global.db:
    Global.db.create_tables([Message, EditMessage, Chat, ChatHistory, Author, Version])
