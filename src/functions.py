# Functions that deal with the csv files

import csv
import numpy as np
import pandas as pd
import datetime
import os

def display_data(file_name):
    if not os.path.exists(file_name):
        print(f"Error: File '{file_name}' not found!")
        return None

    df = pd.read_csv(file_name)
    print(df)
    return df

def edit_data(file_path, col_to_edit, new_value):
    df = pd.read_csv(file_path)

    mask = df[col_to_edit] == new_value

    if not mask.any():
        print(f"Error: No entry found with {col_to_edit} = {new_value}")
        return

    df.loc[mask, col_to_edit] = new_value

    df.to_csv(file_path, index=False)

    print(f"Successfully updated {col_to_edit} for {new_value}.")

def add_data(file_path,new_data):
    df = pd.read_csv(file_path)

    # Check if the entry already exists
    mask = (df['first_name'] == new_data['first_name']) & (df['last_name'] == new_data['last_name']) & (df['date_of_birth'] == new_data['date_of_birth']) & (df['file_path'] == new_data['file_path'])

    if mask.any():
        print(f"Entry for {new_data['first_name']} {new_data['last_name']} already exists.")
        return

    # If the entry doens't exist, add the new row to the DataFrame
    df = df.append(new_data, ignore_index=True)

    # Save the modified DataFrame back to the CSV file
    df.to_csv(file_path, index=False)

    # Print a success message
    print(f"Successfully added new entry for {new_data['first_name']} {new_data['last_name']}.")

def delete_data(file_path, first_name, last_name):
    df = pd.read_csv(file_path)

    # Check if the entry already exists
    mask = (df['first_name'] == first_name) & (df['last_name'] == last_name)

    if mask.any():
        print(f"No entry found for {first_name} {last_name}.")
        return

    # If the entry does exist, remove the row from the DataFrame
    df = df[~mask]

    # Save the modified DataFrame back to the CSV file
    df.to_csv(file_path, index=False)

    # Print a success message
    print(f"Successfully deleted the entry for {delete_data['first_name']} {delete_data['last_name']}.")

def filter_data(tag):
    return #data which matches the tag


# display_data('data/celebrities.csv')
# edit_data(file_path, column to change, new data)

# new_entry = {
#     "first_name": "NAME",
#     "last_name": "LASTNAME",
#     "date_of_birth": "MONTH DAY, YEAR",
#     "images_path": "src/Data/Images/FILENAME"
# }
#
# add_data("data/celebrities.csv", new_entry)

# delete_data("data/celebrities.csv", "FIRSTNAME", "LASTNAME")

