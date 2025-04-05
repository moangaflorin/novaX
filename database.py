from db_config import get_db_connection

# Get a connection to the database
conn = get_db_connection()
                                            
# Now you can interact with the database
cursor = conn.cursor()

# Example query to fetch a user
cursor.execute("SELECT user_id, email, username FROM users WHERE username = %s", ("Test",))

# Fetch and print the result
user = cursor.fetchone()
if user:
    print("User found:", user)
else:
    print("User not found.")

# Close the connection when done
cursor.close()
conn.close()
