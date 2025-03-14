import unittest
import os
import csv
from main import MainApp
from gui import *
from functions import *
from accounts import *
from celebrity_bio_app import CelebrityBioApp
from add_celebrity import AddCelebrityFrame
from login import LoginFrame
from register import RegisterFrame

class TestCelebrityBioApp(unittest.TestCase):
    def setUp(self):
        """Set up a temporary CSV file for testing and initialize the app."""
        self.test_csv = 'test_celebrity_data.csv'
        with open(self.test_csv, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'Age', 'Profession', 'Image Path'])
            writer.writerow(['John Doe', '30', 'Actor', 'path/to/image.jpg'])
        self.app = MainApp()

    def tearDown(self):
        """Remove the test CSV file after testing."""
        if os.path.exists(self.test_csv):
            os.remove(self.test_csv)

    def test_add_celebrity(self):
        """Test adding a new celebrity."""
        frame = AddCelebrityFrame(self.app)
        frame.name_entry.insert(0, 'Jane Smith')
        frame.age_entry.insert(0, '28')
        frame.profession_entry.insert(0, 'Singer')
        frame.image_path = 'path/to/image2.jpg'
        frame.save_celebrity()

        with open(self.test_csv, 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)
            self.assertEqual(len(rows), 3)
            self.assertEqual(rows[1], ['John Doe', '30', 'Actor', 'path/to/image.jpg'])
            self.assertEqual(rows[2], ['Jane Smith', '28', 'Singer', 'path/to/image2.jpg'])

    def test_edit_celebrity(self):
        """Test editing an existing celebrity."""
        self.app.edit_data('John Doe', '35', 'Director', 'path/to/new_image.jpg')

        with open(self.test_csv, 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)
            self.assertEqual(rows[1], ['John Doe', '35', 'Director', 'path/to/new_image.jpg'])

    def test_delete_celebrity(self):
        """Test deleting a celebrity."""
        self.app.delete_data('John Doe')

        with open(self.test_csv, 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)
            self.assertEqual(len(rows), 1)

    def test_login(self):
        """Test login functionality."""
        login_frame = LoginFrame(self.app)
        login_frame.username_entry.insert(0, 'testuser')
        login_frame.password_entry.insert(0, 'testpass')
        result = login_frame.login()
        self.assertTrue(result)

    def test_register(self):
        """Test registration functionality."""
        register_frame = RegisterFrame(self.app)
        register_frame.username_entry.insert(0, 'newuser')
        register_frame.password_entry.insert(0, 'newpass')
        register_frame.confirm_password_entry.insert(0, 'newpass')
        result = register_frame.register_user()
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
