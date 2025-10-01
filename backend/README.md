# 🏔️ Polish Peaks - Backend

This is the backend API for the Polish Peaks project, built with FastAPI (Python).

## 🛠️ Tech Stack

- **Framework:** FastAPI (Python)
- **Database:** PostgreSQL (or SQLite for development)
- **Python Version:** 3.8+

## 🚀 Setup & Installation

### 1. Navigate to the backend directory

```bash
cd backend
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Upgrade pip

```bash
python3 -m pip install --upgrade pip
```

### 4. Install dependencies

```bash
pip3 install "fastapi[standard]"
```

## 🏃‍♂️ Running the Backend

Start the FastAPI development server:

```bash
python3 -m fastapi dev main.py
```

The API will be available at:

- **API**: http://localhost:8000
- **Interactive API Docs (Swagger)**: http://localhost:8000/docs
- **Alternative API Docs (ReDoc)**: http://localhost:8000/redoc
