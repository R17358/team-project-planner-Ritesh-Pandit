from user import UserManager
from team import TeamManager
from project_board import ProjectBoard
import json


def user_menu():
    um = UserManager()

    while True:
        print("\n--- USER MENU ---")
        print("1. Create User")
        print("2. List Users")
        print("3. Describe User")
        print("4. Update User")
        print("5. Get User Teams")
        print("0. Back to Main Menu")
        
        choice = input("Enter choice: ")

        if choice == "1":
            name = input("Enter name: ")
            display_name = input("Enter display name: ")
            req = json.dumps({"name": name, "display_name": display_name})
            print(um.create_user(req))

        elif choice == "2":
            print(um.list_users())

        elif choice == "3":
            uid = input("Enter user id: ")
            req = json.dumps({"id": uid})
            print(um.describe_user(req))

        elif choice == "4":
            uid = input("Enter user id: ")
            name = input("Enter new name: ")
            display_name = input("Enter new display name: ")
            req = json.dumps({
                "id": uid,
                "user": {"name": name, "display_name": display_name}
            })
            print(um.update_user(req))

        elif choice == "5":
            uid = input("Enter user id: ")
            req = json.dumps({"id": uid})
            print(um.get_user_teams(req))

        elif choice == "0":
            break
        else:
            print("Invalid choice")


def team_menu():
    tm = TeamManager()

    while True:
        print("\n--- TEAM MENU ---")
        print("1. Create Team")
        print("2. List Teams")
        print("3. Describe Team")
        print("4. Update Team")
        print("5. Add Users to Team")
        print("6. Remove Users from Team")
        print("7. List Team Users")
        print("0. Back to Main Menu")

        choice = input("Enter choice: ")

        if choice == "1":
            name = input("Enter team name: ")
            desc = input("Enter description: ")
            admin = input("Enter admin user id: ")
            req = json.dumps({"name": name, "description": desc, "admin": admin})
            print(tm.create_team(req))

        elif choice == "2":
            print(tm.list_teams())

        elif choice == "3":
            tid = input("Enter team id: ")
            req = json.dumps({"id": tid})
            print(tm.describe_team(req))

        elif choice == "4":
            tid = input("Enter team id: ")
            name = input("Enter new name: ")
            desc = input("Enter new description: ")
            admin = input("Enter new admin user id: ")
            req = json.dumps({
                "id": tid,
                "team": {"name": name, "description": desc, "admin": admin}
            })
            print(tm.update_team(req))

        elif choice == "5":
            tid = input("Enter team id: ")
            users = input("Enter user IDs (comma separated): ").split(",")
            req = json.dumps({"id": tid, "users": users})
            print(tm.add_users_to_team(req))

        elif choice == "6":
            tid = input("Enter team id: ")
            users = input("Enter user IDs (comma separated): ").split(",")
            req = json.dumps({"id": tid, "users": users})
            print(tm.remove_users_from_team(req))

        elif choice == "7":
            tid = input("Enter team id: ")
            req = json.dumps({"id": tid})
            print(tm.list_team_users(req))

        elif choice == "0":
            break
        else:
            print("Invalid choice")


def project_board_menu():
    pb = ProjectBoard()

    while True:
        print("\n--- PROJECT BOARD MENU ---")
        print("1. Create Board")
        print("2. Close Board")
        print("3. Add Task")
        print("4. Update Task Status")
        print("5. List Boards")
        print("6. Export Board")
        print("0. Back to Main Menu")

        choice = input("Enter choice: ")

        if choice == "1":
            name = input("Enter board name: ")
            desc = input("Enter description: ")
            team_id = input("Enter team id: ")
            req = json.dumps({"name": name, "description": desc, "team_id": team_id})
            print(pb.create_board(req))

        elif choice == "2":
            bid = input("Enter board id: ")
            req = json.dumps({"id": bid})
            print(pb.close_board(req))

        elif choice == "3":
            title = input("Enter task title: ")
            desc = input("Enter task description: ")
            user_id = input("Enter assigned user id: ")
            board_id = input("Enter board id: ")
            req = json.dumps({
                "title": title,
                "description": desc,
                "user_id": user_id,
                "board_id": board_id
            })
            print(pb.add_task(req))

        elif choice == "4":
            tid = input("Enter task id: ")
            status = input("Enter status (OPEN/IN_PROGRESS/COMPLETE): ")
            req = json.dumps({"id": tid, "status": status})
            print(pb.update_task_status(req))

        elif choice == "5":
            uid = input("Enter user id: ")
            req = json.dumps({"id": uid})
            print(pb.list_boards(req))

        elif choice == "6":
            bid = input("Enter board id: ")
            req = json.dumps({"id": bid})
            print(pb.export_board(req))

        elif choice == "0":
            break
        else:
            print("Invalid choice")


def main():
    while True:
        print("\n=== PROJECT MANAGEMENT SYSTEM ===")
        print("1. User Operations")
        print("2. Team Operations")
        print("3. Project Board Operations")
        print("0. Exit")

        choice = input("Enter choice: ")

        try:
            if choice == "1":
                user_menu()
            elif choice == "2":
                team_menu()
            elif choice == "3":
                project_board_menu()
            elif choice == "0":
                print("Exiting... Goodbye!")
                break
            else:
                print("Invalid option! Please try again.")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
