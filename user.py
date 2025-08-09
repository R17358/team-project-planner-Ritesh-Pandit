from user_base import UserBase
import os
import json
import uuid
import datetime

class UserManager(UserBase):

    def __init__(self, db_path="db/users.json"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        try:
            with open(self.db_path, "r") as f:
                json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            with open(self.db_path, "w") as f:
                f.write("[]")


    # create a user
    def create_user(self, request: str) -> str:
        data = json.loads(request)
        name = data["name"]
        display_name = data["display_name"]

        if len(name)>64 or len(display_name)>64:
            raise ValueError("Name or Display Name is too long")
        
        with open(self.db_path, "r") as f:
            users = json.load(f)

        for user in users:
            if user["name"]==name:
                raise ValueError("User already exists with same name")
            
        date_time = datetime.datetime.now().isoformat()
            
        description = f"{name} ({display_name}) joined on {date_time}"
        
        user_id = str(uuid.uuid4())

        user_data = {
            "id": user_id,
            "name": name,
            "display_name": display_name,
            "description": description,
            "creation_time": date_time
        }

        users.append(user_data)

        with open(self.db_path, "w") as f:
            json.dump(users, f, indent=2)

        return json.dumps({"id": user_id})
    
    def list_users(self) -> str:
        try:
            with open(self.db_path, "r") as f:
                users = json.load(f)

            filtered_users = []
            for user in users:
                obj = {
                    "name":user["name"],
                    "display_name":user["display_name"],
                    "creation_time":user["creation_time"]
                }
                filtered_users.append(obj)           
            return json.dumps(filtered_users, indent=2)
        except Exception as e:
            raise RuntimeError(f"Failed to read users: {e}")

    def describe_user(self, request: str) -> str:
        data = json.loads(request)
        id = data["id"]
       
        try:
            with open(self.db_path, "r") as f:
                records = json.load(f)

            found = False

            for record in records:
                if record["id"] == id:
                    description = record["description"]
                    name = record["name"]
                    creation_time = record["creation_time"]
                    
                    found = True
                    break

            if not found:
                raise RuntimeError("There is no record with this id")


            return json.dumps({"name":name,
                               "description":description,
                               "creation_time":creation_time
                               })

        except Exception as e:
            raise RuntimeError(f"Failed to update user: {e}")

            
    
    def update_user(self, request: str) -> str:
        data = json.loads(request)
        id = data["id"]
        name = data["user"]["name"]
        display_name = data["user"]["display_name"]

        if len(name) > 64:
            raise ValueError("Name can not be greater than 64 characters")

        if len(display_name) > 128:
            raise ValueError("Display name can not be greater than 128 characters")

        try:
            with open(self.db_path, "r") as f:
                records = json.load(f)

            updated = False

            for record in records:
                if record["id"] == id:
                    if record["name"] != name:
                        raise RuntimeError("Name can not be updated")
                    record["display_name"] = display_name
                    updated = True
                    break

            if not updated:
                raise RuntimeError("There is no record with this id")

            with open(self.db_path, "w") as f:
                json.dump(records, f, indent=2)

            return json.dumps({"id": id, "message": "User Updated Successfully"})

        except Exception as e:
            raise RuntimeError(f"Failed to update user: {e}")


    def get_user_teams(self, request: str) -> str:
        
        data = json.loads(request)
        user_id = data["id"]

        team_db_path = "db/teams.json"
        if not os.path.exists(team_db_path):
            raise RuntimeError("No teams database found")

        with open(team_db_path, "r") as f:
            teams = json.load(f)

        user_teams = []
        for team in teams:
            # Check if 'users' key exists and contains this user
            if "users" in team and user_id in team["users"]:
                user_teams.append({
                    "name": team["name"],
                    "description": team["description"],
                    "creation_time": team["creation_time"]
                })

        return json.dumps(user_teams, indent=2)

            
            
        

            
        
