INSERT INTO users (id, email, name)
VALUES ('00000000-0000-0000-0000-000000000001', 'test@example.com', 'Test User')
ON CONFLICT (id) DO NOTHING;
