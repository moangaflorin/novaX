#!/usr/bin/env python
"""
Simple WebSocket client for testing the chat application.
This script connects to the WebSocket server and allows sending messages from the command line.
"""

import asyncio
import json
import sys
import websockets
import uuid
from datetime import datetime

async def receive_messages(websocket):
    """Receive and display messages from the WebSocket server"""
    try:
        while True:
            message = await websocket.recv()
            data = json.loads(message)
            
            if 'type' in data and data['type'] == 'history':
                print("\n--- Message History ---")
                for msg in data['messages']:
                    timestamp = datetime.fromtimestamp(msg['timestamp']/1000).strftime('%H:%M:%S')
                    print(f"[{timestamp}] {msg['sender']}: {msg['text']}")
                print("--- End of History ---\n")
            else:
                timestamp = datetime.fromtimestamp(data['timestamp']/1000).strftime('%H:%M:%S')
                print(f"\n[{timestamp}] {data['sender']}: {data['text']}")
            
            print("> ", end="", flush=True)
    except websockets.exceptions.ConnectionClosed:
        print("\nConnection to the server closed")
    except Exception as e:
        print(f"\nError in receiving messages: {e}")

async def send_messages(websocket, user_id):
    """Send messages from the command line to the WebSocket server"""
    try:
        print("Type your messages (press Enter to send, Ctrl+C to exit):")
        while True:
            print("> ", end="", flush=True)
            message = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
            message = message.strip()
            
            if message:
                message_data = {
                    "sender": user_id,
                    "text": message,
                    "timestamp": int(datetime.now().timestamp() * 1000)
                }
                await websocket.send(json.dumps(message_data))
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"\nError in sending messages: {e}")

async def main():
    user_id = f"User_{uuid.uuid4().hex[:8]}"
    print(f"Connecting as: {user_id}")
    
    uri = f"ws://localhost:8000/ws/{user_id}"
    
    try:
        async with websockets.connect(uri) as websocket:
            print(f"Connected to {uri}")
            
            # Create tasks for receiving and sending messages
            receive_task = asyncio.create_task(receive_messages(websocket))
            send_task = asyncio.create_task(send_messages(websocket, user_id))
            
            # Run both tasks concurrently
            await asyncio.gather(receive_task, send_task)
    except websockets.exceptions.ConnectionError:
        print(f"Could not connect to {uri}. Is the server running?")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 