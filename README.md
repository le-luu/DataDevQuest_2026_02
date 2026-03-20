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

```python
def query_jobs(token, job_url, job_type_selected, status_selected, record_limit ):
    payload= {}
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        'X-Tableau-Auth': token
    }
    # response = requests.request('GET', job_url, headers=headers, data=payload)

    #Initialize all_jobs list to store all returned jobs, and initialized page_number
    all_jobs = []
    page_num = 1

    #A while loop to iterate to each page until go through all available objects
    while True:
        #Set the url with job_url and pageNumber, pageSize parameter
        url = f"{job_url}?pageNumber={page_num}&pageSize={record_limit}&filter=jobType:eq:{job_type_selected},status:eq:{status_selected}&sort=createdAt:desc"

        #Send the GET request to get thre response
        response = requests.request('GET', url, headers=headers, data=payload)

        #Parse JSON and get the backgroundJobs objects
        data = response.json()
        jobs = data.get("backgroundJobs",{}).get("backgroundJob",[])
```

In this first option, I defined a query_job function to interate to each page to query the job following the filter in job, status, and sort by a column in the endpoint. However, with the query job from REST API, it doesn't show details of the job. So I need to use another endpoint to send the GET request to get more info (For example: task name, flow name, flow_id or datasource_id, datasource_name) by passing the job id from the query job function into this get_job_info function. Then, I merge 2 tables together.

**2/ Using REST API to query the job and job info in One endpoint**

```python
payload ={}
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        'X-Tableau-Auth': token
    }

    #Set the filter, sorting, number of record in the endpoint
    url = f"{job_url}?pageNumber=1&pageSize={record_limit}&filter=jobType:eq:{job_type_selected},status:eq:{status_selected}&sort=createdAt:desc&fields=id,status,createdAt,startedAt,endedAt,priority,jobType,title,subtitle"

    all_jobs=[]
    #Send a GET request to get the response
    response = requests.request('GET', url, headers=headers, data=payload)
    data = response.json()

    #Flattening data
    jobs = data.get("backgroundJobs",{}).get("backgroundJob",[])

    #Store each job in the all_jobs list
    all_jobs.extend(jobs)
    df = pd.DataFrame(all_jobs)
    return df
```

Thanks to Jordan (a creator of this challenge), I learned a new way by using fields parameter in the endpoint. From there, I can apply filter, sort and list all the fields I want in the fields parameter.

**3/ Using TSC in Python to query the job**

```python
def list_jobs_TSC(PAT_NAME, PAT_SECRET, SERVER_ADDRESS, SITE_NAME, job_type_selected, status_selected, record_limit):
    #Authorized step
    tableau_auth = TSC.PersonalAccessTokenAuth(token_name=PAT_NAME, personal_access_token=PAT_SECRET, site_id=SITE_NAME)
    server = TSC.Server(SERVER_ADDRESS, use_server_version=True)

    with server.auth.sign_in(tableau_auth):
        #Using the filter function to filter job with status, job type order by a timestamp and get a slice of 10
        testing = server.jobs.filter(page_size=100,status=status_selected, job_type=job_type_selected).order_by("-created_at")[:record_limit]
        #Store all responses in a list
        jobs = list(testing)

        data = []
        #Store each job in a row in a data list
        for job in jobs:
            data.append({
                "id": job.id,
                "type": job.type,
                "status": job.status,
                "created_at": job.created_at,
                "started_at": job.started_at,
                "ended_at": job.ended_at,
                "title":job.title,
                "notes":job.name
            })

    df = pd.DataFrame(data)
    return df
```

For TSC option, I use the filter function to apply the filter to some fields and add order_by to order a column and set a slice to limit number of result. However, I couldn't get the title, details of the job. Some of columns (title, subtitle, notes) return None.

In the final step, I calculate the average and standard deviation of the running time in seconds and decide how many seconds to wait if it's low/ moderate/ high variablity.
