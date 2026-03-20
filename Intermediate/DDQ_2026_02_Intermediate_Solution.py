"""
DataDevQuest - DDQ2026_02
Challenged By: Jordan Woods
Level: Intermediate
Created By: Le Luu

Objective: Learn how to add filter, sort, and slice background jobs effectively
"""

import pandas as pd
import json
import tableauserverclient as TSC
from dotenv import load_dotenv
import os 
import requests

#Define the get_token function => retrieve token and site_id
def get_token(url, PAT_NAME, PAT_SECRET, SITE_NAME):
    
    payload = json.dumps({
      # Define the credentials data
      "credentials": {
        "personalAccessTokenName": PAT_NAME,
        "personalAccessTokenSecret": PAT_SECRET,
        "site": {
          "contentUrl": SITE_NAME
        }
      }
    })
    
    headers = {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    }

    #Send POST request to get the response
    response = requests.request("POST", url, headers=headers, data=payload)
    #Store the response in data variable
    data=response.json()
    #Get the token and site_id
    token = data['credentials']['token']
    site_id = data['credentials']['site']['id']
    return token, site_id


#Define the query_jobs function to retrieve all jobs using REST API
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

        #Store objects in a jobs list
        if isinstance(jobs,dict):
            jobs = [jobs]
        
        if not jobs:
            break

        #Store all jobs in the all_jobs list
        all_jobs.extend(jobs)

        #Catch number of page and total objects from server
        total_objs = int(data["pagination"]["totalAvailable"])

        #If the total jobs is greater than available objects from server => break the loop
        if len(all_jobs) >= total_objs:
            break

        #Increase the page_num by 1 and loop again
        page_num+=1

    #Finally, store all jobs in a dataframe df and return it
    df = pd.DataFrame(all_jobs)
    return df

#Define get_job_info function to get all details of the job (id, name, type)
def get_job_info(token, job_url, job_id):
    payload= {}
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        'X-Tableau-Auth': token
    }
    url = f"{job_url}/{job_id}"

    #Send the GET request with the job_id var
    response = requests.request('GET', url, headers=headers, data=payload)

    #Parse JSON
    data = response.json()

    #Get the job_info details
    job_info = data.get('job',{})
    #Catch the type of the job because the RunFlow and ExtractRefresh has different objects
    job_type = data.get('job',{}).get('type')

    #Parse all fields from the object
    field = {
        'job_id': job_info.get("id"),
        'type': job_type,

        'flow_id': None,
        'flow_name': None,
        'flowRunId': None,
        'datasource_id': None,
        'datasource_name': None,
        'notes': None
    }
    #If the flow is Runflow, then get id, name and runid
    if job_type == "RunFlow":
        field["flow_id"] = job_info.get("runFlowJobType", {}).get("flow", {}).get("id")
        field["flow_name"] = job_info.get("runFlowJobType", {}).get("flow", {}).get("name")
        field["flowRunId"] = job_info.get("runFlowJobType", {}).get("flowRunId")
        cols_drop = ['datasource_id','datasource_name','notes']
        for key in cols_drop:
            field.pop(key, None)

    # if the type is RefreshExtract, then get the notes, datasource_id, and datasource_name
    elif job_type == "RefreshExtract":
        field['notes'] = job_info.get("extractRefreshJob", {}).get('notes')
        field["datasource_id"] = job_info.get("extractRefreshJob", {}).get("datasource", {}).get("id")
        field["datasource_name"] = job_info.get("extractRefreshJob", {}).get("datasource", {}).get("name")
        cols_drop = ['flow_id','flow_name','flowRunId']
        for key in cols_drop:
            field.pop(key, None)

    #Store in the dataframe
    df = pd.DataFrame([field])

    return df

#Query jobs using TSC
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

#Query jobs using REST API with fields parameter
def testing_new_field(token, job_url,job_type_selected, status_selected, record_limit):
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

# def list_tasks(PAT_NAME, PAT_SECRET, SERVER_ADDRESS, SITE_NAME):
#     tableau_auth = TSC.PersonalAccessTokenAuth(token_name=PAT_NAME, personal_access_token=PAT_SECRET, site_id=SITE_NAME)
#     server = TSC.Server(SERVER_ADDRESS, use_server_version=True)

#     with server.auth.sign_in(tableau_auth):
#         all_tasks, pagination_item = server.tasks.get()
#         print("\nThere are {} tasks on site: ".format(pagination_item.total_available))
#         print([task.id for task in all_tasks])

#     print(all_tasks)

def get_user_input():
    #ask users to enter the job type
    while True:
        print("2 Job type can select: ")
        print("1. Run Flow")
        print("2. Refresh Extract")

        selected_value = input("Please enter the job type you want in number: ").strip()
        if selected_value == "1":
            job_type_selected = 'run_flow'
            print("==> You selected Run Flow task")
            break
        elif selected_value == "2":
            job_type_selected = 'refresh_extracts_via_bridge'
            print("==> You selected Refresh Extract via Bridge task")
            break
        else:
            print("Please enter the option 1 or 2 for job type")
            continue
    
    while True:
        print("\nSelect job status:")
        print("1. Success")
        print("2. Failed")

        status_input = input("Enter status (1 or 2): ").strip()

        if status_input == "1":
            status_selected = "Success"
            print("==> You selected Success")
            break
        elif status_input == "2":
            status_selected = "Failed"
            print("==> You selected Failed")
            break
        else:
            print("Please enter option 1 or 2.\n")

    while True:
        limit_input = input("\nEnter number of records to display: ").strip()

        if limit_input.isdigit() and int(limit_input) > 0:
            record_limit = int(limit_input)
            print(f"==> Showing top {record_limit} records")
            break
        else:
            print("Please enter a valid positive number.\n")

    return job_type_selected, status_selected, record_limit

