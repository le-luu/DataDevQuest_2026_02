# DataDev Quest Challenge 2026_02

![image](https://github.com/le-luu/DataDevQuest_2025_03/blob/main/img/logo.svg)

### Challenged By:

Jordan Woods

### Solution Video
[![DDQ_2026_02](https://img.youtube.com/vi/n8_kODsYo20/0.jpg)](https://www.youtube.com/watch?v=n8_kODsYo20)

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

<img src="https://github.com/le-luu/DataDevQuest_2026_02/blob/main/img/beginner_main.png" height="500">
Then build a program to let the user choose the option to add users from a CSV file or update users if found existing users on the list.

### Output

<img src=https://github.com/le-luu/DataDevQuest_2026_02/blob/main/img/beginner_add_users.png width='600'>

Add new users from a CSV file to the site. The program will check if users in the CSV are new or already existed in the user list from Tableau Cloud site. It will seperate into 2 groups. For the new users group, it will add those users to the site.

<img src="https://github.com/le-luu/DataDevQuest_2026_02/blob/main/img/beginner_update_users.png" height="600">

For the list of existing users, it will ask users if they want to update or remove those users. If choosing "update", it will let the user to choose updating the site role, assign user to another group or remove user from a group.

<img src="https://github.com/le-luu/DataDevQuest_2026_02/blob/main/img/beginner_remove.png" height="500">

Remove user from the site. For existing users list, the user can choose to remove from the site.

## Intermediate Challenge

Link to the Intermediate Challenge: https://datadevquest.com/challenges/ddq2026-02-fetch-recent-refreshes-intermediate

### Objective

- Filter, sort and slice background jobs
- Track the history jobs
- Apply REST API, TSC in Python to track the jobs
- Dynamically using parameter to fetch refreshes

### Tasks

I applied 3 ways to solve the challenge:

**1/ Using REST API to query jobs and get the job info from another endpoint**

**2/ Using REST API to query the job and job info in one endpoint**

**3/ Using TSC in Python to query the job**
