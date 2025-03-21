import pandas as pd
import csv

# Account class
class Account:
    def __init__(self, name: str, pw: str, admin: bool):
        self.user_name = name
        self.password = pw
        self.is_admin = admin
    
    def set_user_name(self, name):
        self.user_name = name
    
    def get_user_name(self):
        return self.user_name
    
    def set_password(self, password):
        self.password = password
    
    def get_password(self):
        return self.password
    
    def set_is_admin(self, is_admin):
        self.is_admin = is_admin

    def get_is_admin(self):
        return self.is_admin
    
    def account_info_to_string(self):
        return f"Username: {self.user_name}\tPassword: {self.password}\tAdmin: {self.is_admin}"


# Guest account class
class Guest(Account):
    def __init__(self):
        self.user_name = "Guest"
        self.password = ""
        self.is_admin = False
    
    def account_info_to_string(self):
        return "Guest User"
    


# Function to register a new user - appends the users account information to the given file.
def register_user(user_name, password, is_admin, file_path):
    # First, make sure that the user has inputted a unique username.
    accounts_df = pd.read_csv(file_path)
    user_data = accounts_df[accounts_df["user_name"] == user_name]

    # If no account exists with the same username, go ahead and create the account
    if user_data.empty:
        user_info = [user_name,password,is_admin]
        with open(file_path,"a",newline="") as account_file:
            writer = csv.writer(account_file)
            writer.writerow(user_info) # Append the new account information to the file.
            account_file.close()

            #print(f"Account successfully created! You are now logged in.\nWelcome {user_name}!")
            current_account = Account(user_name,password,is_admin) # Create a new Account object with the users data
            return True, current_account, "Registered"
    else:
        #print(f"Sorry, the username {user_name} is already taken, Please try again.")
        return False, Guest(), f"Sorry, the username {user_name} is already taken, Please try again."



# Function to log user into the program. Returns a boolean (successful or unsuccessful login)
def login(user_name, password, file_path):
    try:
        accounts_df = pd.read_csv(file_path)

        # Check if the user is registered.
        user_data = accounts_df[accounts_df["user_name"] == user_name]

        if user_data.empty:
            #print(f"No account found for the username {user_name}.")
            return False, Guest(), f"No account found for the username {user_name}."
        
        user_data = user_data.iloc[0]
        
        # Verify the user's password
        if str(user_data.iloc[1]) == password:
            #print(f"Login successful!\nWelcome {user_name}!")
            current_account = Account(user_data["user_name"],user_data["password"],user_data["is_admin"]) # Create a new Account object with the users data
            return True, current_account, "Logged In."
        else:
            #print("Incorrect password.")
            return False, Guest(), "Incorrect password."

    except Exception as e:
        #print("An error occurred...")
        print(e)
        return False, Guest(), f"{e} error occurred..."



# Function to log user out of the program.
def log_out():
    #print("Successfully logged out.")
    return False, Guest(), "Successfully logged out."



#Testing the functions + example usage
# logged_in = False
# current_account = Guest()

# print("---------------------------------------")
# print(f"1. {logged_in = }\n{current_account.account_info_to_string()}")
# logged_in, current_account = register_user("ryan","password",True,"src\\Data\\accountInfo.csv")


# print("---------------------------------------")
# print(f"2. {logged_in = }\n{current_account.account_info_to_string()}")
# logged_in, current_account = register_user("matteo","password",False,"src\\Data\\accountInfo.csv")


# print("---------------------------------------")
# print(f"3. {logged_in = }\n{current_account.account_info_to_string()}")
# logged_in, current_account = register_user("tomasz","password",True,"src\\Data\\accountInfo.csv")


# print("---------------------------------------")
# print(f"4. {logged_in = }\n{current_account.account_info_to_string()}")
# logged_in, current_account = login("erica","password","src\\Data\\accountInfo.csv")


# print("---------------------------------------")
# print(f"5. {logged_in = }\n{current_account.account_info_to_string()}")
# logged_in, current_account = login("ryan","password","src\\Data\\accountInfo.csv")


# print("---------------------------------------")
# print(f"6. {logged_in = }\n{current_account.account_info_to_string()}")
# logged_in, current_account = login("nolan","password","src\\Data\\accountInfo.csv")


# print("---------------------------------------")
# print(f"7. {logged_in = }\n{current_account.account_info_to_string()}")
# logged_in, current_account = log_out()


# print("---------------------------------------")
# print(f"8. {logged_in = }\n{current_account.account_info_to_string()}")