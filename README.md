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
- **Development:** VS Code Dev Container (recommended)

## 🚀 Getting Started

### Option A: Development Container (Recommended)

The easiest way to get started is using VS Code with the development container:

1. Install [VS Code](https://code.visualstudio.com/) and [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
2. Clone and open the repository in VS Code
3. Press `Ctrl+Shift+P` → "Dev Containers: Reopen in Container"
4. Start development: `./dev.sh`
5. Access:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

For more details about the development container setup, see the [Dev Container README](./.devcontainer/README.md).

### Option B: Manual Setup

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

## 🧪 Testing

The backend includes automated tests written with `pytest` (covering services, storage, and API behavior).

Run the backend test suite:

```bash
cd backend
pytest -q
```

## 📁 Project Structure

```
polish-peaks/
├── README.md          # Project overview and setup guide
├── .devcontainer/     # VS Code development container configuration
│   └── README.md      # Development container setup guide
├── dev.sh             # Development helper script
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
