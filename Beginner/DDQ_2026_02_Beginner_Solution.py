"""
DataDevQuest - DDQ2026_02
Challenged By: Jordan Woods
Level: Beginner
Created By: Le Luu

Objective: Familiarize yourself with VizQL Data Service, and connect and execute a query to a published data source.
Description: 
Use the filter by Category to keep only Furniture and Technology.
"""
import pandas as pd
import json
import tableauserverclient as TSC
from dotenv import load_dotenv
import os 

#List all users on the site with id, fullname, user_name, site_role, domain and groups
def list_all_users(PAT_NAME, PAT_SECRET, SERVER_ADDRESS, SITE_ID):
    tableau_auth = TSC.PersonalAccessTokenAuth(token_name=PAT_NAME, personal_access_token=PAT_SECRET, site_id=SITE_ID)
    server = TSC.Server(SERVER_ADDRESS, use_server_version=True)

    with server.auth.sign_in(tableau_auth):
        all_users, pagination_item = server.users.get()
        print(f"\nFound {pagination_item.total_available} user(s) on site: {SERVER_ADDRESS}/{SITE_ID}")

        user_list = []
        for user in all_users:
            server.users.populate_groups(user)
            user_list.append({"id": user.id,
                              "full_name": user.fullname,
                              "user_name": user.name,                               
                              "site_role": user.site_role,
                              "domain": user.domain_name,
                              "groups": [group.name for group in user.groups]})
    return user_list

def user_add(PAT_NAME, PAT_SECRET, SERVER_ADDRESS, SITE_ID, list_users_to_add_df):
    tableau_auth = TSC.PersonalAccessTokenAuth(token_name=PAT_NAME, personal_access_token=PAT_SECRET, site_id=SITE_ID)
    server = TSC.Server(SERVER_ADDRESS, use_server_version=True)

    with server.auth.sign_in(tableau_auth):
        # users_to_add = []
        for row in list_users_to_add_df.itertuples():
            user1= TSC.UserItem(name=row.username, site_role=row.license_level)
            # users_to_add.append(user1)
            print(f"\nUser {user1.name} with site role {user1.site_role} added to the list of users to be added.")
            server.users.add(user1)

def user_remove(PAT_NAME, PAT_SECRET, SERVER_ADDRESS, SITE_ID, users_to_remove_df):
    tableau_auth = TSC.PersonalAccessTokenAuth(token_name=PAT_NAME, personal_access_token=PAT_SECRET, site_id=SITE_ID)
    server = TSC.Server(SERVER_ADDRESS, use_server_version=True)

    with server.auth.sign_in(tableau_auth):
        for row in users_to_remove_df.itertuples():
            server.users.remove(row.id)
            print(f"\n==> User {row.user_name} was removed from the site.")

# def list_all_groups(PAT_NAME, PAT_SECRET, SERVER_ADDRESS, SITE_ID):
#     tableau_auth = TSC.PersonalAccessTokenAuth(token_name=PAT_NAME, personal_access_token=PAT_SECRET, site_id=SITE_ID)
#     server = TSC.Server(SERVER_ADDRESS, use_server_version=True)

#     with server.auth.sign_in(tableau_auth):
#         all_groups, pagination_item = server.groups.get()
#         #Create an index for the list of groups
#         group_list = []
#         for group in all_groups:
#             group_list.append({"group_id": group.id,
#                               "group_name": group.name})
#     return group_list

def user_updates(PAT_NAME, PAT_SECRET, SERVER_ADDRESS, SITE_ID, list_users_to_add_df):
    tableau_auth = TSC.PersonalAccessTokenAuth(token_name=PAT_NAME, personal_access_token=PAT_SECRET, site_id=SITE_ID)
    server = TSC.Server(SERVER_ADDRESS, use_server_version=True)

    with server.auth.sign_in(tableau_auth):

        user_name_to_update = input("\nEnter the username of the user you want to update: ")

        all_users, _ = server.users.get()

        user_to_update = next((user for user in all_users if user.name == user_name_to_update), None)

        if user_to_update is None:
            print(f"User {user_name_to_update} not found on the site.")
            return
        
        while True:
            print("\nWould you like to update:")
            print("1. Site Role")
            print("2. Add User to a Group")
            print("3. Remove a User from a Group")
            print("4. Exit")

            selection = input("Enter the number corresponding to your choice: ")

            if selection == "1":
                site_roles = {
                    "1": "Viewer",
                    "2": "Creator",
                    "3": "ExploreCanPublish",
                    "4": "Unlicensed",
                    "5": "ReadOnly"
                }
                print("\nAvailable site roles:")
                for key, value in site_roles.items():
                    print(f"{key}. {value}")
                role_selection = input("Enter the number corresponding to the site role you want to assign: ")
                if role_selection in site_roles:
                    user_to_update.site_role = site_roles[role_selection]
                    server.users.update(user_to_update)
                    print(f"==> User {user_to_update.name} - site role updated to {user_to_update.site_role}")

                else:
                    print("Invalid selection. Please try again.")

            elif selection == "2":
                server.users.populate_groups(user_to_update)
                if not user_to_update.groups:
                    print(f"\n==> User {user_to_update.name} is not currently in any groups.")
                    all_groups, pagination_item = server.groups.get()

                    print("\nAvailable groups:")

                    group_list = []
                    for group in all_groups:
                        group_list.append({"name": group.name, "id": group.id})
                    groups_df = pd.DataFrame(group_list)
                    print(groups_df)

                    group_name = input("\nEnter the name of the group to add the user to: ")

                    # find the selected group
                    group = next((g for g in all_groups if g.name == group_name), None)

                    if group:
                        server.groups.add_user(group, user_to_update.id)
                        print(f"User {user_to_update.name} added to group {group.name}")
                        
                    else:
                        print("Group not found.")

                else:
                    print(f"\n==> User {user_to_update.name} is currently in the following groups:")
                    for group in user_to_update.groups:
                        print(group.name)
                    print(f"\nWould you like to add user {user_to_update.name} to another group?")
                    add_to_group_selection = input("Enter y for yes, n for no:")
                    if add_to_group_selection.lower() == "y":
                        all_groups, pagination_item = server.groups.get()

                        print("\nAvailable groups:")

                        group_list = []
                        for group in all_groups:
                            group_list.append({"name": group.name, "id": group.id})
                        groups_df = pd.DataFrame(group_list)
                        print(groups_df)

                        group_name = input("\nEnter the name of the group to add the user to: ")

                        # find the selected group
                        group = next((g for g in all_groups if g.name == group_name), None)

                        if group:
                            server.groups.add_user(group, user_to_update.id)
                            print(f"\n==> User {user_to_update.name} was added to group {group.name}")
                            
                        else:
                            print("Group not found.")

            elif selection == "3":
                server.users.populate_groups(user_to_update)
                if not user_to_update.groups:
                    print(f"\n==> User {user_to_update.name} is not currently in any groups.")
                else:
                    print(f"\n==> User {user_to_update.name} is currently in the following groups:")
                    for group in user_to_update.groups:
                        print(group.name)

                    group_name = input("\nEnter the name of the group to remove the user from: ")

                    group = next((g for g in user_to_update.groups if g.name == group_name), None)

                    if group:
                        server.groups.remove_user(group, user_to_update.id)
                        print(f"\n==> User {user_to_update.name} was removed from group {group.name}")
                    else:
                        print("Group not found.")

            elif selection == "4":
                print("Exiting...")
                break
            else:
                print("Invalid selection. Please try again.")

