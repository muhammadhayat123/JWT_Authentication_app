# 🛡️ FastAPI JWT Authentication + Todo App

This is a simple FastAPI project with **JWT-based authentication**, where:

- Users **register only once** — no separate login required.
- After registration, a **JWT token** is returned.
- That token must be used to **create todos** securely.

---

## 🚀 Features

- User Registration ✅
- JWT Token generation after registration ✅
- Todo creation (requires valid token) ✅
- Swagger UI for testing ✅

---

## 📦 Requirements

- Python 3.8+
- FastAPI
- SQLAlchemy
- JWT (`pyjwt` or `python-jose`)
- Uvicorn
- dotenv

Install dependencies:

```bash
pip install fastapi uvicorn sqlalchemy python-dotenv pyjwt
