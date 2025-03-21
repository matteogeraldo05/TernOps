import os
import pandas as pd
import functions

def test_display_data():
    # Assuming the file "test_file.csv" exists and is valid
    result = functions.display_data("src\\tests\\test_celebrities.csv")
    assert result is not None
    assert isinstance(result, pd.DataFrame)

def test_display_data_file_not_found():
    # Simulating a case where the file does not exist
    result = functions.display_data("non_existing_file.csv")
    assert result is None  

def test_edit_data():
    # Assuming "test_file.csv" exists and contains the data to be edited
    functions.edit_data("src\\tests\\test_celebrities.csv", "first_name", "John", "date_of_birth", "June 16, 2005")
    df = pd.read_csv("src\\tests\\test_celebrities.csv")
    # Check if the "date_of_birth" for "John" was updated correctly
    assert df.loc[df['first_name'] == "John", 'date_of_birth'].iloc[0] == "June 16, 2005"

def test_edit_data_entry_not_found():
    # Test case where no entry is found for editing
    functions.edit_data("src\\tests\\test_celebrities.csv", "first_name", "NonExistent", "date_of_birth", "June 16, 2005")
    df = pd.read_csv("src\\tests\\test_celebrities.csv")
    assert df.loc[df['first_name'] == "NonExistent", 'date_of_birth'].empty

def test_add_data():
    new_data = {
        "first_name": "Bill", 
        "last_name": "Smith", 
        "date_of_birth": "June 16, 2005", 
        "date_of_death": "", 
        "achievements": "", 
        "industry": "", 
        "family": "", 
        "associations": "", 
        "controversies": "", 
        "discography": "", 
        "filmography": "", 
        "genres": "", 
        "influence": "", 
        "political_orientation": "", 
        "gender": "", 
        "net_worth": "", 
        "images_path": "", 
        "biography": ""
    }
    functions.add_data("src\\tests\\test_celebrities.csv", new_data)
    df = pd.read_csv("src\\tests\\test_celebrities.csv")
    assert not df[(df['first_name'] == "Bill") & (df['last_name'] == "Smith")].empty

def test_add_data_entry_exists():
    new_data = {
        "first_name": "John", 
        "last_name": "Doe", 
        "date_of_birth": "June 16, 2005", 
        "date_of_death": "", 
        "achievements": "", 
        "industry": "", 
        "family": "", 
        "associations": "", 
        "controversies": "", 
        "discography": "", 
        "filmography": "", 
        "genres": "", 
        "influence": "", 
        "political_orientation": "", 
        "gender": "", 
        "net_worth": "", 
        "images_path": "", 
        "biography": ""
    }
    functions.add_data("src\\tests\\test_celebrities.csv", new_data)
    df = pd.read_csv("src\\tests\\test_celebrities.csv")
    assert df[(df['first_name'] == "John") & (df['last_name'] == "Doe")].shape[0] == 1

def test_delete_data():
    # Assuming "src\\tests\\test_celebrities.csv" contains the data to be deleted
    functions.delete_data("src\\tests\\test_celebrities.csv", "John", "Doe")
    df = pd.read_csv("src\\tests\\test_celebrities.csv")
    assert df[(df['first_name'] == "John") & (df['last_name'] == "Doe")].empty

def test_delete_data_entry_not_found():
    # Test case where no entry is found for deletion
    functions.delete_data("src\\tests\\test_celebrities.csv", "NonExistent", "User")
    df = pd.read_csv("src\\tests\\test_celebrities.csv")
    assert df[(df['first_name'] == "NonExistent") & (df['last_name'] == "User")].empty