from customtkinter import *
import accounts
app = CTk()
app.title("Celebrity Bio Application")
app.geometry("1280x720")
app.resizable(False, False)

#Frames for diffrent pages
mainFrame = None
loginFrame = None

def hideAllFrames():
    if mainFrame:
        mainFrame.place_forget()
    if loginFrame:
        loginFrame.place_forget()

# Show the main frame
def showMainFrame():
    hideAllFrames()
    mainFrame.place(relx=0.5, rely=0.5, anchor="center")

# Show the login frame
def showLoginFrame():
    hideAllFrames()
    loginFrame.place(relx=0.5, rely=0.5, anchor="center")

def registerAccount():
    pass

def addCelebrity():
    pass

def removeCelebrity():
    pass

def editCelebrity():
    pass

def createMainFrame():
    global mainFrame
    mainFrame = CTkFrame(app, width=1280, height=720)
    mainFrame.place(relx=0.5, rely=0.5, anchor="center")  
    #Login / Register buttons
    loginButton = CTkButton(mainFrame, text="Login", command=showLoginFrame, width=60) #keep the same width as the register button
    loginButton.place(relx=0.96, rely=0.05, anchor="center")
    registerButton = CTkButton(mainFrame, text="Register", command=registerAccount, width=15)
    registerButton.place(relx=0.91, rely=0.05, anchor="center")

    #Celebrity management buttons
    addButton = CTkButton(mainFrame, text="Add", command=addCelebrity, width=60)
    addButton.place(relx=0.4, rely=0.5, anchor="center")
    removeButton = CTkButton(mainFrame, text="Remove", command=removeCelebrity, width=60)
    removeButton.place(relx=0.5, rely=0.5, anchor="center")
    editButton = CTkButton(mainFrame, text="Edit", command=editCelebrity, width=60)
    editButton.place(relx=0.6, rely=0.5, anchor="center")

    #Searchbar
    searchbar = CTkEntry(mainFrame, width=500, placeholder_text="Search for a celebrity")
    searchbar.place(relx=0.5, rely=0.05, anchor="center")


def createLoginFrame():
    def printToConsole():
        username = usernameField.get()
        password = passwordField.get()
        print(f"Username: {username}, Password: {password}")
        
    global loginFrame
    loginFrame = CTkFrame(app, width=1280, height=720)
    loginFrame.place(relx=0.5, rely=0.5, anchor="center")  

    loginLabel = CTkLabel(loginFrame, text="Login", font=("Arial", 22))
    loginLabel.place(relx=0.5, rely=0.2, anchor="center")

    #Username
    usernameField = CTkEntry(loginFrame, width=500, placeholder_text="Enter your username...")
    usernameField.place(relx=0.5, rely=0.5, anchor="center")
    #Password
    passwordField = CTkEntry(loginFrame, width=500, placeholder_text="Enter your password...", show="*")
    passwordField.place(relx=0.5, rely=0.6, anchor="center")
    #Submit
    submitButton = CTkButton(loginFrame, text="Login", command=printToConsole, width=80, font=("Arial", 16))
    submitButton.place(relx=0.5, rely=0.8, anchor="center")

    #go back to main menu
    backButton = CTkButton(loginFrame, text="home", command=showMainFrame, width=60)
    backButton.place(relx=0.1, rely=0.05, anchor="center")

createLoginFrame()
createMainFrame()

showMainFrame()
app.mainloop()