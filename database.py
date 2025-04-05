from db_config import get_db_connection

conn = get_db_connection()
                                            
cursor = conn.cursor()

cursor.execute("SELECT user_id, email, username FROM users WHERE username = %s", ("Test",))


user = cursor.fetchone()
if user:
    print("User found:", user)
else:
    print("User not found.")

cursor.close()
conn.close()
