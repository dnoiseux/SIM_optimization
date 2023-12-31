#Jasper Rate plan optimizer
#Python 3.7.3 (default, Mar 27 2019, 09:23:15) [MSC v.1915 64 bit (AMD64)] :: Anaconda, Inc. on win32

import pandas as pd

# Specify the file path for the rate plan cost
file_path1 = r'H:\OneDrive - Dimonoff Inc\Documents\!!Jasper optimisation\rateplancost.xlsx' 

# Read the Excel file into a DataFrame and set the 'Rate Plan' column as the index
rate_plan_df = pd.read_excel(file_path1)
#rate_plan_df = rate_plan_df.set_index('Rate Plan')

# Access the columns by their names and save them into variables
rate_plan_name = rate_plan_df['Rate Plan'] # replace 'column1' with your actual column name
rate_plan_cost = rate_plan_df['Rate_Plan_Cost'] # replace 'column2' with your actual column name
rate_plan_size = rate_plan_df['Rate_Plan_Size (MB)'] # replace 'column3' with your actual column name
rate_plan_type = rate_plan_df['Rate_Plan_type'] # replace 'column4' with your actual column name 
overage_rate = rate_plan_df['Rate_Plan_Overage_Rate (per MB)'] # replace 'column5' with your actual column name
rate_plan_name_alt1 = rate_plan_df['Rate_plan_name_2'] # replace 'column5' with your actual column name
rate_plan_name_alt2 = rate_plan_df['Rate_plan_name_3'] # replace 'column5' with your actual column name


# Specify the file path for the Jasper device export (renamed to export.xlsx) that represent the accounts
file_path2 = r'H:\OneDrive - Dimonoff Inc\Documents\!!Jasper optimisation\export.xlsx'

# Read the Excel file into a DataFrame and set the 'ICCID' column as the index
account_df = pd.read_excel(file_path2)
#account_df = account_df.set_index('ICCID')

# Access the columns by their names
# Replace the column names with the actual ones in your 'export.xlsx' file
account_column1 = account_df['Cycle to Date Usage (MB)']  # replace 'column1' with your actual column name
account_column2 = account_df['Custom 1']  # replace 'column2' with your actual column name
account_column3 = account_df['IPv4 Address']  # replace 'column3' with your actual column name
account_column4 = account_df['MSISDN']  # replace 'column4' with your actual column name
account_column5 = account_df['ICCID']  # replace 'column5' with your actual column name
account_column6 = account_df['Rate Plan']  # replace 'column5' with your actual column name
account_column7 = account_df['SIM Status']  # replace 'column5' with your actual column name
#account_column8 = account_df['Activated']  # replace 'column5' with your actual column name
account_column9 = account_df['In Session']  # replace 'column5' with your actual column name
account_column10 = account_df['CAN ou ROAM']  # replace 'column5' with your actual column name

 
# Remove commas from 'Cycle to Date Usage (MB)' and convert it to numbers (floats) 
account_df['Cycle to Date Usage (MB)'] = account_df['Cycle to Date Usage (MB)'].str.replace(',', '').astype(float)

# !!!Check if 'Cycle to Date Usage (MB)' is greater than 0 for SIMs that are not activated!!!
for index, row in account_df.iterrows():
    # Check if 'SIM Status' is not 'Activated' and 'Cycle to Date Usage (MB)' is greater than 0 
    if row['SIM Status'] != 'Activated' and row['Cycle to Date Usage (MB)'] > 0:
        # Raise a warning with ICCID, SIM status and Cycle to Date Usage (MB) for the SIM
        print(f"Warning: ICCID {row['ICCID']}, SIM status {row['SIM Status']}, Cycle to Date Usage (MB) {row['Cycle to Date Usage (MB)']}")


# Filter the DataFrame to only keep rows where 'SIM Status' is 'Activated'  
account_df = account_df[account_df['SIM Status'] == 'Activated']

