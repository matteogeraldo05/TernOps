import unittest
import os
import csv

from gui import *
from functions import *
from accounts import *

class TestCelebrityBioApp(unittest.TestCase):
    def setUp(self):
        """Set up a temporary CSV file for testing and initialize the app."""
        self.test_csv = 'test_celebrity_data.csv'
        with open(self.test_csv, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['First_Name', 'Last_Name', 'date_of_birth', 'images_path'])
            writer.writerow(['John', 'Doe', 'July 8, 2001', 'path/to/image.jpg'])
        self.app = CTk()

    def tearDown(self):
        """Remove the test CSV file after testing."""
        if os.path.exists(self.test_csv):
            os.remove(self.test_csv)

    def test_add_celebrity(self):
        """Test adding a new celebrity."""
        self.app.createEditCelebrityFrame("Add")
        celebrityData = {
                "first_name": 'Jane',
                "last_name": 'Smith',
                "date_of_birth": 'April, 15, 1993',
                "images_path": 'path/to/image2.jpg'
            }
        self.app.add_data(self.test_csv, celebrityData)


        with open(self.test_csv, 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)
            self.assertEqual(len(rows), 3)
            self.assertEqual(rows[1], ['John', 'Doe', 'July 8, 2001', 'path/to/image.jpg'])
            self.assertEqual(rows[2], ['Jane', 'Smith', 'April, 15, 1993', 'path/to/image2.jpg'])

    def test_edit_celebrity(self):
        """Test editing an existing celebrity."""
        self.app.edit_data('John', 'Doe', 'June 10, 2001', 'path/to/new_image.jpg')

        with open(self.test_csv, 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)
            self.assertEqual(rows[1], ['John', 'Doe', 'June 10, 2001', 'path/to/new_image.jpg'])

    def test_delete_celebrity(self):
        """Test deleting a celebrity."""
        self.app.delete_data(self.test_csv, 'John', 'Doe')

        with open(self.test_csv, 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)
            self.assertEqual(len(rows), 1)

    def test_login(self):
        """Test login functionality."""
        result = login("Rio", 321, self.test_csv)
        self.assertTrue(result)

    def test_register(self):
        """Test registration functionality."""        
        result = register_user("Rio", 321, False, self.test_csv)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
