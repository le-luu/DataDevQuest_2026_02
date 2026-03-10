import pandas as pd
import json
import tableauserverclient as TSC
from dotenv import load_dotenv
import os 

# load_dotenv()

#print("PAT name:", PAT_NAME)
#print("PAT secret:", PAT_SECRET)
#print("Server address:", SERVER_ADDRESS)
#print("Site ID:", SITE_ID)
#PAT_NAME = os.getenv("PAT_NAME")
#PAT_SECRET = os.getenv("PAT_SECRET")
#SERVER_ADDRESS = os.getenv("SERVER_ADDRESS")
#SITE_ID = os.getenv("SITE_ID")

# tableau_auth = TSC.PersonalAccessTokenAuth(token_name=PAT_NAME, personal_access_token=PAT_SECRET, site_id=SITE_ID)
# server = TSC.Server(SERVER_ADDRESS, use_server_version=True)

# with server.auth.sign_in(tableau_auth):

#     all_users, pagination_item = server.users.get()

#     print("\nThere are {} users on site".format(pagination_item.total_available))

#     for user in all_users:
#         server.users.populate_groups(user)

#         print(f"\nUser: {user.name}")
#         print("Groups:")
#         for group in user.groups:
#             print(group.name)

# with server.auth.sign_in(tableau_auth):
#     all_users, pagination_item = server.users.get()
#     print("\nThere are {} user on site: ".format(pagination_item.total_available))
#     print([[user.name,user.site_role] for user in all_users])



def list_all_users(PAT_NAME, PAT_SECRET, SERVER_ADDRESS, SITE_ID):
    tableau_auth = TSC.PersonalAccessTokenAuth(token_name=PAT_NAME, personal_access_token=PAT_SECRET, site_id=SITE_ID)
    server = TSC.Server(SERVER_ADDRESS, use_server_version=True)

    with server.auth.sign_in(tableau_auth):
        all_users, pagination_item = server.users.get()
        print(f"\nThere are {pagination_item.total_available} user on site: {SERVER_ADDRESS}/{SITE_ID}")
        #Create an index for the list of users
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

# csv_path = r"C:\Users\LeLuu\Documents\TableauDevQuest\DataDevQuest_Challenges\2026_02\user_list.csv"
# list_users_to_add = pd.read_csv(csv_path)
# print(list_users_to_add)

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
            print(f"\nUser {row.user_name} removed from the site.")

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
        user1= TSC.UserItem(name=list_users_to_add_df["username"], site_role=list_users_to_add_df["license_level"])
        
        while True:
            print("\nWould you like to update:")
            print("1. Site Role")
            print("2. Add User to a Group")
            print("4. Exit")

            selection = input("Enter the number corresponding to your choice: ")

            if selection == "1":
                site_roles = {
                    "1": "Viewer",
                    "2": "Creator",
                    "3": "ExploreCanPublish",
                    "4": "Unlicensed",
                    "5": "ReadOnly",
                    "6": "Viewer"
                }
                print("\nAvailable site roles:")
                for key, value in site_roles.items():
                    print(f"{key}. {value}")
                role_selection = input("Enter the number corresponding to the site role you want to assign: ")
                if role_selection in site_roles:
                    user1.site_role = site_roles[role_selection]
                    server.users.update(user1)
                    print(f"User {user1.name} site role updated to {user1.site_role}")
                else:
                    print("Invalid selection. Please try again.")

            elif selection == "2":
                all_groups, pagination_item = server.groups.get()
                print("\nAvailable groups:")
                #Store the group names and ids in a list of dictionaries
                group_list = []
                for group in all_groups:
                    print(group.name,group.id)
                    group_list.append({"name": group.name, "id": group.id})

                group_name = input("Enter the name of the group to add the user to: ")
                server.groups.add_user(group_name, user1)

            elif selection == "4":
                print("Exiting...")
                break
            else:
                print("Invalid selection. Please try again.")

