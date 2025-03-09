# Functions that deal with the csv files

import csv
import numpy as np
import pandas as pd
import datetime
import os

import os
import pandas as pd

class DataManager:
    def __init__(self, file_path):
        self.file_path = file_path

    def display_data(self):
        """Displays and returns the contents of the CSV file."""
        if not os.path.exists(self.file_path):
            print(f"Error: File '{self.file_path}' not found!")
            return None

        df = pd.read_csv(self.file_path)
        print(df)
        return df

    def edit_data(self, identifier_col, identifier_value, column_to_edit, new_value):
        """Edits a specific entry in the CSV file."""
        df = pd.read_csv(self.file_path)

        mask = df[identifier_col] == identifier_value
        if not mask.any():
            print(f"Error: No entry found with {identifier_col} = {identifier_value}")
            return

        df.loc[mask, column_to_edit] = new_value
        df.to_csv(self.file_path, index=False)
        print(f"Successfully updated {column_to_edit} for {identifier_value}.")

    def add_data(self, new_data):
        """Adds a new row to the CSV file if it doesn't already exist."""
        df = pd.read_csv(self.file_path)

        mask = (df['first_name'] == new_data['first_name']) & \
               (df['last_name'] == new_data['last_name']) & \
               (df['date_of_birth'] == new_data['date_of_birth']) & \
               (df['images_path'] == new_data['images_path'])

        if mask.any():
            print(f"Entry for {new_data['first_name']} {new_data['last_name']} already exists.")
            return

        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
        df.to_csv(self.file_path, index=False)
        print(f"Successfully added new entry for {new_data['first_name']} {new_data['last_name']}.")

    def delete_data(self, first_name, last_name):
        """Deletes an entry from the CSV file."""
        df = pd.read_csv(self.file_path)

        mask = (df['first_name'] == first_name) & (df['last_name'] == last_name)
        if not mask.any():
            print(f"No entry found for {first_name} {last_name}.")
            return

        df = df[~mask]
        df.to_csv(self.file_path, index=False)
        print(f"Successfully deleted the entry for {first_name} {last_name}.")




# def display_data(file_name):
#     if not os.path.exists(file_name):
#         print(f"Error: File '{file_name}' not found!")
#         return None

#     df = pd.read_csv(file_name)
#     print(df)
#     return df


# def edit_data(file_path, identifier_col, identifier_value, column_to_edit, new_value):

#     df = pd.read_csv(file_path)

#     # Check if the column to edit exists
#     mask = df[identifier_col] == identifier_value

#     # Check if the entry already exists
#     if not mask.any():
#         print(f"Error: No entry found with {identifier_col} = {identifier_value}")
#         return

#     # If the entry exists, update the value in the specified column
#     df.loc[mask, column_to_edit] = new_value

#     # Save the modified DataFrame back to the CSV file
#     df.to_csv(file_path, index=False)

#     # Print a success message
#     print(f"Successfully updated {column_to_edit} for {identifier_value}.")


# # Example Usage:
# edit_data("data/celebrities.csv", "first_name", "Bill", "date_of_birth", "October 29, 1955")


# def add_data(file_path,new_data):
#     df = pd.read_csv(file_path)

#     # Check if the entry already exists
#     mask = (df['first_name'] == new_data['first_name']) & (df['last_name'] == new_data['last_name']) & (df['date_of_birth'] == new_data['date_of_birth']) & (df['images_path'] == new_data['images_path'])

#     if mask.any():
#         print(f"Entry for {new_data['first_name']} {new_data['last_name']} already exists.")
#         return

#     # If the entry doens't exist, add the new row to the DataFrame
#     df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)

#     # Save the modified DataFrame back to the CSV file
#     df.to_csv(file_path, index=False)

#     # Print a success message
#     print(f"Successfully added new entry for {new_data['first_name']} {new_data['last_name']}.")


# def delete_data(file_path, first_name, last_name):
#     df = pd.read_csv(file_path)

#     # Check if the entry already exists
#     mask = (df['first_name'] == first_name) & (df['last_name'] == last_name)

#     if not mask.any():
#         print(f"No entry found for {first_name} {last_name}.")
#         return

#     # If the entry does exist, remove the row from the DataFrame
#     df = df[~mask]

#     # Save the modified DataFrame back to the CSV file
#     df.to_csv(file_path, index=False)

#     # Print a success message
#     print(f"Successfully deleted the entry for {first_name} {last_name}.")


# # def filter_data(tag):
# #     return #data which matches the tag

# # edit_data("data/celebrities.csv", "first_name", "Steve", "date_of_birth", "February 24, 1955")

# # new_entry = {
# #     "first_name": "Katy",
# #     "last_name": "Perry",
# #     "date_of_birth": "October 25, 1984",
# #     "images_path": "src/Data/Images/katy_perry.jpg"
# # }
# #
# # add_data("data/celebrities.csv", new_entry)
# #
# # display_data('data/celebrities.csv')

# # delete_data("data/celebrities.csv", "FIRSTNAME", "LASTNAME")


# def menu():
#     file_path = "data/celebrities.csv"
#     while True:
#         print("\nMenu:")
#         print("1. Display Data")
#         print("2. Edit Data")
#         print("3. Add Data")
#         print("4. Delete Data")
#         print("5. Exit")

#         choice = input("Enter your choice: ")

#         if choice == "1":
#             display_data(file_path)
#         elif choice == "2":
#             identifier_col = input("Enter the identifier column (e.g., first_name): ")
#             identifier_value = input("Enter the identifier value: ")
#             column_to_edit = input("Enter the column to edit: ")
#             new_value = input("Enter the new value: ")
#             edit_data(file_path, identifier_col, identifier_value, column_to_edit, new_value)
#         elif choice == "3":
#             new_entry = {
#                 'first_name': input("Enter first name: "),
#                 'last_name': input("Enter last name: "),
#                 'date_of_birth': input("Enter date of birth: "),
#                 'images_path': input("Enter image path: ")
#             }
#             add_data(file_path, new_entry)
#         elif choice == "4":
#             first_name = input("Enter first name to delete: ")
#             last_name = input("Enter last name to delete: ")
#             delete_data(file_path, first_name, last_name)
#         elif choice == "5":
#             print("Exiting...")
#             break
#         else:
#             print("Invalid choice. Please try again.")


# if __name__ == "__main__":
#     menu()