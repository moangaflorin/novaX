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
