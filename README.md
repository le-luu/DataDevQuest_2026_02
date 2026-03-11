# DataDev Quest Challenge 2026_02

![image](https://github.com/le-luu/DataDevQuest_2025_03/blob/main/img/logo.svg)

### Challenged By:

Jordan Woods

### Solution Video

## Beginner Challenge

Link to the Beginner Challenge: https://datadevquest.com/challenges/ddq2026-02-bulk-add-users-beginner

### Objective

- Learn how to add/remove multiple users on the site
- Assign/Remove groups to specified users
- Update the User's info on the site

### Tasks

Assume that users are working on Tableau Cloud and there are a list of users (contains existing users and new users) need to add to a site on Tableau Cloud. Write a program to:

- Add new users on the site
- If the user already existed on the site, then:
  - Check if admin wants to update the user's info (site role, add to another group, remove from a group) or
  - Remove the user from the list

![image](https://github.com/le-luu/DataDevQuest_2026_02/blob/main/img/beginner_modules_func.png)

To solve the problem above, I built some functions:

- list_all_users: to list all current users on the site, return the list of users
- user_add: to add the list of users on the site
- user_remove: to remove a list of users on the site
- user_update: to update the user's info on the site, it could be: site role, add user to a group or remove users from a group

![image](https://github.com/le-luu/DataDevQuest_2026_02/blob/main/img/beginner_main.png)

Then build a program to let the user choose the option to add users from a CSV file or update users if found existing users on the list.

### Output

![image](https://github.com/le-luu/DataDevQuest_2026_02/blob/main/img/beginner_add_users.png)

Add new users from a CSV file to the site

![image](https://github.com/le-luu/DataDevQuest_2026_02/blob/main/img/beginner_update_users.png)

Update user's info (site role, assign to a new group or remove user from a group)

![image](https://github.com/le-luu/DataDevQuest_2026_02/blob/main/img/beginner_remove.png)

Remove user from the site
