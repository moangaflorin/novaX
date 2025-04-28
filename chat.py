from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request
from fastapi.templating import Jinja2Templates
from database import Database
import json
from typing import Dict
import traceback
import asyncio

# Initialize router
router = APIRouter()

# Initialize templates
templates = Jinja2Templates(directory="templates")

# Store active WebSocket connections
connected_clients: Dict[str, WebSocket] = {}

# Track disconnection timeouts to handle page refreshes
disconnect_timers: Dict[str, asyncio.Task] = {}

@router.get("/chat")
async def chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@router.get("/api/messages")
async def get_messages(limit: int = 50, room_id: str = "general"):
    """API endpoint to get message history"""
    messages = await Database.get_message_history(limit, room_id)
    return {"messages": messages}

@router.get("/api/connections")
async def get_connections():
    """API endpoint to check active WebSocket connections"""
    return {
        "connections": len(connected_clients),
        "clients": list(connected_clients.keys())
    }

async def broadcast_message(data: str, exclude_user_id: str = None):
    """Broadcast a message to all connected clients except the sender"""
    disconnected_clients = []
    
    for client_id, client_socket in connected_clients.items():
        if client_id != exclude_user_id:
            try:
                await client_socket.send_text(data)
                print(f"Message broadcast to {client_id}")
            except Exception as e:
                print(f"Error broadcasting to {client_id}: {e}")
                disconnected_clients.append(client_id)
    
    # Clean up disconnected clients
    for client_id in disconnected_clients:
        if client_id in connected_clients:
            del connected_clients[client_id]

async def handle_delayed_disconnect(username: str):
    """
    Handle user disconnect with a delay to avoid notifications during page refreshes.
    This function is called when a user disconnects and waits for a set time before
    sending a disconnect notification. If the user reconnects during this period,
    the notification is cancelled.
    """
    try:
        # Wait for a short time to see if the user reconnects (like during a page refresh)
        await asyncio.sleep(3)
        
        # If we get here and the user hasn't reconnected, send the disconnect notification
        if username not in connected_clients:
            # Notify other users that this user has disconnected
            disconnection_msg = json.dumps({
                "sender": "System",
                "text": f"{username} has left the chat",
                "timestamp": 0,  # Special timestamp to identify system messages
                "type": "system"
            })
            await broadcast_message(disconnection_msg)
            print(f"Sent disconnect notification for {username}")
    except Exception as e:
        print(f"Error in delayed disconnect for {username}: {e}")
    finally:
        # Clean up the timer reference
        if username in disconnect_timers:
            del disconnect_timers[username]

@router.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    # Check if user is already connected
    if username in connected_clients:
        # Close the existing connection
        try:
            old_connection = connected_clients[username]
            await old_connection.close(code=1000, reason="Logged in from another session")
            print(f"Closed previous connection for {username}")
        except Exception as e:
            print(f"Error closing previous connection for {username}: {e}")
    
    # Cancel any pending disconnect notification if the user is reconnecting
    if username in disconnect_timers:
        disconnect_timers[username].cancel()
        del disconnect_timers[username]
        print(f"Cancelled disconnect timer for {username} - this appears to be a page refresh")
        reconnect = True
    else:
        reconnect = False
    
    # Accept the new connection
    await websocket.accept()
    connected_clients[username] = websocket
    print(f"New client connected: {username}. Total clients: {len(connected_clients)}")
    
    try:
        # Send message history to the newly connected client
        message_history = await Database.get_message_history()
        await websocket.send_json({"type": "history", "messages": message_history})
        print(f"Sent message history to {username}")
        
        # Only notify others if this is not a reconnect during page refresh
        if not reconnect:
            # Notify other users that this user has connected
            connection_msg = json.dumps({
                "sender": "System",
                "text": f"{username} has joined the chat",
                "timestamp": 0,  # Special timestamp to identify system messages
                "type": "system"
            })
            await broadcast_message(connection_msg, username)
        
        # Handle incoming messages
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            print(f"Received message from {username}: {message_data['text']}")
            
            # Save message to database
            await Database.save_message(message_data)
            
            # Broadcast the message to all connected clients except the sender
            await broadcast_message(data, username)
    except WebSocketDisconnect:
        print(f"Client disconnected: {username}")
        if username in connected_clients:
            del connected_clients[username]
            
            # Schedule a delayed disconnect notification
            # This allows for reconnection during page refreshes without notifications
            disconnect_task = asyncio.create_task(handle_delayed_disconnect(username))
            disconnect_timers[username] = disconnect_task
            
    except Exception as e:
        print(f"Error in websocket connection for {username}: {e}")
        traceback.print_exc()
        if username in connected_clients:
            del connected_clients[username] 