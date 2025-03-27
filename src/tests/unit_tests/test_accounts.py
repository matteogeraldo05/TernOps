import unittest
import os
import csv
from accounts import Account, Guest, register_user, login, log_out

class TestAccount(unittest.TestCase):
    def test_account_creation(self):
        account = Account("test_user", "password123", False)
        self.assertEqual(account.get_user_name(), "test_user")
        self.assertEqual(account.get_password(), "password123")
        self.assertFalse(account.get_is_admin())

    def test_guest_account(self):
        guest = Guest()
        self.assertEqual(guest.get_user_name(), "Guest")
        self.assertEqual(guest.get_password(), "")
        self.assertFalse(guest.get_is_admin())

    def test_account_info_to_string(self):
        account = Account("test_user", "password123", False)
        self.assertEqual(account.account_info_to_string(), "Username: test_user\tPassword: password123\tAdmin: False")

    def test_guest_account_info_to_string(self):
        guest = Guest()
        self.assertEqual(guest.account_info_to_string(), "Guest User")

class TestAccountFunctions(unittest.TestCase):
    def setUp(self):
        self.file_path = "src/Data/accountInfo.csv"
        # Create a temporary CSV file for testing
        with open(self.file_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["user_name", "password", "is_admin"])
            writer.writerow(["existing_user", "password123", False])

    def tearDown(self):
        # Remove the temporary CSV file after tests
        os.remove(self.file_path)

    def test_register_user_success(self):
        success, account, message = register_user("new_user", "password123", False, self.file_path)
        self.assertTrue(success)
        self.assertEqual(account.get_user_name(), "new_user")
        self.assertEqual(message, "Registered")

    def test_register_user_failure(self):
        success, account, message = register_user("existing_user", "password123", False, self.file_path)
        self.assertFalse(success)
        self.assertEqual(account.get_user_name(), "Guest")
        self.assertIn("already taken", message)

    def test_login_success(self):
        success, account, message = login("existing_user", "password123", self.file_path)
        self.assertTrue(success)
        self.assertEqual(account.get_user_name(), "existing_user")
        self.assertEqual(message, "Logged In.")

    def test_login_failure(self):
        success, account, message = login("nonexistent_user", "password123", self.file_path)
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