# 🏔️ Polish Peaks

**Polish Peaks** is a personal portfolio project designed to provide a central place to store and view photos from mountain summits across Poland. The main goal of the project is to allow users to upload summit photos and keep them organized in one place, tracking their climbing achievements.

> This project is inspired by the idea of completing all major Polish summits, but it is a personal project and not affiliated with or endorsed by any official organization.

## ✨ Main Idea

- Store summit photos in one place
- Organize photos by summit
- Keep a personal record of climbing achievements
- Track progress toward completing all major summits

## 🛠️ Tech Stack

- **Frontend:** Next.js (React, TypeScript, Tailwind CSS)
- **Backend:** FastAPI (Python)
- **Database:** PostgreSQL (or SQLite for development)
- **Containerization:** Docker (optional, for easy local setup)

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/dawstr8/polish-peaks.git
cd polish-peaks
```

### 2. Backend Setup

For detailed backend setup instructions, see the [Backend README](./backend/README.md).

Quick start:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip3 install "fastapi[standard]"
python3 -m fastapi dev main.py
```

### 3. Frontend Setup

For detailed frontend setup instructions, see the [Frontend README](./frontend/README.md).

Quick start:

```bash
cd frontend
npm install
npm run dev
```

## 📁 Project Structure

```
polish-peaks/
├── README.md          # Project overview and setup guide
├── backend/           # FastAPI backend application
│   └── README.md      # Backend development documentation
└── frontend/          # Next.js frontend application
    └── README.md      # Frontend development documentation
```

This is a full-stack web application with a clear separation between frontend and backend components. Each component has its own dedicated documentation for development setup and guidelines.

## ⚡ Contribution

This is a personal portfolio project. Contributions are welcome in the form of suggestions, feedback, or ideas, but core development is done by the author.

## 👤 Author

**Dawid Strojek**

- Portfolio: https://www.linkedin.com/in/dawid-strojek/
- GitHub: https://github.com/dawstr8
- Email: dawid.strojek@gmail.com
