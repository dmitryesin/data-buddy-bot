CREATE TABLE users (
    id INT PRIMARY KEY,
    language TEXT NOT NULL
);

CREATE TABLE user_questions (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    question JSONB NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);