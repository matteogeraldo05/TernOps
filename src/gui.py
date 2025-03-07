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
editCelebrityFrame = None
favoritesFrame = None

# Hide all frames
def hideAllFrames():
    if mainFrame:
        mainFrame.pack_forget()
    if signInFrame:
        signInFrame.place_forget()
    if favoritesFrame:
        favoritesFrame.pack_forget()
    if editCelebrityFrame:
        editCelebrityFrame.pack_forget()

# Show the main frame
def showMainFrame():
    hideAllFrames()
    createMainFrame()
    mainFrame.pack(fill="both", expand=True)

# Show the login frame
def showSignInFrame(signInType):
    hideAllFrames()
    createSignInFrame(signInType)

def showEditCelebrityFrame():
    hideAllFrames()
    createEditCelebrityFrame()

def createMainFrame():
    global mainFrame, userAccount

    # Frame to house all elements
    mainFrame = CTkFrame(app, width=1280, height=720)
    mainFrame.pack(fill="both", expand=True)

    topFrame = CTkFrame(mainFrame, width=1280, height=70)
    topFrame.pack(fill="x", side="top")

    #User info
    userLabel = CTkLabel(topFrame, text=userAccount.get_user_name(), font=("Arial", 22))
    userLabel.pack(side="left", padx=40)
    #TODO Profile Picture 
    #profilePicture = CTkImage(dark_image=Image.open("src\\Data\\Images\\user\\default.png"), size=(30,30))
    #profilePictureLabel = CTkLabel(mainFrame, image=profilePicture)

    # Login / Register buttons
    loginButton = CTkButton(topFrame, text="Login", command=lambda: showSignInFrame("Login to Account"), width=60) #keep the same width as the register button
    loginButton.pack(side="right", padx=15)
    registerButton = CTkButton(topFrame, text="Register", command=lambda: showSignInFrame("Register Account"), width=15)
    registerButton.pack(side="right")

    # Searchbar
    searchbar = CTkEntry(topFrame, width=500, placeholder_text="Search for a celebrity")
    searchbar.pack(side="top", pady=10)

    # Scrollable frame to house list of celebrities
    scrollFrame = CTkScrollableFrame(mainFrame, width=1280, height=660)
    scrollFrame.pack(fill="both")
    
    #Celebrity management buttons
    addButton = CTkButton(scrollFrame, text="Add", command=None, width=60)
    addButton.pack(side="left", padx=10)
    removeButton = CTkButton(scrollFrame, text="Remove", command=None, width=60)
    removeButton.pack(side="left", padx=10)
    editButton = CTkButton(scrollFrame, text="Edit", command=None, width=60)
    editButton.pack(side="left", padx=10)

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
    backButton.place(relx=0.05, rely=0.05, anchor="center")

def createEditCelebrityFrame(editType):
    global editCelebrityFrame
    
    editCelebrityFrame = CTkFrame(app, width=1280, height=720)
    editCelebrityFrame.place(relx=0.5, rely=0.5, anchor="center")

    
    submitButton = CTkButton(signInFrame, text=editType, command=None, width=80, font=("Arial", 16))
    submitButton.place(relx=0.5, rely=0.8, anchor="center")

    #go back to main menu
    backButton = CTkButton(signInFrame, text="home", command=showMainFrame, width=60)
    backButton.place(relx=0.05, rely=0.05, anchor="center")

createMainFrame()

showMainFrame()
app.mainloop()