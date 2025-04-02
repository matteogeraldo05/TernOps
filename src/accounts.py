import pandas as pd
import csv

# Account class
class Account:
    def __init__(self, name: str, pw: str, admin: bool, fav: list):
        self.user_name = name
        self.password = pw
        self.is_admin = admin
        self.favourites = fav or []
    
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
    
    def get_favourites(self):
        return self.favourites
    
    def add_favourite(self, file_path, celebrity_name):
        # check if the celebrity has already been favourited
        if celebrity_name in self.favourites:
            print(f"Celebrity already found in {self.user_name}'s favourites!")
            return
        
        # add the celebrity's name to the list of their favourites
        self.favourites.append(celebrity_name)

        # update the csv file with the new list
        accounts_df = pd.read_csv(file_path) 
        mask = accounts_df["user_name"] == self.user_name
        accounts_df.loc[mask, "favourites"] = ",".join(self.favourites)
        accounts_df.to_csv(file_path, index=False)

        print(f"{celebrity_name} added to {self.user_name}'s favourites!")

    def remove_favourite(self, file_path, celebrity_name):
        # check if the celebrity is in the users favourites
        if celebrity_name not in self.favourites:
            print(f"Celebrity not found in {self.user_name}'s favourites!")
            return
        
        # remove the celebrity's name from the users list of favourites
        self.favourites.remove(celebrity_name)

        # update the csv file with the new list
        accounts_df = pd.read_csv(file_path) 
        mask = accounts_df["user_name"] == self.user_name
        accounts_df.loc[mask, "favourites"] = ",".join(self.favourites)
        accounts_df.to_csv(file_path, index=False)

        print(f"{celebrity_name} removed from {self.user_name}'s favourites!")

    def account_info_to_string(self):\
        # Join the favourite list into string like "Mark Hamill, John Doe"
        fav_str = ", ".join(self.favourites) if self.favourites else "none"
        return f"Username: {self.user_name}\tPassword: {self.password}\tAdmin: {self.is_admin}\tFavs: {fav_str}"


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
            current_account = Account(user_name,password,is_admin,[]) # Create a new Account object with the users data
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
            # extract the users favourites from user_data as a list
            favourites_list = user_data["favourites"]
            if pd.isna(favourites_list):  
                favourites_list = []  
            else:
                favourites_list = favourites_list.split(",")

            #print(f"Login successful!\nWelcome {user_name}!")
            current_account = Account(user_data["user_name"], user_data["password"], user_data["is_admin"], favourites_list) # Create a new Account object with the users data
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