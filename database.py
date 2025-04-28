from datetime import datetime
from db_config import get_db_connection
import traceback

class Database:
    @staticmethod
    async def save_message(message: dict):
        """Save message to database"""
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # Convert timestamp from milliseconds to datetime
            timestamp = datetime.fromtimestamp(message["timestamp"]/1000)
            
            cursor.execute(
                "INSERT INTO messages (sender, message_text, timestamp, room_id) VALUES (%s, %s, %s, %s)",
                (message["sender"], message["text"], timestamp, "general")
            )
            conn.commit()
            print(f"Message saved: {message['sender']}: {message['text']}")
        except Exception as e:
            conn.rollback()
            print(f"Error saving message: {e}")
            traceback.print_exc()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    async def get_message_history(limit: int = 50, room_id: str = "general"):
        """Get message history from database"""
        conn = get_db_connection()
        cursor = conn.cursor()
        messages = []
        try:
            cursor.execute(
                "SELECT sender, message_text, timestamp FROM messages WHERE room_id = %s ORDER BY timestamp DESC LIMIT %s",
                (room_id, limit)
            )
            rows = cursor.fetchall()
            for row in rows:
                messages.append({
                    "sender": row[0],
                    "text": row[1],
                    "timestamp": int(row[2].timestamp() * 1000)  # Convert to milliseconds
                })
        except Exception as e:
            print(f"Error retrieving messages: {e}")
            traceback.print_exc()
        finally:
            cursor.close()
            conn.close()
        
        # Return messages in chronological order (oldest first)
        return list(reversed(messages))

    @staticmethod
    def check_user_credentials(username: str, password_bytes: bytes):
        """Check user credentials against database"""
        import bcrypt  # Import here to avoid circular imports
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
            result = cursor.fetchone()
            
            if not result:
                return False
                
            stored_hash = bytes.fromhex(result[0][2:])
            return bcrypt.checkpw(password_bytes, stored_hash)
        except Exception as e:
            print(f"Error checking credentials: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def register_user(email: str, username: str, hashed_password: bytes):
        """Register a new user in the database"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Check if email exists
            cursor.execute("SELECT 1 FROM public.users WHERE email = %s", (email,))
            if cursor.fetchone():
                return "Email already in use."
            
            # Check if username exists
            cursor.execute("SELECT 1 FROM public.users WHERE username = %s", (username,))
            if cursor.fetchone():
                return "Username already taken."
                
            # Insert the new user
            cursor.execute(
                "INSERT INTO public.users (email, username, password) VALUES (%s, %s, %s)",
                (email, username, hashed_password)
            )
            conn.commit()
            return None  # Success
        except Exception as e:
            conn.rollback()
            print(f"Registration error: {e}")
            return "Registration failed due to a server error."
        finally:
            cursor.close()
            conn.close()
            
    @staticmethod
    def initialize_database():
        """Initialize the database with required tables"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Create users table if it doesn't exist
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                email VARCHAR(100) UNIQUE NOT NULL,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(100) NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
            """)
            
            # Recreate messages table with correct timestamp field
            # First check if the table exists
            cursor.execute("""
            SELECT EXISTS (
               SELECT FROM information_schema.tables 
               WHERE table_schema = 'public'
               AND table_name = 'messages'
            );
            """)
            
            table_exists = cursor.fetchone()[0]
            
            if table_exists:
                # Check if we need to update the schema
                cursor.execute("""
                SELECT data_type FROM information_schema.columns 
                WHERE table_name = 'messages' AND column_name = 'timestamp';
                """)
                timestamp_type = cursor.fetchone()[0]
                
                if 'timestamp' not in timestamp_type.lower():
                    # If the type is not a timestamp, drop and recreate
                    print("Recreating messages table with correct timestamp field...")
                    cursor.execute("DROP TABLE messages;")
                    table_exists = False
            
            if not table_exists:
                cursor.execute("""
                CREATE TABLE messages (
                    id SERIAL PRIMARY KEY,
                    sender VARCHAR(100) NOT NULL,
                    message_text TEXT NOT NULL,
                    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
                    room_id VARCHAR(100) DEFAULT 'general'
                );
                """)
                
                # Create indexes
                cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_messages_timestamp ON messages(timestamp);
                """)
                
                cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_messages_room ON messages(room_id);
                """)
            
            conn.commit()
            print("Database initialized successfully.")
        except Exception as e:
            conn.rollback()
            print(f"Error initializing database: {e}")
            traceback.print_exc()
        finally:
            cursor.close()
            conn.close()