def main():

    print("==========================================================")
    print("====== DataDev Quest 2026-02 Intermediate Challenge ======")
    print("====== Challenged By: Jordan Woods                  ======")
    print("====== Solved By: Le Luu                            ======")
    print("==========================================================\n")

    load_dotenv()
    
    PAT_NAME = os.getenv("PAT_NAME")
    PAT_SECRET = os.getenv("PAT_SECRET")
    SITE_NAME = os.getenv("SITE_NAME")
    SERVER_ADDRESS = os.getenv("SERVER_ADDRESS")
    API_VERSION = os.getenv("API_VERSION")

    #Get the token and site_id
    url = f"{SERVER_ADDRESS}/api/{API_VERSION}/auth/signin"
    token, site_id = get_token(url,PAT_NAME,PAT_SECRET,SITE_NAME)
    
    #Set the job endpoint
    job_url = f"{SERVER_ADDRESS}/api/{API_VERSION}/sites/{site_id}/jobs"

    print("==================== USER INPUT =============================")
    job_type_selected, status_selected, record_limit = get_user_input()
    

    #===========================================================================
    #========================== OPTION 1: USING REST API =======================
    #===========================================================================
    
    print("\n\n========================== OPTION 1: USING REST API ===========================\n")
    all_jobs = query_jobs(token,job_url,job_type_selected, status_selected, record_limit)
    if all_jobs.empty:
        print(f"\nNo jobs found for job type: {job_type_selected}")
        return
    
    #Lookup the job id from all_jobs dataframe to get the job info
    # job_info_df = pd.concat([
    #     get_job_info(token, job_url, job_id)
    #     for job_id in all_jobs["id"]
    # ], ignore_index=True)
    filtered_jobs = all_jobs[all_jobs["status"] == status_selected]

    if filtered_jobs.empty:
        print(f"\nNo jobs found for:")
        print(f"   - Job Type: {job_type_selected}")
        print(f"   - Status: {status_selected}")
        return
    
    job_info_list = []

    for job_id in all_jobs["id"]:
        try:
            df = get_job_info(token, job_url, job_id)
            if df is not None and not df.empty:
                job_info_list.append(df)
        except Exception as e:
            print(f"ERROR!!! Failed job_id {job_id}: {e}")

    if not job_info_list:
        print("\nNo detailed job info")
        return

    job_info_df = pd.concat(job_info_list, ignore_index=True)

    # Safe concat
    if job_info_list:
        job_info_df = pd.concat(job_info_list, ignore_index=True)
    else:
        job_info_df = pd.DataFrame()

    restapi_df = all_jobs.merge(
        job_info_df,
        how="left",
        left_on="id",
        right_on="job_id"   # or "job_id" depending on your function output
    )
    restapi_df = restapi_df.drop(columns=['priority','job_id','type'])
    print(restapi_df.to_string())


    #===========================================================================
    #================ OPTION 2: USING REST API with field param ================
    #===========================================================================
    print("\n\n========================== OPTION 2: USING REST API with fields param ===========================\n")
    rest_api_fields_df = testing_new_field(token,job_url,job_type_selected, status_selected, record_limit)
    print(rest_api_fields_df.to_string())

    #===========================================================================
    #============================ OPTION 3: USING TSC ==========================
    #===========================================================================

    print("\n\n========================== OPTION 3: USING TSC ===========================\n")

    tsc_jobs_df = list_jobs_TSC(PAT_NAME, PAT_SECRET, SERVER_ADDRESS, SITE_NAME,job_type_selected, status_selected, record_limit)
    print(tsc_jobs_df.to_string())

    
    #===========================================================================
    #=================== Calculate avg waitime and its std =====================
    #===========================================================================
    restapi_df['startedAt'] = pd.to_datetime(restapi_df['startedAt'] )
    restapi_df['endedAt'] = pd.to_datetime(restapi_df['endedAt'])
    restapi_df['running_time_in_sec'] =  (restapi_df['endedAt']-restapi_df['startedAt']).dt.total_seconds()

    avg_time = restapi_df['running_time_in_sec'].mean()
    std_time = restapi_df['running_time_in_sec'].std()

    print("\n\n========================== Analyze Time ===========================\n")
    print(f'Average time: {avg_time:.2f} seconds')
    print(f'Standard deviation: {std_time:.2f} seconds')
    cv = std_time/avg_time 

    if cv < 0.5:
        print(f"CV = std/avg = {cv:.2f} < 0.5 => Low Variability")
    elif cv >=0.5 and cv <=1:
        print(f"\0.5<= CV={cv:.2f} <=1 => Moderate Variability")
    else:
        print(f"CV = std/avg = {cv:.2f} > 1 => High Variability")

    print(f"Waiting time for 90% of above job finishes = {restapi_df['running_time_in_sec'].quantile(0.9)} seconds")

    print("\n Program Ends! See you again! :) ~Le~")
if __name__ == "__main__":
    main()