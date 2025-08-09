import json
import os
import uuid
from datetime import datetime
from project_board_base import ProjectBoardBase

class ProjectBoard(ProjectBoardBase):

    def __init__(self, db_path="db/boards.json"):
        self.boards_file = db_path
        os.makedirs(os.path.dirname(self.boards_file), exist_ok=True)

        try:
            with open(self.boards_file, "r") as f:
                json.load(f)
        except Exception as e:
            with open(self.boards_file, "w") as f:
                f.write("[]")

    def _read_boards(self):
        with open(self.boards_file, "r") as f:
            return json.load(f)

    def _write_boards(self, boards):
        with open(self.boards_file, "w") as f:
            json.dump(boards, f, indent=2)

    # create a board
    def create_board(self, request: str):
        data = json.loads(request)
        name = data["name"].strip()
        description = data["description"].strip()
        team_id = data["team_id"]

        if len(name) > 64:
            raise ValueError("Board name exceeds 64 characters")
        if len(description) > 128:
            raise ValueError("Board description exceeds 128 characters")

        boards = self._read_boards()

       
        for b in boards:
            if b["team_id"] == team_id and b["name"].lower() == name.lower():
                raise ValueError("Board name must be unique within a team")

        board_id = str(uuid.uuid4())
        new_board = {
            "id": board_id,
            "name": name,
            "description": description,
            "team_id": team_id,
            "creation_time": data.get("creation_time", datetime.now().isoformat()),
            "status": "OPEN",
            "tasks": []
        }
        boards.append(new_board)
        self._write_boards(boards)
        return json.dumps({"id": board_id})

    # close a board
    def close_board(self, request: str) -> str:
        data = json.loads(request)
        board_id = data["id"]

        boards = self._read_boards()
        for b in boards:
            if b["id"] == board_id:
                if any(task["status"] != "COMPLETE" for task in b["tasks"]):
                    raise ValueError("Cannot close board: All tasks must be COMPLETE")
                b["status"] = "CLOSED"
                b["end_time"] = datetime.now().isoformat()
                self._write_boards(boards)
                return json.dumps({"status": "Board closed"})
        raise ValueError("Board not found")

    # add task to board
    def add_task(self, request: str) -> str:
        data = json.loads(request)
        title = data["title"].strip()
        description = data["description"].strip()
        user_id = data["user_id"]
        board_id = data["board_id"]

        if len(title) > 64:
            raise ValueError("Task title exceeds 64 characters")
        if len(description) > 128:
            raise ValueError("Task description exceeds 128 characters")

        boards = self._read_boards()
        for b in boards:
            if b["id"] == board_id:
                if b["status"] != "OPEN":
                    raise ValueError("Can only add tasks to an OPEN board")
                # Unique title in the same board
                for t in b["tasks"]:
                    if t["title"].lower() == title.lower():
                        raise ValueError("Task title must be unique in a board")
                task_id = str(uuid.uuid4())
                b["tasks"].append({
                    "id": task_id,
                    "title": title,
                    "description": description,
                    "user_id": user_id,
                    "creation_time": data.get("creation_time", datetime.now().isoformat()),
                    "status": "OPEN"
                })
                self._write_boards(boards)
                return json.dumps({"id": task_id})
        raise ValueError("Board not found")

    # update the status of a task
    def update_task_status(self, request: str):
        data = json.loads(request)
        task_id = data["id"]
        new_status = data["status"]

        boards = self._read_boards()
        for b in boards:
            for t in b["tasks"]:
                if t["id"] == task_id:
                    t["status"] = new_status
                    self._write_boards(boards)
                    return json.dumps({"status": "Task updated"})
        raise ValueError("Task not found")

    # list all open boards for a team
    def list_boards(self, request: str) -> str:
        data = json.loads(request)
        team_id = data["id"]

        boards = self._read_boards()
        open_boards = [
            {"id": b["id"], "name": b["name"]}
            for b in boards
            if b["team_id"] == team_id and b["status"] == "OPEN"
        ]
        return json.dumps(open_boards, indent=2)

    # export board
    def export_board(self, request: str) -> str:
        data = json.loads(request)
        board_id = data["id"]

        boards = self._read_boards()
        for b in boards:
            if b["id"] == board_id:
                if not os.path.exists("out"):
                    os.makedirs("out")
                filename = f"out/board_{board_id}.txt"
                with open(filename, "w") as f:
                    f.write(f"Board: {b['name']}\n")
                    f.write(f"Description: {b['description']}\n")
                    f.write(f"Team ID: {b['team_id']}\n")
                    f.write(f"Status: {b['status']}\n")
                    f.write(f"Created: {b['creation_time']}\n")
                    if "end_time" in b:
                        f.write(f"Closed: {b['end_time']}\n")
                    f.write("\nTasks:\n")
                    for t in b["tasks"]:
                        f.write(f"  - {t['title']} [{t['status']}]\n")
                        f.write(f"    Description: {t['description']}\n")
                        f.write(f"    Assigned to: {t['user_id']}\n")
                        f.write(f"    Created: {t['creation_time']}\n\n")
                return json.dumps({"out_file": filename})
        raise ValueError("Board not found")
