import json

import requests
import pandas as pd
import openpyxl

headers = {
    'Authorization': 'Bearer ',
    'Content-Type': 'application/json',
    'gtmhub-accountid': ''
}
# this line prepares the excel file to be read
# make sure to have the excel file in the same directory as this python script
# first argument: excel file name
# second argument: excel sheet name
kpi_updates = pd.read_excel("kpi_update_example.xlsx", "Sheet1")

# test function to ensure that the correct values are being pulled from the excel file
def test():
    for x in range(0, 5):
        body = {
                "group": kpi_updates.iloc[x,1],
                "timeZone": "UTC-7",
                "value": kpi_updates.iloc[x,3]
            }
        name = kpi_updates.iloc[x, 2]
        print(name)
        print(body)


# creates and returns a dictionary of all KPIS in the account
# name : id pairs
# iterates through the json response from GET kpis
def kpiDict():
    kpis_json = requests.get('https://app.gtmhub.com/api/v2/kpis', headers = headers).json()
    kpis_items = kpis_json['items']
    kpi_dict = dict({"KPI_name": "KPI_id"})
    for x in range(0, len(kpis_items)):
        kpi_name = kpis_items[x]['name']
        kpi_id = kpis_items[x]['id']
        kpi_dict[kpi_name] = kpi_id
    print(kpi_dict)
    return kpi_dict


# creates snapshots for the KPIs included in the excel file

# takes a dictionary as the parameter, use the kpiDict() function to create the dictionary
# uses the name column to determine whether to post snapshots to existing KPI or create new one

# date column must be in string format (YYYY-MM-DD)
# use excel function =TEXT([cell number], "yyyy-mm-dd")
def backdateKpis(dictionary):
    # iterates through excel file and sets date and value field
    # make sure that the time zone is the same as listed in aggregated report settings
    for x in range(0, len(kpi_updates.index)):
        body = {
                "group": kpi_updates.iloc[x,1],
                "timeZone": "UTC+2",
                "value": kpi_updates.iloc[x,3]
            }
        # print(body)
        kpi_id = ''
        name = kpi_updates.iloc[x,2]
        # Checks to see if the KPI name exists in the account
        # if yes, gets the ID for that specific KPI
        # if no, POST call to create KPI with that name, adds name and ID to dictionary, gets ID of newly created KPI
        # make sure to update te ownerIds array with the correct ownerId
        if name in dictionary:
            kpi_id = dictionary[name]
        else:
            kpi_body = {
                'aggregation': 'last',
                'name': name,
                'ownerIds': ['6478534e2b7b7b50d60030a4'],
                'targetOperator': 'should_increase',
                'formatting':{'fractionSize': 2, 'prefix': "", 'suffix': ""}
            }
            # make sure to change for appropriate data center
            newKpiResponse = requests.post('https://app.quantive.com/api/v1/kpis', data=json.dumps(kpi_body), headers=headers)
            # getting name and ID from the newly created KPI
            newKpiJson = newKpiResponse.json()
            newKpiId = newKpiJson['id']
            newKpiName = newKpiJson['name']
            print("Created New KPI: " + newKpiName)
            # adding newly created KPI name and ID to dictionary
            dictionary[newKpiName] = newKpiId
            kpi_id = newKpiId
        # Using the ID from the dictionary, POSTs snapshot using the body declared above
        url = "https://app.quantive.com/api/v1/kpis/" + kpi_id + "/snapshots"
        response = requests.post(url, data=json.dumps(body), headers = headers)
        print(response)


# commented out function calls
# kpiDict()

# test()

# backdateKpis(kpiDict())

# check list before running
# 1. Changed all URLs to appropriate data centers
# 2. Changed timezone in body
# 3. Correct Excel sheet and file name
# 4. Changed ownerIDs array in body
# 5. Correct account id and token
