# Project Management System (User, Team & Board Manager)

A lightweight Python-based project management backend to handle **Users**, **Teams**, and **Boards** with Tasks.  
It uses simple JSON files as a database for storing data, making it easy to test and run without external dependencies.

---

## 📌 Features

### User Management
- Create, list, describe, and update users
- Retrieve all teams a user belongs to

### Team Management
- Create, list, describe, and update teams
- Add/remove users from a team (max 50 users)
- List all users in a team

### Board & Task Management
- Create project boards for teams
- Add tasks to boards
- Update task statuses
- Close boards (only when all tasks are complete)
- Export a board to a `.txt` file for reporting

---

## 🛠 Requirements

- Python **3.10+**
- No external libraries are required (only standard Python modules).

---

## 📂 Project Structure

```bash

project/
│
├── user.py # UserManager class
├── team.py # TeamManager class
├── project_board.py # ProjectBoard class
├── user_base.py # UserBase class
├── team_base.py # TeamBase class
├── project_board_base.py # ProjectBoardBase class
├── main.py # Example usage / testing
├── db/
│ ├── users.json # User data storage
│ ├── teams.json # Team data storage
│ └── boards.json # Board & task storage
├── out/ # Board exports
│
├── requirements.txt
└── README.md
```
---

## 🚀 How to Run

1. **Clone the repository**
```bash

git clone https://github.com/R17358/team-project-planner-Ritesh-Pandit.git
cd project

```

2. **Create Folders in project -> db/ and out/**

3. **Install and run**

```bash

pip install -r requirements.txt
python main.py

```


