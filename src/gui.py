from customtkinter import *
from CTkMessagebox import CTkMessagebox
import accounts
import functions


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
    def logoutAndShowMain():
        global userAccount
        userAccount = accounts.Guest() #todo
        showMainFrame()
    
    def removeCelebrity(firstName, lastName):
        deleteCeleb = CTkMessagebox(message=f"Are you sure you would like to delete {firstName} {lastName}? This action is permenant.", icon="warning", option_1="Yes", option_2="No")
        if deleteCeleb.get() == "Yes":
            functions.delete_data("src\\Data\\celebrities.csv", firstName, lastName)
            showMainFrame()
        else:
            pass

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

    if userAccount.get_user_name() == "Guest":
        # Login / Register buttons
        loginButton = CTkButton(topFrame, text="Login", command=lambda: showSignInFrame("Login to Account"), width=60)
        loginButton.pack(side="right", padx=15)
        registerButton = CTkButton(topFrame, text="Register", command=lambda: showSignInFrame("Register Account"), width=60)
        registerButton.pack(side="right")
    else:
        # Logout button
        logoutButton = CTkButton(topFrame, text="Logout", command=logoutAndShowMain, width=60) 
        logoutButton.pack(side="right", padx=15)


    # Add Celebrity
    addButton = CTkButton(topFrame, text="Add", command=lambda: createEditCelebrityFrame("Add"), width=60)
    addButton.pack(side="right", padx=90)

    # Searchbar
    searchbar = CTkEntry(topFrame, width=500, placeholder_text="Search for a celebrity")
    searchbar.pack(side="right", pady=20)

    # Scrollable frame to house list of celebrities
    scrollFrame = CTkScrollableFrame(mainFrame, width=1280, height=660)
    scrollFrame.pack(fill="both")

    # Load the celebrities from CSV file
    celebrities = functions.load_celebrities_file("src/Data/celebrities.csv")

    # Create a row for each celebrity in the CSV file
    for celebrity in celebrities:
        firstName = celebrity["first_name"]
        lastName = celebrity["last_name"]
        dateOfBirth = celebrity["date_of_birth"]

        # Create the row using the celebrity data
        rowFrame = CTkFrame(scrollFrame, width=1280, height=100)
        rowFrame.pack(fill="x", pady=5)

        # Name and DOB
        nameAndDOBLabel = CTkLabel(rowFrame, text=f"{firstName} {lastName} - {dateOfBirth}", font=("Arial", 16))
        nameAndDOBLabel.pack(side="left", padx=20)
        
        # Celebrity management buttons
        editButton = CTkButton(rowFrame, text="edit", command=None, width=60)
        editButton.pack(side="right", padx=10)

        removeButton = CTkButton(rowFrame, text="delete", command=lambda firstName=celebrity["first_name"], lastName=celebrity["last_name"]: removeCelebrity(firstName, lastName), width=60)
        removeButton.pack(side="right", padx=10)

        # Favorite button
        favoriteButton = CTkButton(rowFrame, text="favorite", command=None, width=60)
        favoriteButton.pack(side="right", padx=10)

def createSignInFrame(signInType):
    def printToConsole():
        global userAccount
        username = str(usernameField.get())
        password = str(passwordField.get())

        if signInType == "Login to Account":    
            successfulRegister, newUserAccount, successText = accounts.login(username, password, "src\\Data\\accountInfo.csv")
            print(f"successfulRegister: {successfulRegister}")
            print(f"Username: {username}")
            print(f"Password: {password}")

        elif signInType == "Register Account":
            successfulRegister, newUserAccount, successText = accounts.register_user(username, password, False, "src\\Data\\accountInfo.csv")
        else:
            print("Invalid sign in type")
            
        if successfulRegister:
            userAccount = newUserAccount
            successLabel = CTkLabel(signInFrame, text=f"Successfuly {successText}\n Redirecting Home", font=("Arial", 18), width=640, text_color="green")
            successLabel.place(relx=0.5, rely=0.3, anchor="center")
            app.after(2000, showMainFrame)
        else:
            successLabel = CTkLabel(signInFrame, text=successText, font=("Arial", 18), width=640, text_color="red")
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
    global localImagePath

    def getImagePath():
        global localImagePath
        filePath = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;")])
        filePathLabel = CTkLabel(editCelebrityFrame, text=f"Image: {filePath}", font=("Arial", 16))
        filePathLabel.place(relx=0.5, rely=0.6, anchor="center")
        celebrityName = firstNameField.get() + "_" + lastNameField.get()
        localImagePath = functions.copy_image_to_folder(filePath, celebrityName)

    def editCelebrity():
        firstName = firstNameField.get()
        lastName = lastNameField.get()
        dateOfBirth = dobField.get()
        imagePath = localImagePath

        celebrityData = {
            "first_name": firstName,
            "last_name": lastName,
            "date_of_birth": dateOfBirth,
            "images_path": imagePath
        }

        # Add the celebrity to the CSV
        functions.add_data("src/Data/celebrities.csv", celebrityData)

        # Show success message
        successMessage = CTkLabel(editCelebrityFrame, text=f"Successfully added {firstName} {lastName}!", font=("Arial", 16), text_color="green")
        successMessage.place(relx=0.5, rely=0.75, anchor="center")
        app.after(2000, showMainFrame)


    global editCelebrityFrame
    
    editCelebrityFrame = CTkFrame(app, width=1280, height=720)
    editCelebrityFrame.place(relx=0.5, rely=0.5, anchor="center")
    
    # Add a label to inform the user of the action
    editLabel = CTkLabel(editCelebrityFrame, text=f"Please fill in the details to {editType} a celebrity", font=("Arial", 22))
    editLabel.place(relx=0.5, rely=0.1, anchor="center")

    # Fields for first name, last name, date of birth, and image path
    firstNameField = CTkEntry(editCelebrityFrame, width=500, placeholder_text="Enter First Name")
    firstNameField.place(relx=0.5, rely=0.3, anchor="center")

    lastNameField = CTkEntry(editCelebrityFrame, width=500, placeholder_text="Enter Last Name")
    lastNameField.place(relx=0.5, rely=0.4, anchor="center")

    dobField = CTkEntry(editCelebrityFrame, width=500, placeholder_text="Enter Date of Birth (ex. October 29, 1955)")
    dobField.place(relx=0.5, rely=0.5, anchor="center")

    imageSelectButton = CTkButton(editCelebrityFrame, width=100, text="Select Image", command=getImagePath)
    imageSelectButton.place(relx=0.5, rely=0.7, anchor="center")

    # Submit button to add celebrity
    submitButton = CTkButton(editCelebrityFrame, text="Add Celebrity", command=editCelebrity, width=100, font=("Arial", 16))
    submitButton.place(relx=0.5, rely=0.8, anchor="center")

    # Go back to main menu
    backButton = CTkButton(editCelebrityFrame, text="Home", command=showMainFrame, width=60)
    backButton.place(relx=0.05, rely=0.05, anchor="center")

createMainFrame()

showMainFrame()
app.mainloop()