def main():
    load_dotenv()

    PAT_NAME = os.getenv("PAT_NAME")
    PAT_SECRET = os.getenv("PAT_SECRET")
    SERVER_ADDRESS = os.getenv("SERVER_ADDRESS")
    SITE_ID = os.getenv("SITE_ID")
    #All users currently on the site
    all_users = list_all_users(PAT_NAME, PAT_SECRET, SERVER_ADDRESS, SITE_ID)
    current_users_df = pd.DataFrame(all_users)
    print("Current All Users on the Site:")
    print(current_users_df)

    csv_path = r"C:\Users\LeLuu\Documents\TableauDevQuest\DataDevQuest_Challenges\2026_02\user_list.csv"
    list_users_to_add_df = pd.read_csv(csv_path)
    print("\nUsers from the CSV file:")
    print(list_users_to_add_df)

    #check if the users in the csv file already exist on the site
    users_to_add_df = list_users_to_add_df[list_users_to_add_df["username"].isin(current_users_df["user_name"])]
    #if user already existed on the site, update the info
    if len(users_to_add_df) > 0:
        print("These users_already exist on the site:", users_to_add_df)
        print("Would you like to update the user info or remove them from the site?")
        print("1. Update user info")
        print("2. Remove user from the site")
        selection = input("Enter the number corresponding to your choice: ")
        if selection == "1":
            user_updates(PAT_NAME, PAT_SECRET, SERVER_ADDRESS, SITE_ID, users_to_add_df)
        elif selection == "2":
            print("Here is the list of all users on the site:")
            users_list = list_all_users(PAT_NAME, PAT_SECRET, SERVER_ADDRESS, SITE_ID)
            current_users_df = pd.DataFrame(users_list)
            print(current_users_df)
            selected_users_to_remove = input("\nEnter the index of the users you want to remove from the site, separated by commas: ")
            selected_users_to_remove = [int(index.strip()) for index in selected_users_to_remove.split(",")]
            users_to_remove_df = current_users_df[current_users_df.index.isin(selected_users_to_remove)]
            
            print("\nUsers selected to be removed:")
            print(users_to_remove_df)
            user_remove(PAT_NAME, PAT_SECRET, SERVER_ADDRESS, SITE_ID, users_to_remove_df)
            users_list = list_all_users(PAT_NAME, PAT_SECRET, SERVER_ADDRESS, SITE_ID)
            current_users_df = pd.DataFrame(users_list)
    #else add the new user to the site
    else:
        user_add(PAT_NAME, PAT_SECRET, SERVER_ADDRESS, SITE_ID, list_users_to_add_df)
        new_list = list_all_users(PAT_NAME, PAT_SECRET, SERVER_ADDRESS, SITE_ID)
        new_list_df = pd.DataFrame(new_list)
        print("\nNew list of users on the site after adding new users:")
        print(new_list_df)
    
    # print("\nHere is the list of all users on the site:")
    # print(current_users_df)
    # #Select users index to remove from current_users_df
    # selected_users_to_remove = input("\nEnter the index of the users you want to remove from the site, separated by commas: ")
    # selected_users_to_remove = [int(index.strip()) for index in selected_users_to_remove.split(",")]
    # users_to_remove_df = current_users_df[current_users_df.index.isin(selected_users_to_remove)]
    # print("\nUsers selected to be removed:")
    # print(users_to_remove_df)
    # user_remove(PAT_NAME, PAT_SECRET, SERVER_ADDRESS, SITE_ID, users_to_remove_df)
    # users_list = list_all_users(PAT_NAME, PAT_SECRET, SERVER_ADDRESS, SITE_ID)
    # current_users_df = pd.DataFrame(users_list)

    # all_groups = list_all_groups(PAT_NAME, PAT_SECRET, SERVER_ADDRESS, SITE_ID)
    # all_groups_df = pd.DataFrame(all_groups)
    # print(all_groups_df)
if __name__ == "__main__":
    main()