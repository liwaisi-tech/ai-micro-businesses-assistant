"""SQL query templates for conversation-related operations."""

# Conversations table queries
CREATE_CONVERSATIONS_TABLE = """
CREATE TABLE IF NOT EXISTS conversations (
    id SERIAL PRIMARY KEY,
    whatsapp_number VARCHAR(20) NOT NULL UNIQUE,
    start_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP,
    summary TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""

# Messages table queries
CREATE_MESSAGES_TABLE = """
CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""

# Conversation queries
GET_CONVERSATION_BY_ID = """
SELECT * FROM conversations WHERE id = %(id)s;
"""

GET_CONVERSATION_BY_PHONE = """
SELECT * FROM conversations WHERE whatsapp_number = %(whatsapp_number)s;
"""

CREATE_CONVERSATION = """
INSERT INTO conversations (whatsapp_number, summary)
VALUES (%(whatsapp_number)s, %(summary)s)
RETURNING *;
"""

UPDATE_CONVERSATION = """
UPDATE conversations
SET 
    end_time = COALESCE(%(end_time)s, end_time),
    summary = COALESCE(%(summary)s, summary),
    updated_at = CURRENT_TIMESTAMP
WHERE id = %(id)s
RETURNING *;
"""

LIST_ALL_CONVERSATIONS = """
SELECT * FROM conversations ORDER BY start_time DESC;
"""

DELETE_CONVERSATION = """
DELETE FROM conversations WHERE id = %(id)s;
"""

# Message queries
GET_MESSAGE_BY_ID = """
SELECT * FROM messages WHERE id = %(id)s;
"""

CREATE_MESSAGE = """
INSERT INTO messages (conversation_id, role, content)
VALUES (%(conversation_id)s, %(role)s, %(content)s)
RETURNING *;
"""

GET_MESSAGES_BY_CONVERSATION = """
SELECT * FROM messages 
WHERE conversation_id = %(conversation_id)s 
ORDER BY timestamp ASC;
"""

DELETE_MESSAGE = """
DELETE FROM messages WHERE id = %(id)s;
"""

# Index creation
CREATE_CONVERSATION_INDEXES = """
CREATE INDEX IF NOT EXISTS idx_conversations_whatsapp_number ON conversations(whatsapp_number);
CREATE INDEX IF NOT EXISTS idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX IF NOT EXISTS idx_messages_timestamp ON messages(timestamp);
"""
