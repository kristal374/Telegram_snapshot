LOAD_FILE = {'File': False, 'Video': False, 'Photo': False}

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
author TEXT NOT NULL,
author_id INTEGER NOT NULL,
real_author TEXT,
real_author_id TEXT,
text_message TEXT,
message BLOB,
time TIME NOT NULL,
id_stack INTEGER,
type TEXT NOT NULL,
deleted INTEGER NOT NULL);"""
ADD_CHAT_MESSAGE = """
INSERT INTO chat_log_{}(author, author_id, real_author, real_author_id, text_message, message, time, id_stack, type, deleted) 
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
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
