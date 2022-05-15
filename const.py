DB_NAME = 'Telegram.db'
COLUMN = ["id", "chat_id", "name", "class", "phone", "tag", "status", "active"]
ENTRY_CHECK = "SELECT * FROM chat WHERE chat_id = {}"
ADD_NOTE_CHAT = "INSERT INTO chat(chat_id, name, class, phone, tag, status, active) VALUES (?, ?, ?, ?, ?, ?, ?);"
CHANNEL_DB = """
CREATE TABLE IF NOT EXISTS chat(
id INTEGER PRIMARY KEY AUTOINCREMENT,
chat_id INTEGER NOT NULL,
name TEXT,
class TEXT NOT NULL,
phone INTEGER,
tag TEXT,
status TEXT NOT NULL,
active TEXT NOT NULL);"""
UPDATE_NOTE = "UPDATE chat SET name='{}', class='{}', phone={}, tag='{}', status='{}' WHERE id = {}"
GET_CHANNEL_ID = "SELECT chat_id FROM chat"
UPDATE_STATUS = "UPDATE chat SET status=0 WHERE chat_id = {}"
