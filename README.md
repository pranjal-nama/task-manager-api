# 📝 Task Manager API

A simple Flask-based Task Manager API that supports user authentication with JWT and full CRUD operations on tasks.

---

## 🚀 Project Overview

- User registration & login
- JWT-based authentication
- CRUD operations for tasks
- Task fields: `id`, `title`, `description`, `status`, `user_id`, `created_time`
- Users can only access their own tasks

---

## ⚙️ Local Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/pranjal-nama/task-manager-api.git
cd task-manager-api
```

### 2. Create a virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # For Windows
# OR
source venv/bin/activate  # For Mac/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the server

```bash
flask run
```

🌍 Deployed API
Base URL: 

📮 Postman Collection
🔗 Click to open Postman Collection

📘 API Endpoints
All routes require a JWT token:
```bash
Authorization: Bearer <your_token_here>
```

🧑 Authentication
POST /api/auth/register – Register a user
POST /api/auth/login – Login and receive JWT

✅ Task Management
POST /api/tasks/create – Create a task
GET /api/tasks/all – Get all tasks
PUT /api/tasks/update/<task_id> – Update a task
DELETE /api/tasks/delete/<task_id> – Delete a task
