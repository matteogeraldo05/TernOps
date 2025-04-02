import unittest
import os
import csv
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))
from accounts import Account, Guest, register_user, login, log_out

class TestAccount(unittest.TestCase):
    def test_account_creation(self):
        account = Account("test_user", "password123", False, "none")
        self.assertEqual(account.get_user_name(), "test_user")
        self.assertEqual(account.get_password(), "password123")
        self.assertFalse(account.get_is_admin())
        self.assertEqual(account.get_favourites(), "none")

    def test_guest_account(self):
        guest = Guest()
        self.assertEqual(guest.get_user_name(), "Guest")
        self.assertEqual(guest.get_password(), "")
        self.assertFalse(guest.get_is_admin())

    def test_account_info_to_string(self):
        # Case when fav is an empty list (defaults to "none")
        account = Account("test_user", "password123", False, [])
        self.assertEqual(account.account_info_to_string(), "Username: test_user\tPassword: password123\tAdmin: False\tFavs: none")
        
        # Case when fav contains some values
        account_with_favs = Account("test_user2", "password456", True, ["John Doe", "Barry Allen"])
        self.assertEqual(account_with_favs.account_info_to_string(), "Username: test_user2\tPassword: password456\tAdmin: True\tFavs: John Doe, Barry Allen")


    def test_guest_account_info_to_string(self):
        guest = Guest()
        self.assertEqual(guest.account_info_to_string(), "Guest User")

class TestAccountFunctions(unittest.TestCase):
    def setUp(self):
        # Temporary Test
        self.test_csv = "test_accounts.csv"  
        self.test_username = "test_user"
        self.test_password = "password123"

        # Create test CSV with account data
        with open(self.test_csv, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["user_name", "password", "is_admin", "favourites"])  
            writer.writerow([self.test_username, self.test_password, False, ""])  

    def tearDown(self):
        # Remove test CSV after tests.
        os.remove(self.test_csv)

    def test_register_user_success(self):
        success, account, message = register_user("new_user", "password123", False, self.test_csv)
        self.assertTrue(success)
        self.assertEqual(account.get_user_name(), "new_user")
        self.assertEqual(message, "Registered")

    def test_register_user_failure(self):
        success, account, message = register_user(self.test_username, "newpass123", False, self.test_csv)
        self.assertFalse(success, msg=f"Unexpected success: {message}")


    def test_login_success(self):
        success, account, message = login("test_user", "password123", self.test_csv)
        self.assertTrue(success)
        self.assertEqual(account.get_user_name(), "test_user")
        self.assertEqual(message, "Logged In.")

    def test_login_failure(self):
        success, account, message = login("nonexistent_user", "password1234", self.test_csv)
        self.assertFalse(success)
        self.assertEqual(account.get_user_name(), "Guest")
        self.assertIn("No account found", message)

    def test_log_out(self):
        success, account, message = log_out()
        self.assertFalse(success)
        self.assertEqual(account.get_user_name(), "Guest")
        self.assertEqual(message, "Successfully logged out.")

if __name__ == "__main__":
    unittest.main()