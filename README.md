# python-scripts
A repository containing python scripts 

switchPrimaryAndUnlink.py
-
- There was a situation with an emterprise company setting up multiple accounts, adding users to both accounts and then eventually phasing out one of the accounts
- This left a large number of users with a primary account that was scheduled for deletion, however they also had an SSO connection, and due to how our primary / secondary logic was set up users couldn't have an SSO connection to a secondary account
- A simple switch primary / secondary wouldnt work
- The workaround involved several steps, using both our API as well as our authentication providers (auth0) API
- The script took an excel file of emails, then for each email:
- Got the ClientID from auth0
- Used the clientID to get the primary and secondary account information
- Removed the SSO identity for the old primary account in Auth0
- Deleted the duplicate auth0 profile that was created in the above step
- Switched the user primary and secondary account now that the SSO connection is removed 

backdateKPI.py 
-
- Used to add old updates to KPIs, a customer reached out with a file containing thousands of records they wanted to add to a KPI
- Takes an excel file of KPI names, update values and update dates
- Makes a GET KPIs call to the account and stores all existing KPI names and ids in a dictionary
- Parses the excel file, checks the given name against the dictionary of existing names
-   If the name exists, uses the id to POST an update on the given date and time
-   If the name does not exist, POST the new KPI, store the name and id in the dictionary and POST the update

combineKRs.py
-
- Used to combine existing Key Results in an account, A customer reached out explaining that they had incorrectly set up their key results and wanted to combine certain Key results
- Takes ids of the Key Result to POST to and the Key result to GET from
- Creates a file containing the Key Result name, update value and date and time of update

getAccountNameFromId.py
-
- Used to create a list of account names that could have been impacted by a bug, engineering provided a list of account IDs, however the Customer Service managers needed to know which specific accounts were impacted.
- Takes an array of Account IDs
- Cross referenced the account IDs in chargebee to get the account name
- Created files with the names of EU and US based accounts that were impacted

getComments.py
-
- A customer reached out asking for a way to see all comments made on key results by a specific user
- This script takes the ID of a specific user, then parses the response from 2 different GET calls (depending on where the comments were left)
- If there is a comment made by the specific user, the title of the Key Result, the text of the comment, and the date and time are written to an excel file

queryMoments.py
- 
- Used to see a full list of moments (history) for a given account
- The GET moments call only returns 10 records at a time, so when looking for a specific moment, using something like postman would be very tedious and time comsuming

removeAccounts.py
-
- Used to remove users from a number of accounts, internal users were asking for a way to remove old accounts from their switch accounts page
- Takes an array of account ids
- Parses the array and removes the specified user from each account

switchEmails.py
-
- Used to switch emails for user profiles in an account, we would often set up SSO for an account and then have the companys IT team reach out saying that they were switching their email domain or formatting
- This script takes an excel file containing old and new emails
- It then parses the file and executes a PATCH call on the user profiles to update the email














