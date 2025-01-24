import hashlib

def signup():
    username = input("Enter username: ")
    password = input("Enter password: ")
    conf_pass = input("Confirm password: ")

    if conf_pass == password:
        hide = conf_pass.encode()
        hash_1 = hashlib.md5(hide).hexdigest()

        with open("Registered.csv") as file:
            file.write(username + "\n")
            file.write(hash_1)
        file.close
        print("You have registered successfully!")
    else:
        print("Passwords is not same as above! \n")


def login():
    username = input("Enter username: ")
    password = input("Enter password: ")

    check = password.encode()
    check_hash = hashlib.md5(check).hexdigest()
    with open("Registered.csv", "r") as file:
        stored_user, stored_pass = file.read().split("\n")
    file.close()
    if username == stored_user and check_hash == stored_pass:
         print("Logged in Successfully!")
    else:
         print("Login failed! \n")

while 1:
    print("********** Login System **********")
    print("1.Signup")
    print("2.Login")
    print("3.Exit")
    ch = int(input("Enter your choice: "))
    if ch == 1:
        signup()
    elif ch == 2:
        login()
    elif ch == 3:
        break
    else:
        print("Wrong Choice!")
