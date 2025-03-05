from customtkinter import *
from PIL import Image
import accounts


app = CTk()
app.title("Celebrity Bio Application")
app.geometry("1280x720")
app.resizable(False, False)

#Store the user Account (Default is Guest account)
userAccount = accounts.Guest()

#Frames for diffrent pages
mainFrame = None
signInFrame = None
favoritesFrame = None

# Hide all frames
def hideAllFrames():
    if mainFrame:
        mainFrame.place_forget()
    if signInFrame:
        signInFrame.place_forget()
    if favoritesFrame:
        favoritesFrame.place_forget()

# Show the main frame
def showMainFrame():
    hideAllFrames()
    createMainFrame()
    mainFrame.place(relx=0.5, rely=0.5, anchor="center")

# Show the login frame
def showSignInFrame(signInType):
    hideAllFrames()
    #signInFrame.place(relx=0.5, rely=0.5, anchor="center")
    createSignInFrame(signInType)

def createMainFrame():
    global mainFrame, userAccount
    
    # Frame to house all elements
    mainFrame = CTkFrame(app, width=1280, height=720)
    mainFrame.place(relx=0.5, rely=0.5, anchor="center")  

    # topFrame to house top elements (user info, login/register buttons)
    topFrame = CTkFrame(mainFrame, width=1280, height=100)
    topFrame.place(relx=0.5, rely=0.05, anchor="center")

    #User info
    userLabel = CTkLabel(mainFrame, text=userAccount.get_user_name(), font=("Arial", 22))
    userLabel.place(relx=0.08, rely=0.05, anchor="center")
    #TODO Profile Picture 
    #profilePicture = CTkImage(dark_image=Image.open("src\\Data\\Images\\user\\default.png"), size=(30,30))
    #profilePictureLabel = CTkLabel(mainFrame, image=profilePicture)
    #profilePictureLabel.place(relx=0.01, rely=0.05, anchor="w")

    #Login / Register buttons
    loginButton = CTkButton(mainFrame, text="Login", command=lambda: showSignInFrame("Login to Account"), width=60) #keep the same width as the register button
    loginButton.place(relx=0.96, rely=0.05, anchor="center")
    registerButton = CTkButton(mainFrame, text="Register", command=lambda: showSignInFrame("Register Account"), width=15)
    registerButton.place(relx=0.91, rely=0.05, anchor="center")

    #Celebrity management buttons
    addButton = CTkButton(mainFrame, text="Add", command=None, width=60)
    addButton.place(relx=0.4, rely=0.5, anchor="center")
    removeButton = CTkButton(mainFrame, text="Remove", command=None, width=60)
    removeButton.place(relx=0.5, rely=0.5, anchor="center")
    editButton = CTkButton(mainFrame, text="Edit", command=None, width=60)
    editButton.place(relx=0.6, rely=0.5, anchor="center")

    #Searchbar
    searchbar = CTkEntry(mainFrame, width=500, placeholder_text="Search for a celebrity")
    searchbar.place(relx=0.5, rely=0.05, anchor="center")

def createSignInFrame(signInType):
    def printToConsole():
        global userAccount
        username = usernameField.get()
        password = passwordField.get()

        if signInType == "Login to Account":    
            successfulRegister, newUserAccount, successText = accounts.login(username, password, "src\\Data\\accountInfo.csv")
        elif signInType == "Register Account":
            successfulRegister, newUserAccount, successText = accounts.register_user(username, password, False, "src\\Data\\accountInfo.csv")
        else:
            print("Invalid sign in type")
            
        if successfulRegister:
            userAccount = newUserAccount
            successLabel = CTkLabel(signInFrame, text=f"Successfuly {successText}\n Redirecting Home", font=("Arial", 18), width=640)
            successLabel.place(relx=0.5, rely=0.3, anchor="center")
            app.after(2000, showMainFrame)
        else:
            successLabel = CTkLabel(signInFrame, text=successText, font=("Arial", 18), width=640)
            successLabel.place(relx=0.5, rely=0.3, anchor="center")

    global signInFrame
    signInFrame = CTkFrame(app, width=1280, height=720)
    signInFrame.place(relx=0.5, rely=0.5, anchor="center")  

    loginLabel = CTkLabel(signInFrame, text=signInType, font=("Arial", 22))
    loginLabel.place(relx=0.5, rely=0.2, anchor="center")

    #Username
    usernameField = CTkEntry(signInFrame, width=500, placeholder_text="Enter your username...")
    usernameField.place(relx=0.5, rely=0.5, anchor="center")
    #Password
    passwordField = CTkEntry(signInFrame, width=500, placeholder_text="Enter your password...", show="*")
    passwordField.place(relx=0.5, rely=0.6, anchor="center")
    #Submit
    submitButton = CTkButton(signInFrame, text=signInType, command=printToConsole, width=80, font=("Arial", 16))
    submitButton.place(relx=0.5, rely=0.8, anchor="center")

    #go back to main menu
    backButton = CTkButton(signInFrame, text="home", command=showMainFrame, width=60)
    backButton.place(relx=0.1, rely=0.05, anchor="center")


createMainFrame()

showMainFrame()
app.mainloop()