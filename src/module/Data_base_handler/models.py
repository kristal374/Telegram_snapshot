from peewee import *
from src.module.const import *
from src.settings import Global

Global.db = SqliteDatabase(DB_NAME)


class BaseModel(Model):
    id = AutoField(primary_key=True, null=False)

    class Meta:
        database = Global.db
        order_by = "id"

    def __str__(self):
        return str(self.__data__)


class Message(BaseModel):
    chat_id = IntegerField(unique=True)
    message_id = IntegerField(unique=True)
    author = TextField()
    author_id = IntegerField()
    real_author = TextField(null=True)
    real_author_id = IntegerField(null=True)
    text_message = TextField(null=True)
    message = BlobField(null=True)
    message_extension = TextField(null=True)
    time = DateTimeField()
    id_stack = IntegerField(null=True)
    type = TextField()
    redacted = BooleanField()
    deleted = BooleanField()


class EditMessage(Message):
    date_edit = DateTimeField()

    class Meta:
        db_table = "edit_message"


class Chat(BaseModel):
    chat_id = IntegerField(unique=True)
    name = TextField(null=True)
    category = CharField(max_length=7, column_name="class")
    phone = IntegerField(null=True)
    tag = CharField(max_length=32, null=True)
    photo = BlobField(null=True)
    bio = TextField()
    status = BooleanField()
    active = BooleanField()


class ChatHistory(BaseModel):
    chat_id = IntegerField()
    name = TextField(null=True)
    category = CharField(max_length=7, column_name="class")
    phone = IntegerField(null=True)
    tag = CharField(max_length=32, null=True)
    photo = BlobField(null=True)
    bio = TextField()
    status = BooleanField()
    active = BooleanField()
    date_edit = DateTimeField()

    class Meta:
        db_table = "change_history_preview"


class Author(BaseModel):
    name = TextField(null=True)
    author_id = IntegerField(unique=True)
    category = CharField(max_length=7, column_name="class")


class Version(Model):
    version = IntegerField()

    class Meta:
        database = Global.db