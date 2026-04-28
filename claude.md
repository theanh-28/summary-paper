# 🧠 AI Context File – Summary Paper System

---

## 📌 Project Overview

This is a **fullstack web application** for summarizing academic papers.

The system allows users to:

* Upload research papers (PDF, text)
* Generate summaries using NLP/ML models
* Manage saved summaries
* Analyze usage via dashboard (Power BI – integrated later)

---

## 🏗️ System Architecture

### Backend (FastAPI)

* RESTful API
* Handles authentication, business logic, NLP processing

### Frontend (React)

* SPA (Single Page Application)
* Communicates with backend via API

### Future

* Power BI Dashboard for analytics (NOT core logic now)

---

## ⚙️ Tech Stack

### Backend

* FastAPI
* SQLAlchemy (ORM)
* **MySQL**
* Pydantic (validation)
* JWT Authentication

### Frontend

* React
* Axios (API calls)
* React Router
* State management (Context API or Redux)

---

## 🗄️ Database Schema (MySQL)

### User

* id (PK)
* email (unique)
* password (hashed)
* created_at

### Paper

* id (PK)
* user_id (FK -> User.id)
* title
* content
* file_path
* created_at

### Summary

* id (PK)
* paper_id (FK -> Paper.id)
* type (short | detailed)
* content
* created_at

---

## 📂 Backend Structure

```
backend/
├── app/
│   ├── main.py
│   ├── api/                # Route layer
│   ├── schemas/           # Pydantic models
│   ├── models/            # DB models
│   ├── services/          # Business logic
│   ├── repositories/      # DB access
│   ├── core/              # config, security
│   ├── db/                # database
│   ├── utils/             # helpers
│   └── ml/                # summarization logic
```

---

## 📂 Frontend Structure

```
frontend/
├── src/
│   ├── components/
│   ├── pages/
│   ├── services/         # API calls
│   ├── hooks/
│   ├── context/
│   ├── routes/
│   └── utils/
```

---

## 🔐 Authentication Flow

* User registers
* User logs in → receives JWT
* JWT stored in localStorage
* All protected APIs require token

---

## 📊 Core Features (Business Logic)

### 1. User Management

* Register
* Login
* Logout
* Update profile

### 2. Paper Management

* Upload paper (PDF/Text)
* Store metadata:

  * title
  * author (optional)
  * upload date
* Extract text from file

### 3. Summarization

* Input: paper content
* Output:

  * short summary
  * detailed summary
* Support multiple methods:

  * extractive
  * abstractive (optional)

### 4. History

* Save summaries
* View previous summaries
* Delete history

### 5. Search

* Search papers by title/content

---

## 🔄 Business Flow: Summarize Paper

1. User uploads file
2. Backend extracts text
3. Text sent to ML module
4. Summary generated
5. Saved to DB
6. Returned to frontend

---

## 🔌 API Design Rules

* RESTful only
* Use prefix: `/api/v1`
* Use proper HTTP methods:

  * GET
  * POST
  * PUT
  * DELETE

---

## 🌐 API Endpoints

### Auth

* POST /api/v1/auth/register
* POST /api/v1/auth/login

### Papers

* POST /api/v1/papers/upload
* GET /api/v1/papers/
* GET /api/v1/papers/{id}

### Summarization

* POST /api/v1/summarize

### History

* GET /api/v1/history
* DELETE /api/v1/history/{id}

---

## 🧱 Backend Coding Rules

* Use async/await for all endpoints
* DO NOT put business logic in routes
* Services handle logic
* Repositories handle DB queries

---

## 🧠 ML / NLP Rules

* All summarization logic must be inside `/ml`
* Do NOT mix ML logic with API routes
* Model loading must be optimized (load once, reuse)

---

## 🧾 Error Handling

All APIs must return JSON format:

```
{
  "error": true,
  "message": "Error message"
}
```

---

## 🎨 Frontend Rules

* Separate UI and logic
* API calls must go through `/services`
* Do NOT call API directly in components

---

## 🔄 Frontend Flow

1. User interacts with UI
2. Component calls service
3. Service calls backend API
4. Response returned → update UI

---

## 📄 Pages (Frontend)

### Auth Pages

* Login
* Register

### Main Pages

* Dashboard
* Upload Paper
* Summary Result
* History

---

## 🚀 Future Integration (Power BI)

* Visualize:

  * number of summaries
  * user activity
  * popular topics

NOTE: This is NOT required in current implementation.

---

## ⚠️ Rules for AI Code Generation

When generating code:

* ALWAYS follow folder structure
* DO NOT create duplicate logic
* REUSE existing services/models
* KEEP code modular
* KEEP functions small and focused

---

## ❌ Things to Avoid

* Fat controllers (routes doing logic)
* Direct DB access in routes
* Mixing frontend/backend concerns
* Hardcoding values

---

## 🛢️ Database Setup (MySQL)

### Environment Variables (`.env`)

```
DB_HOST=localhost
DB_PORT=3306
DB_NAME=summary_paper
DB_USER=root
DB_PASSWORD=yourpassword

SECRET_KEY=supersecretkey
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

---

### Database Connection (`app/core/database.py`)

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DB_URL = (
    f"mysql+aiomysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

engine = create_async_engine(DB_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
```

---

## 🔄 Alembic (Database Migration)

### Install

```
pip install alembic
```

---

### Init Alembic

```
alembic init alembic
```

---

### Config (`alembic.ini`)

Update DB URL:

```
sqlalchemy.url = mysql+aiomysql://user:password@localhost/db_name
```

---

### Link Models (`alembic/env.py`)

```python
from app.core.database import Base
from app.models import *

target_metadata = Base.metadata
```

---

### Create Migration

```
alembic revision --autogenerate -m "init"
```

---

### Apply Migration

```
alembic upgrade head
```

---

## 🧱 Example Model (SQLAlchemy)

```python
from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
```

---

## 🐳 (Optional) Docker MySQL

```yaml
version: '3.8'
services:
  mysql:
    image: mysql:8.0
    container_name: summary_mysql
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: summary_paper
    ports:
      - "3306:3306"
```

---

## 🗄️ Database Rules

- NEVER use localhost inside Docker
- Always use DB_HOST=db
- Do NOT access DB directly in routes
- Always go through repository layer
- Use async SQLAlchemy only

---

## ⚠️ Rules for AI Code Generation

When generating code:

* ALWAYS follow folder structure
* DO NOT create duplicate logic
* REUSE existing services/models
* KEEP code modular
* KEEP functions small and focused

---

## ❌ Things to Avoid

* Fat controllers (routes doing logic)
* Direct DB access in routes
* Mixing frontend/backend concerns
* Hardcoding values

---

## ✅ Expected Outcome

A clean, scalable fullstack system with:

* Clear separation of concerns
* Maintainable code
* Easy to extend ML features
* Ready for real-world backend practices (MySQL + Alembic)