def main():
    print("================================================")
    print("=== DataDevQuest - 2026_02 - Beginner        ===")
    print("=== Challenged by: Jordan Woods              ===")
    print("=== Solved by: Le Luu                        ===")
    print("================================================")
    print()

    load_dotenv()

    #Load credentials data from .env file
    PAT_NAME = os.getenv("PAT_NAME")
    PAT_SECRET = os.getenv("PAT_SECRET")
    SERVER_ADDRESS = os.getenv("SERVER_ADDRESS")
    SITE_ID = os.getenv("SITE_ID")
    CSV_PATH = os.getenv("CSV_PATH")
    #All users currently on the site
    all_users = list_all_users(PAT_NAME, PAT_SECRET, SERVER_ADDRESS, SITE_ID)
    current_users_df = pd.DataFrame(all_users)
    print(current_users_df)


    list_users_to_add_df = pd.read_csv(CSV_PATH)
    print("\n=================================================")
    print("Users from the CSV file to add:")
    print(list_users_to_add_df)
    print("=================================================")

    #check if the users in the csv file already exist on the site
    users_to_add_df = list_users_to_add_df[list_users_to_add_df["username"].isin(current_users_df["user_name"])]
    #if a user already existed on the site, update the info or remove the user
    if len(users_to_add_df) > 0: 
        print("\n=================================================")
        print("These users already exist on the site:", users_to_add_df)
        print("\nWould you like to update the user info or remove them from the site?")
        print("1. Update user info")
        print("2. Remove user from the site")

        selection = input("Enter the number corresponding to your choice: ")
        if selection == "1":
            print("=================================================")
            print("==========    UPDATE USER PROFILE      ==========")
            print("=================================================")
            user_updates(PAT_NAME, PAT_SECRET, SERVER_ADDRESS, SITE_ID, users_to_add_df)

            print("\n=================================================")
            print("List of users on the site after updating user info:")
            users_list = list_all_users(PAT_NAME, PAT_SECRET, SERVER_ADDRESS, SITE_ID)
            current_users_df = pd.DataFrame(users_list)
            print(current_users_df)

        elif selection == "2":
            print("\n=================================================")
            print("==========    REMOVE USER FROM SITE    ==========")
            print("=================================================")

            users_list = list_all_users(PAT_NAME, PAT_SECRET, SERVER_ADDRESS, SITE_ID)
            current_users_df = pd.DataFrame(users_list)
            print(current_users_df)

            #Choose the user to remove from the list
            selected_users_to_remove = input("\nEnter the index of the users you want to remove from the site, separated by commas: ")
            selected_users_to_remove = [int(index.strip()) for index in selected_users_to_remove.split(",")]
            users_to_remove_df = current_users_df[current_users_df.index.isin(selected_users_to_remove)]
            
            print(f"\n==> Users {users_to_remove_df['user_name'].tolist()} selected to be removed")
            # print(users_to_remove_df)
            user_remove(PAT_NAME, PAT_SECRET, SERVER_ADDRESS, SITE_ID, users_to_remove_df)
            print("\n=================================================")

            users_list = list_all_users(PAT_NAME, PAT_SECRET, SERVER_ADDRESS, SITE_ID)
            current_users_df = pd.DataFrame(users_list)
            print(current_users_df)

    #else add the new user to the site
    else:
        user_add(PAT_NAME, PAT_SECRET, SERVER_ADDRESS, SITE_ID, list_users_to_add_df)
        new_list = list_all_users(PAT_NAME, PAT_SECRET, SERVER_ADDRESS, SITE_ID)
        new_list_df = pd.DataFrame(new_list)
        print("\n=================================================")
        print("New list of users on the site after adding new users:")
        print(new_list_df)
    

if __name__ == "__main__":
    main()