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


def edit_data(file_path, identifier_col, identifier_value, column_to_edit, new_value):

    df = pd.read_csv(file_path)

    # Check if the column to edit exists
    mask = df[identifier_col] == identifier_value

    # Check if the entry already exists
    if not mask.any():
        print(f"Error: No entry found with {identifier_col} = {identifier_value}")
        return

    # If the entry exists, update the value in the specified column
    df.loc[mask, column_to_edit] = new_value

    # Save the modified DataFrame back to the CSV file
    df.to_csv(file_path, index=False)

    # Print a success message
    print(f"Successfully updated {column_to_edit} for {identifier_value}.")


# Example Usage:
edit_data("data/celebrities.csv", "first_name", "Bill", "date_of_birth", "October 29, 1955")


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


# edit_data("data/celebrities.csv", "first_name", "Steve", "date_of_birth", "February 24, 1955")

new_entry = {
    "first_name": "Katy",
    "last_name": "Perry",
    "date_of_birth": "October 25, 1984",
    "images_path": "src/Data/Images/katy_perry.jpg"
}

add_data("data/celebrities.csv", new_entry)

display_data('data/celebrities.csv')



# delete_data("data/celebrities.csv", "FIRSTNAME", "LASTNAME")