# when account CAN ou ROAM is empty , then set Can ou ROAM to ROAM 
account_df['CAN ou ROAM'] = account_df['CAN ou ROAM'].fillna('ROAM')


# Sort the DataFrame by 'CAN or ROAM' in descending order and then by 'Cycle to Date Usage (MB)' in descending order
#account_df = account_df.sort_values(by='CAN ou ROAM', ascending=False)
#print(account_df)

#save into two separate excel files accounts with CAN or ROAM 
# sort only by CAN 
account_CAN_df = account_df[account_df['CAN ou ROAM'] == 'CAN']
account_CAN_df = account_CAN_df.sort_values(by='Cycle to Date Usage (MB)', ascending=False)
account_CAN_df.to_excel('CAN.xlsx', index=False)
# sort only by ROAM
account_ROAM_df = account_df[account_df['CAN ou ROAM'] == 'ROAM']
account_ROAM_df = account_ROAM_df.sort_values(by='Cycle to Date Usage (MB)', ascending=False)
account_ROAM_df.to_excel('ROAM.xlsx', index=False)

# Merge the two DataFrames on the 'Rate Plan' column and keep all rows from the 'account_df' DataFrame (left join)
merged_df = pd.merge(account_df, rate_plan_df, on='Rate Plan', how='left')
merged_df = merged_df.sort_values(by=['CAN ou ROAM', 'Rate_Plan_Size (MB)', 'Cycle to Date Usage (MB)'], ascending=False)
#merged_df = merged_df.reset_index(drop=True)

# Save the merged to an Excel file 
merged_df.to_excel('merged.xlsx', index=False)

# Group the merged DataFrame by 'Rate Plan', count the number of accounts for each rate plan, and calculate the mean 'Rate_Plan_Cost' for each rate plan
grouped_df = merged_df.groupby(['Rate Plan', 'CAN ou ROAM']).agg({'Rate Plan': 'size', 'Rate_Plan_Cost': 'mean'}).rename(columns={'Rate Plan': 'Number of Accounts', 'Rate_Plan_Cost': 'Average Cost', 'Cycle to Date Usage (MB)': 'sum', 'Rate_Plan_Size (MB)': 'sum'}).reset_index()

# Now you can calculate the total cost for each rate plan by multiplying the number of accounts by the average cost of the rate plan 
grouped_df['Total Cost'] = grouped_df['Number of Accounts'] * grouped_df['Average Cost']

pause = input("Press the <ENTER> key to continue...")


# Calculate the total cost for each rate plan by multiplying the number of accounts by the cost of the rate plan
#grouped_df['Total Cost'] = grouped_df['Number of Accounts'] * grouped_df['Cost']

# Calculate the grand total of the number of accounts and the total cost
total_accounts = grouped_df['Number of Accounts'].sum()
total_cost = grouped_df['Total Cost'].sum()

# Print the summary and the grand total
print(grouped_df)


#print(f"Grand Total of Number of Accounts: {total_accounts}")
print(f"Grand Total of Cost: {total_cost}")

# Save the summary to an Excel file
grouped_df.to_excel('summary.xlsx', index=False)


pause = input("Press the <ENTER> key to continue to optimization...")

#############################################
### Optimisation part ###
#############################################

# Create a list of available rate plans and their remaining capacities
rate_plans = merged_df['Rate Plan'].unique()
rate_plan_capacities = {rate_plan: merged_df[merged_df['Rate Plan'] == rate_plan]['Rate_Plan_Size (MB)'].sum() for rate_plan in rate_plans}
print(rate_plan_capacities) # format as a table 


pause = input("Press the <ENTER> key to continue to next step...")

# Sort the accounts in descending order by their usage
accounts = merged_df.sort_values('Cycle to Date Usage (MB)', ascending=False)

# Create a list of available rate plans and their remaining capacities
rate_plans = merged_df['Rate Plan'].unique()
rate_plan_capacities = {rate_plan: merged_df[merged_df['Rate Plan'] == rate_plan]['Rate_Plan_Size (MB)'].sum() for rate_plan in rate_plans}

