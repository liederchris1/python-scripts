import requests
import json
import numpy as np
import re

us_api_token = ""
eu_api_token = ""
account_id = ""
us_url = "https://gtmhub-us.chargebee.com/api/v2/customers?id[is]="
eu_url = "https://gtmhub.chargebee.com/api/v2/customers?id[is]="

us_headers = {
    'Authorization': 'Basic ' + us_api_token,
}

eu_headers = {
    'Authorization': 'Basic ' + eu_api_token,
}


# us accountId <> name


def parse_files(file):
    account_ids = []
    with open(file, "r") as f:
        lines = f.readlines()
        pattern2 = r'[a-zA-Z]+\(“([a-zA-Z0-9]*)'
        for line in lines:
            # print(line)
            if re.search(pattern2, line):
                account_ids.append(re.search(pattern2, line)[1])

    return account_ids


def us_accountIdToCompany(us):
    name_array = []
    for i in range(0, len(us)):
        response = requests.get(us_url + us[i], headers=us_headers)
        response_1 = response.json()
        if (response_1['list'] != []):
            customer = (response_1['list'][0])
            company = customer['customer']['company']
            name_array.append(company)
        # else:
        #     name_array.append('No Chargebee record for accountId' + us[i])
    return name_array


def eu_accountIdToCompany(eu):
    name_array = []
    for i in range(0, len(eu)):
        response = requests.get(eu_url + eu[i], headers=eu_headers)
        response_1 = response.json()
        if(response_1['list'] != []):
            customer = (response_1['list'][0])
            company = customer['customer']['company']
            name_array.append(company)
        # else:
        #     name_array.append('No Chargebee record for accountId: ' + eu[i])
    return name_array


def write_to_file(file, arr, subject):
    f = open(file, "a")
    f.write(subject + "\n")
    for i in range(0, len(arr)):
        f.write("     " + arr[i] + "\n")


write_to_file("US_Accounts.txt", us_accountIdToCompany(parse_files("US_goals.txt")), "US Accounts \n Goals / Objectives")
write_to_file("US_Accounts.txt", us_accountIdToCompany(parse_files("US_metrics.txt")), "\n Metrics / Krs")
write_to_file("US_Accounts.txt", us_accountIdToCompany(parse_files("US_tasks.txt")), "\n Tasks")
write_to_file("US_Accounts.txt", us_accountIdToCompany(parse_files("US_tasks.txt")), "\n Feed Data")

write_to_file("EU_Accounts.txt", eu_accountIdToCompany(parse_files("EU_goals.txt")), "EU Accounts \n Goals / Objectives")
write_to_file("EU_Accounts.txt", eu_accountIdToCompany(parse_files("EU_metrics.txt")), "\n Metrics / Krs")
write_to_file("EU_Accounts.txt", eu_accountIdToCompany(parse_files("EU_tasks.txt")), "\n Tasks")
write_to_file("EU_Accounts.txt", eu_accountIdToCompany(parse_files("EU_tasks.txt")), "\n Feed Data")

#print("EU Accounts with affected tasks: ",  eu_accountIdToCompany(parse_files("EU_tasks.txt")))

#print("EU Accounts with affected metrics: ",  eu_accountIdToCompany(parse_files("EU_metrics.txt")))
#
# print("EU Accounts with affected goals: ",  eu_accountIdToCompany(eu_accountIds_goals))
#
# print("EU Accounts with affected users: ",  eu_accountIdToCompany(eu_accountIds_users))
#
# print("EU Accounts with affected teams: ",  eu_accountIdToCompany(eu_accountIds_teams))
