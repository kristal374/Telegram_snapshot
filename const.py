DB_NAME = 'Telegram.db'
ENTRY_CHECK = "SELECT * FROM chat WHERE chat_id = {}"
ADD_NOTE_CHAT = "INSERT INTO chat(chat_id, name, class, phone, tag, status) VALUES ({}, '{}', '{}', {}, '{}', '{}')"
