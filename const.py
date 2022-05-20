TYPE_PHOTO = 'Photo'
TYPE_LINK = 'Link'
TYPE_PHONE_CALL = 'PhoneCall'
TYPE_GEO = 'GeoPosition'
TYPE_CONTACT = 'Contact'
TYPE_CIRCULAR_VIDEO = "CircularVideo"
TYPE_VIDEO = 'Video'
TYPE_GIF = "GIF"
TYPE_MUSIC = "Music"
TYPE_VOICE_MES = "VoiceMessage"
TYPE_STICKER = 'Sticker'
TYPE_PHOTO_FILE = 'PhotoFile'
TYPE_PDF = 'PDF'
TYPE_VIDEO_FILE = 'VideoFile'
TYPE_FILE = 'File'
TYPE_TEXT = 'Text'
TYPE_ERROR_FILE = 'ErrorTypeFile'

LOAD_FILE = {TYPE_PHOTO: True,
             TYPE_CIRCULAR_VIDEO: True,
             TYPE_VIDEO: True,
             TYPE_MUSIC: True,
             TYPE_VOICE_MES: True,
             TYPE_PHOTO_FILE: True,
             TYPE_VIDEO_FILE: True,
             TYPE_PDF: True,
             TYPE_FILE: True
             }

DB_NAME = 'Telegram.db'
COLUMN = ["id", "chat_id", "name", "class", "phone", "tag", "status", "active"]
ENTRY_CHECK = "SELECT * FROM chat WHERE chat_id = {}"
ADD_NOTE_CHAT = "INSERT INTO chat(chat_id, name, class, phone, tag, status, active) VALUES (?, ?, ?, ?, ?, ?, ?) ON CONFLICT DO NOTHING;"
CHANNEL_DB = """
CREATE TABLE IF NOT EXISTS chat(
id INTEGER PRIMARY KEY AUTOINCREMENT,
chat_id INTEGER UNIQUE NOT NULL,
name TEXT,
class TEXT NOT NULL,
phone INTEGER,
tag TEXT,
status INTEGER NOT NULL,
active INTEGER NOT NULL);"""
UPDATE_NOTE = "UPDATE chat SET name=?, class=?, phone=?, tag=?, status=? WHERE id = {}"
GET_CHANNEL_ID = "SELECT chat_id FROM chat"
UPDATE_STATUS = "UPDATE chat SET status=0 WHERE chat_id = {}"
CREATE_CHAT_LOG = """
CREATE TABLE IF NOT EXISTS chat_log_{}(
id INTEGER PRIMARY KEY AUTOINCREMENT,
message_id INTEGER UNIQUE NOT NULL,
author TEXT NOT NULL,
author_id INTEGER NOT NULL,
real_author TEXT,
real_author_id TEXT,
text_message TEXT,
message BLOB,
time TIME NOT NULL,
id_stack INTEGER,
type TEXT NOT NULL,
redacted INTEGER NOT NULL,
deleted INTEGER NOT NULL,
redacted_message TEXT);"""
ADD_CHAT_MESSAGE = """
INSERT INTO chat_log_{}(message_id, author, author_id, real_author, real_author_id, text_message, message, time, id_stack, type, redacted, deleted, redacted_message) 
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
CREATE_AUTHOR = """
CREATE TABLE IF NOT EXISTS author(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
author_id INTEGER NOT NULL,
class TEXT NOT NULL);
"""
ADD_AUTHOR = "INSERT INTO author(name, author_id, class) VALUES (?, ?, ?)"
SELECT_AUTHOR = "SELECT name FROM author WHERE author_id={};"
DETECTED = "SELECT id, active FROM chat WHERE chat_id={}"
SEARCH_TABLE = "SELECT * FROM sqlite_master WHERE  name='chat_log_{}';"
MESSAGE_DELETE = "UPDATE chat_log_{} SET deleted=1 WHERE id = {}"
MESSAGE_UPDATE = "UPDATE chat_log_{} SET redacted=1, redacted_message='{}' WHERE id = {}"
ALL_MESSAGE = "SELECT id, message_id, text_message, type FROM chat_log_{}"
