import unittest
from unittest.mock import MagicMock, patch
import pandas as pd
import os
import shutil
import tempfile
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))
import accounts
import functions
import csv
from gui import removeCelebrity

class AccountsTest(unittest.TestCase):
    
    def setUp(self):
        # Create a temporary CSV file for testing
        self.temp_dir = tempfile.mkdtemp()
        self.account_file = os.path.join(self.temp_dir, "test_accounts.csv")
        
        # Create a test accounts file
        with open(self.account_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["user_name", "password", "is_admin","favourites"])
            writer.writerow(["testuser", "testpass", True, ""])
    
    def tearDown(self):
        # Remove temporary files after tests
        shutil.rmtree(self.temp_dir)
    
    def test_register_user_success(self):
        # UT-01-CB: Testing successful user registration
        success, account, message = accounts.register_user("newuser", "newpass", False, self.account_file)
        
        self.assertTrue(success)
        self.assertEqual(account.get_user_name(), "newuser")
        self.assertEqual(account.get_password(), "newpass")
        self.assertEqual(account.get_is_admin(), False)
        self.assertEqual(message, "Registered")
        
        # Verify user was added to the file
        df = pd.read_csv(self.account_file)
        self.assertIn("newuser", df["user_name"].values)
    
    def test_register_user_duplicate(self):
        # UT-02-CB: Testing registration with existing username
        success, account, message = accounts.register_user("testuser", "newpass", False, self.account_file)
        
        self.assertFalse(success)
        self.assertEqual(account.get_user_name(), "Guest")
        self.assertTrue("already taken" in message)
    
    def test_login_success(self):
        # UT-03-CB: Testing successful login
        success, account, message = accounts.login("testuser", "testpass", self.account_file)
        
        self.assertTrue(success)
        self.assertEqual(account.get_user_name(), "testuser")
        self.assertEqual(account.get_password(), "testpass")
        self.assertEqual(account.get_is_admin(), True)
        self.assertEqual(message, "Logged In.")
    
    def test_login_wrong_password(self):
        # UT-04-CB: Testing login with incorrect password
        success, account, message = accounts.login("testuser", "wrongpass", self.account_file)
        
        self.assertFalse(success)
        self.assertEqual(account.get_user_name(), "Guest")
        self.assertEqual(message, "Incorrect password.")
    
    def test_login_nonexistent_user(self):
        # UT-05-CB: Testing login with non-existent user
        success, account, message = accounts.login("nonexistent", "pass", self.account_file)
        
        self.assertFalse(success)
        self.assertEqual(account.get_user_name(), "Guest")
        self.assertTrue("No account found" in message)
    
    def test_logout(self):
        # UT-06-CB: Testing logout function
        success, account, message = accounts.log_out()
        
        self.assertFalse(success)
        self.assertEqual(account.get_user_name(), "Guest")
        self.assertEqual(message, "Successfully logged out.")


