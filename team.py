from team_base import TeamBase
import json
import os
import datetime
import uuid

class TeamManager(TeamBase):

    def __init__(self, db_path="db/teams.json"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

        try:
            with open(self.db_path, "r") as f:
                json.load(f)
        except Exception as e:
            with open(self.db_path, "w") as f:
                f.write("[]")

    def create_team(self, request: str) -> str:
        data = json.loads(request)

        # Required fields check
        if "name" not in data or "description" not in data or "admin" not in data:
            raise ValueError("Missing required fields: name, description, admin")

        name = data["name"].strip()
        description = data["description"].strip()
        admin_id = data["admin"].strip()

        # Constraints
        if len(name) > 64:
            raise ValueError("Team name cannot be more than 64 characters")

        if len(description) > 128:
            raise ValueError("Description cannot be more than 128 characters")

        with open(self.db_path, "r") as f:
            team_records = json.load(f)

        # Unique team name check
        for record in team_records:
            if record["name"].lower() == name.lower():
                raise RuntimeError(f"Team '{name}' already exists")

        team_id = str(uuid.uuid4())

        team_data = {
            "id": team_id,
            "name": name,
            "description": description,
            "admin": admin_id,
            "creation_time": datetime.datetime.now().isoformat()
        }

        team_records.append(team_data)

        with open(self.db_path, "w") as f:
            json.dump(team_records, f, indent=2)

        return json.dumps({"id": team_id})

    def list_teams(self) -> str:
        
        try:
            with open(self.db_path, "r") as f:
                teams = json.load(f)

            filtered_team_data= []
            
            for team in teams:
                obj = {
                    "name":team["name"],
                    "description":team["description"],
                    "creation_time":team["creation_time"],
                    "admin":team["admin"]
                }

                filtered_team_data.append(obj)
            
            return json.dumps(filtered_team_data, indent=2)
        except Exception as e:
            raise RuntimeError(f"Failed to fetch teams {e}")
        
    def describe_team(self, request: str) -> str:
        data = json.loads(request)

        if "id" not in data:
            raise ValueError("Missing required field: id")

        team_id = data["id"]

        with open(self.db_path, "r") as f:
            teams = json.load(f)

        for team in teams:
            if team["id"] == team_id:
                
                obj = {
                    "name": team["name"],
                    "description": team["description"],
                    "creation_time": team["creation_time"],
                    "admin": team["admin"]
                }
                return json.dumps(obj, indent=2)

        raise RuntimeError(f"No team found with id {team_id}")
    
    def update_team(self, request: str) -> str:
        data = json.loads(request)

        if "id" not in data or "team" not in data:
            raise ValueError("Missing required fields: 'id' and 'team'")

        team_id = data["id"]
        team_data = data["team"]

        name = team_data.get("name", "").strip()
        description = team_data.get("description", "").strip()
        admin_id = team_data.get("admin", "").strip()

        if len(name) > 64:
            raise ValueError("Team name can not be more than 64 characters")

        if len(description) > 128:
            raise ValueError("Description can not be more than 128 characters")

        with open(self.db_path, "r") as f:
            teams = json.load(f)

        updated = False

        for team in teams:
            if team["id"] == team_id:
                
                if team["name"] != name:
                    for other in teams:
                        if other["id"] != team_id and other["name"] == name:
                            raise RuntimeError("Team name already exists")
                    team["name"] = name

                team["description"] = description
                team["admin"] = admin_id
                updated = True
                break

        if not updated:
            raise RuntimeError(f"No team found with id {team_id}")

        with open(self.db_path, "w") as f:
            json.dump(teams, f, indent=2)

        return json.dumps({"id": team_id, "message": "Team updated successfully"})
    
    def add_users_to_team(self, request: str):
        data = json.loads(request)

        if "id" not in data or "users" not in data:
            raise ValueError("Missing required fields: 'id' and 'users'")

        team_id = data["id"]
        new_users = data["users"]

        if not isinstance(new_users, list):
            raise ValueError("'users' must be a list")

        with open(self.db_path, "r") as f:
            teams = json.load(f)

        updated = False

        for team in teams:
            if team["id"] == team_id:
                
                if "users" not in team:
                    team["users"] = []

                # Combine old and new users without duplicates
                combined_users = list(set(team["users"] + new_users))

                if len(combined_users) > 50:
                    raise RuntimeError("Cannot have more than 50 users in a team")

                team["users"] = combined_users
                updated = True
                break

        if not updated:
            raise RuntimeError(f"No team found with id {team_id}")

        with open(self.db_path, "w") as f:
            json.dump(teams, f, indent=2)

        return json.dumps({"id": team_id, "message": "Users added successfully"})

    def remove_users_from_team(self, request: str):
        data = json.loads(request)

        if "id" not in data or "users" not in data:
            raise ValueError("Missing required fields: 'id' and 'users'")

        team_id = data["id"]
        remove_users = data["users"]

        if not isinstance(remove_users, list):
            raise ValueError("'users' must be a list")

        with open(self.db_path, "r") as f:
            teams = json.load(f)

        updated = False

        for team in teams:
            if team["id"] == team_id:
                if "users" not in team:
                    team["users"] = []

                # Remove specified users
                team["users"] = [u for u in team["users"] if u not in remove_users]

                updated = True
                break

        if not updated:
            raise RuntimeError(f"No team found with id {team_id}")

        with open(self.db_path, "w") as f:
            json.dump(teams, f, indent=2)

        return json.dumps({"id": team_id, "message": "Users removed successfully"})

    def list_team_users(self, request: str):
        data = json.loads(request)

        if "id" not in data:
            raise ValueError("Missing required field: 'id'")

        team_id = data["id"]

        # Read teams
        with open(self.db_path, "r") as f:
            teams = json.load(f)

        team_found = None
        for team in teams:
            if team["id"] == team_id:
                team_found = team
                break

        if not team_found:
            raise RuntimeError(f"No team found with id {team_id}")

        if "users" not in team_found or not team_found["users"]:
            return json.dumps([])  

        user_db_path = "db/users.json"  # same path used in UserManager
        if not os.path.exists(user_db_path):
            raise RuntimeError("Users database not found")

        with open(user_db_path, "r") as f:
            all_users = json.load(f)

        # Filter only users present in this team
        team_users_info = []
        for uid in team_found["users"]:
            for user in all_users:
                if user["id"] == uid:
                    team_users_info.append({
                        "id": user["id"],
                        "name": user["name"],
                        "display_name": user["display_name"]
                    })
                    break

        return json.dumps(team_users_info, indent=2)



