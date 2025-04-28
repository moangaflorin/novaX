# 🔐 Secure Chatroom App

A secure real-time chatroom application built with **FastAPI** and **PostgreSQL**, designed as part of a final exam project. It includes authentication with hashed passwords, a chatroom interface, and planned features like password recovery and two-factor authentication (2FA).

## 🚀 Features

- User registration & login
- Secure password hashing using `bcrypt`
- Basic frontend using Jinja2 templates
- CORS middleware configured for frontend-backend communication
- Upcoming: Password reset, Chatroom interface with session-based access & 2FA

## ⚙️ Tech Stack

- **Backend**: FastAPI
- **Database**: PostgreSQL (`psycopg2`) & Redis
- **Frontend**: HTML/CSS (Jinja2 templates)
- **Security**: bcrypt, CORS, input handling

## 🛠️ Local Setup

### Prerequisites

- Python 3.11+
- PostgreSQL & Redis
- Virtual environment (`venv`)

### Clone & Install

```bash
git clone https://github.com/moangaflorin/novaX.git
cd novaX

python -m venv env
source env/bin/activate  # or .\env\Scripts\activate on Windows

pip install -r requirements.txt

```

## Project Structure

The application is organized using an Object-Oriented Programming (OOP) approach for better maintainability:

```
├── main.py             # Main application entry point
├── models.py           # Data models using Pydantic
├── database.py         # Database interactions
├── auth.py             # Authentication routes
├── chat.py             # Chat and WebSocket functionality
├── db_config.py        # Database connection configuration
├── static/             # Static files (CSS, JS)
│   └── js/
│       └── chat.js     # Client-side chat functionality
└── templates/          # HTML templates
    ├── login.html
    ├── register.html
    └── chat.html
```

## Features

- User registration and authentication
- Real-time chat using WebSockets
- Message persistence in PostgreSQL database
- Message history retrieval

## Setup

1. Make sure PostgreSQL is installed and running
2. Create a database for the application
3. Create a `config.json` file with your database configuration:
   ```json
   {
     "dbname": "your_db_name",
     "user": "your_db_user",
     "host": "localhost",
     "port": 5432
   }
   ```
4. Set the `db_password` environment variable
5. Install dependencies: `pip install -r requirements.txt`
6. Run the application: `uvicorn main:app --reload`

## API Endpoints

- **GET /**  - Login page
- **GET /register** - Registration page
- **GET /chat** - Chat interface
- **POST /login** - User login
- **POST /register** - User registration
- **GET /api/messages** - Get message history
- **WebSocket /ws/{user_id}** - WebSocket connection for real-time chat

## WebSocket Protocol

The WebSocket communication uses JSON messages with the following format:

```json
{
  "sender": "username",
  "text": "message content",
  "timestamp": 1621234567890
}
```

When a client connects, they receive message history in the format:

```json
{
  "type": "history",
  "messages": [
    {
      "sender": "user1",
      "text": "message 1",
      "timestamp": 1621234567000
    },
    {
      "sender": "user2",
      "text": "message 2",
      "timestamp": 1621234567890
    }
  ]
}
```



## 🛠️ Local Setup

### Prerequisites

- Python 3.11+
- PostgreSQL & Redis
- Virtual environment (`venv`)

### Clone & Install

```bash
git clone https://github.com/moangaflorin/novaX.git
cd novaX

python -m venv env
source env/bin/activate  # or .\env\Scripts\activate on Windows

pip install -r requirements.txt