class FunctionsTest(unittest.TestCase):
    
    def setUp(self):
        # Create temporary CSV file and directory for testing
        self.temp_dir = tempfile.mkdtemp()
        self.test_csv = os.path.join(self.temp_dir, "test_celebrities.csv")
        self.image_dir = os.path.join(self.temp_dir, "images")
        os.makedirs(self.image_dir, exist_ok=True)
        
        # Create test image
        self.test_image = os.path.join(self.image_dir, "test.jpg")
        with open(self.test_image, "w") as f:
            f.write("test image content")
        
        # Create test CSV
        with open(self.test_csv, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["first_name", "last_name", "date_of_birth", "images_path"])
            writer.writerow(["John", "Doe", "January 1, 1980", os.path.join(self.image_dir, "john_doe.jpg")])
            writer.writerow(["Jackie", "Chan", "February 15, 1985", os.path.join(self.image_dir, "jackie_chan.jpg")])
            writer.writerow(["Jack", "Sparrow", "March 22, 1980", os.path.join(self.image_dir, "jack_sparrow.jpg")])
    
    def tearDown(self):
        # Clean up temp files
        shutil.rmtree(self.temp_dir)
    
    def test_add_data(self):
        # UT-07-TB: Testing adding new celebrity data
        new_data = {
            "first_name": "Jane",
            "last_name": "Smith",
            "date_of_birth": "February 15, 1985",
            "images_path": os.path.join(self.image_dir, "jane_smith.jpg")
        }
        
        functions.add_data(self.test_csv, new_data)
        
        # Verify data was added
        df = pd.read_csv(self.test_csv)
        self.assertEqual(len(df), 4)  # Original + new entry
        self.assertIn("Jane", df["first_name"].values)
        self.assertIn("Smith", df["last_name"].values)
    
    def test_add_duplicate_data(self):
        # UT-08-TB: Testing adding duplicate celebrity data
        duplicate_data = {
            "first_name": "John",
            "last_name": "Doe",
            "date_of_birth": "January 1, 1980",
            "images_path": os.path.join(self.image_dir, "john_doe.jpg")
        }
        
        # Length of dataframe should remain the same
        before_df = pd.read_csv(self.test_csv)
        before_count = len(before_df)
        
        functions.add_data(self.test_csv, duplicate_data)
        
        after_df = pd.read_csv(self.test_csv)
        self.assertEqual(len(after_df), before_count)
    
    def test_edit_data(self):
        # UT-09-TB: Testing editing celebrity data
        functions.edit_data(self.test_csv, "first_name", "John", "date_of_birth", "January 2, 1981")
        
        # Verify data was updated
        df = pd.read_csv(self.test_csv)
        mask = df["first_name"] == "John"
        self.assertEqual(df.loc[mask, "date_of_birth"].values[0], "January 2, 1981")
    
    def test_delete_data(self):
        # UT-10-TB: Testing deleting celebrity data
        # First create the image file that would be deleted
        john_image = os.path.join(self.image_dir, "john_doe.jpg")
        with open(john_image, "w") as f:
            f.write("test content")
        
        # Update the path in the CSV to match the test file
        df = pd.read_csv(self.test_csv)
        df.loc[0, "images_path"] = john_image
        df.to_csv(self.test_csv, index=False)
        
        # Delete the data
        functions.delete_data(self.test_csv, "John", "Doe")
        
        # Verify data was deleted
        df = pd.read_csv(self.test_csv)
        self.assertEqual(len(df), 2)
        
        # Verify image was deleted
        self.assertFalse(os.path.exists(john_image))
    
    def test_copy_image_to_folder(self):
        # UT-11-OB: Testing copying image to celebrity folder
        dest_path = functions.copy_image_to_folder(self.test_image, "test_celebrity")
        
        # Verify image was copied
        self.assertTrue(os.path.exists(dest_path))
        
        # Cleanup
        if os.path.exists(os.path.dirname(dest_path)):
            shutil.rmtree(os.path.dirname(dest_path))
    
    def test_load_celebrities_file(self):
        # UT-12-CB: Testing loading celebrities from CSV
        celebrities = functions.load_celebrities_file(self.test_csv)
        
        self.assertEqual(len(celebrities), 3)
        self.assertEqual(celebrities[0]["first_name"], "John")
        self.assertEqual(celebrities[0]["last_name"], "Doe")

    # Tests on search function
    def test_filter_by_tag(self):
        # UT-13-OB: Testing Filtering by First Name
        result_df = functions.filter_by_tag(self.test_csv, "first_name", "John")

        self.assertEqual(len(result_df), 1)
        self.assertEqual(result_df["first_name"].iloc[0], "John")

    def test_filter_by_tag_no_match(self):
        # UT-14-OB: Testing Filter for a non-existent name
        result_df = functions.filter_by_tag(self.test_csv, "first_name", "Nonexistent")

        self.assertEqual(len(result_df), 0)

    def test_filter_by_tag_multiple_matches(self):
        # UT-15-OB: Filtering by date of birth in search (Removed but still present)
        result_df = functions.filter_by_tag(self.test_csv, "date_of_birth", "1980")

        self.assertEqual(len(result_df), 2)
        self.assertIn("John", result_df["first_name"].values)
        self.assertIn("Jack", result_df["first_name"].values)

    def test_filter_by_tag_case_insensitive(self):
        # UT-16-OB: Testing for case sensitivity
        result_df = functions.filter_by_tag(self.test_csv, "first_name", "john")
        self.assertEqual(len(result_df), 1)
        self.assertEqual(result_df["first_name"].iloc[0], "John")

    def test_filter_by_tag_empty_string(self):
        # UT-17-OB:  Testing empty bar, should return all
        result_df = functions.filter_by_tag(self.test_csv, "first_name", "")

        self.assertEqual(len(result_df), 3)  

    def test_filter_by_tag_empty_column(self):
        # UT-18-OB: Testing search on empty column 
        with self.assertRaises(ValueError) as context:
            functions.filter_by_tag(self.test_csv, "", "John")

        # Check if the error message matches the expected message
        self.assertEqual(str(context.exception), "Column name cannot be empty")

class TestRemoveCelebrity(unittest.TestCase):
    
    @patch('gui.CTkMessagebox')  
    @patch('gui.functions.delete_data')
    @patch('gui.showMainFrame')
    def test_removeCelebrity_yes(self, mock_showMainFrame, mock_delete_data, MockCTkMessagebox):
        # UT-19-OB: Testing removing function when user selects yes
        mock_messagebox = MockCTkMessagebox.return_value
        mock_messagebox.get.return_value = "Yes" 

        # Fake Celeb
        first_name = "John"
        last_name = "Doe"
        removeCelebrity(first_name, last_name)

        # Assert
        MockCTkMessagebox.assert_called_once_with(
            message=f"Are you sure you would like to delete {first_name} {last_name}? This action is permenant.",
            icon="warning",
            option_1="Yes",
            option_2="No"
        )
        mock_delete_data.assert_called_once_with("src\\Data\\celebrities.csv", first_name, last_name)
        mock_showMainFrame.assert_called_once()

    @patch('gui.CTkMessagebox')  
    @patch('gui.functions.delete_data')
    @patch('gui.showMainFrame')
    def test_removeCelebrity_no(self, mock_showMainFrame, mock_delete_data, MockCTkMessagebox):
        # UT-20-OB: Testing removing function when user selects no
        mock_messagebox = MockCTkMessagebox.return_value
        mock_messagebox.get.return_value = "No"  

        # Fake Celeb
        first_name = "John"
        last_name = "Doe"
        removeCelebrity(first_name, last_name)

        # Assert
        mock_delete_data.assert_not_called()  
        mock_showMainFrame.assert_not_called()  
    
if __name__ == "__main__":
    unittest.main()