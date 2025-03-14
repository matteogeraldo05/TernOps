from customtkinter import *
from CTkMessagebox import CTkMessagebox
from PIL import Image
import accounts
import functions


app = CTk()
app.title("Celebrity Bio Application")
app.geometry("1280x720")
app.resizable(False, False)
colorPalette = {"black": "#000000",
                "veryDarkGray": "#121212",
                "darkGray": "#212121",
                "mediumGray": "#2f2f2f",
                "neutralGray": "#424242",
                "lightGray": "#535353",
                "white": "#ffffff"}

#Store the user Account (Default is Guest account)
userAccount = accounts.Guest()

#Frames for diffrent pages
mainFrame = None
signInFrame = None
editCelebrityFrame = None
celebrityFrame = None
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
    if celebrityFrame:
        celebrityFrame.pack_forget()

# Show the main frame
def showMainFrame():
    hideAllFrames()
    createMainFrame()
    mainFrame.pack(fill="both", expand=True)

# Show the login frame
def showSignInFrame(signInType):
    hideAllFrames()
    createSignInFrame(signInType)

# Show the edit celebrity frame
def showEditCelebrityFrame():
    hideAllFrames()
    createEditCelebrityFrame()

# Show the celebrity frame
def showCelebrityFrame():
    hideAllFrames()
    createCelebrityFrame()

# Create the favorites frame
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

    topFrame = CTkFrame(mainFrame, width=1280, height=70, fg_color="#121212", corner_radius=0)
    topFrame.pack(fill="x", side="top")

    #TODO Profile Picture 
    profilePicture = CTkImage(dark_image=Image.open("src\\Data\\Images\\user\\user.png"), size=(30,30))
    profilePictureLabel = CTkLabel(topFrame, image=profilePicture, text="")
    profilePictureLabel.place(x=20, y=20)
    #User info
    userLabel = CTkLabel(topFrame, text=userAccount.get_user_name(), font=("Arial", 28))
    userLabel.place(x=70, y=20)
    # If the username is too long replce with ...
    if len(userLabel.cget("text")) > 20:
        userLabel.configure(text=userLabel.cget("text")[:20] + "...")

    if userAccount.get_user_name() == "Guest":
        # Login / Register buttons
        loginButton = CTkButton(topFrame, text="Login", font=("Arial", 14), command=lambda: showSignInFrame("Login to Account"), width=60, height=36, fg_color=colorPalette["mediumGray"], hover_color=colorPalette["lightGray"])
        loginButton.place(x=1280 - 60 - 20, y=16)  
        registerButton = CTkButton(topFrame, text="Register", font=("Arial", 14), command=lambda: showSignInFrame("Register Account"), width=60, height=36, fg_color=colorPalette["mediumGray"], hover_color=colorPalette["lightGray"])
        registerButton.place(x=1280 - 60 - 20 - 60 - 20, y=16)
    else:
        # Logout button
        logoutButton = CTkButton(topFrame, text="Logout", font=("Arial", 14), command=logoutAndShowMain, width=60, height=36, fg_color=colorPalette["mediumGray"], hover_color=colorPalette["lightGray"])
        logoutButton.place(x=1280 - 60 - 20, y=20)

    # Searchbar
    searchbar = CTkEntry(topFrame, width=500, placeholder_text="Search for a celebrity", border_width=4, corner_radius=18, font=("Arial", 14), height=46, fg_color=colorPalette["darkGray"])
    searchbar.place(relx=0.5, rely=0.5, anchor="center")
    searchbar.bind("<Return>", lambda event: print(searchbar.get()))
    # Magnifying glass icon
    magnifyIcon = CTkImage(dark_image=Image.open("src\\Data\\Images\\system\\magnify.png"), size=(30, 30))
    # Create a label with the magnify icon and place it inside the search bar
    magnifyLabel = CTkLabel(topFrame, image=magnifyIcon, text="")
    magnifyLabel.place(relx=0.715, rely=0.5, anchor="center")  
    
    # Add Celebrity
    addButton = CTkButton(topFrame, text="+", font=("Arial",24), command=lambda: createEditCelebrityFrame("Add"), width=36, height=36, fg_color=colorPalette["mediumGray"], hover_color=colorPalette["lightGray"])
    addButton.place(relx=0.75, rely=0.5, anchor="center")

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
        dateOfDeath = celebrity["date_of_death"]
        imagesPath = celebrity["images_path"]
        biography = str(celebrity["biography"])
        achievements = celebrity["achievements"]
        industry = celebrity["industry"]
        family = celebrity["family"]
        associations = celebrity["associations"]
        controversies = celebrity["controversies"]
        discography = celebrity["discography"]
        filmography = celebrity["filmography"]
        genres = celebrity["genres"]
        influence = celebrity["influence"]
        political = celebrity["political_orientation"]
        gender = celebrity["gender"]
        netWorth = celebrity["net_worth"]

        # Ccreate a a breif bio
        brief_bio = biography[:100] + "..."
        # Create the row using the celebrity data
        rowFrame = CTkFrame(scrollFrame, width=1280, height=100)
        rowFrame.pack(fill="x", pady=5)

        # Name and DOB
        nameAndDOBLabel = CTkLabel(rowFrame, text=f"{firstName} {lastName} - {dateOfBirth}", font=("Arial", 16))
        nameAndDOBLabel.pack(side="left", padx=20)
        # Biography labek
        bioLabel = CTkLabel(rowFrame, text=brief_bio, font=("Arial", 12))
        bioLabel.pack(side="left", padx=20)
        # Celebrity management buttons
        editButton = CTkButton(rowFrame, text="edit", command=None, width=60)
        editButton.pack(side="right", padx=10)

        removeButton = CTkButton(rowFrame, text="delete", command=lambda firstName=celebrity["first_name"], lastName=celebrity["last_name"]: removeCelebrity(firstName, lastName), width=60)
        removeButton.pack(side="right", padx=10)

        # Favorite button
        favoriteButton = CTkButton(rowFrame, text="favorite", command=None, width=60)
        favoriteButton.pack(side="right", padx=10)

        # If the user clicks on the row, show the celebrity's full info
        rowFrame.bind("<Button-1>", lambda e, celeb=celebrity: createCelebrityFrame(celeb))

# Create the sign in frame
def createSignInFrame(signInType):
    def printToLabel():
        global userAccount
        username = str(usernameField.get())
        password = str(passwordField.get())

        if signInType == "Login to Account":    
            successfulRegister, newUserAccount, successText = accounts.login(username, password, "src\\Data\\accountInfo.csv")

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
    passwordField.bind("<Return>", lambda event: printToLabel())
    #Submit
    submitButton = CTkButton(signInFrame, text=signInType, command=printToLabel, width=80, font=("Arial", 16))
    submitButton.place(relx=0.5, rely=0.8, anchor="center")

    #go back to main menu
    backButton = CTkButton(signInFrame, text="home", command=showMainFrame, width=60)
    backButton.place(relx=0.05, rely=0.05, anchor="center")

# Create the edit celebrity frame
def createEditCelebrityFrame(editType, firstName=None, lastName=None):
    global localImagePath

    def getImagePath():
        global localImagePath
        filePath = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;")])
        filePathLabel = CTkLabel(editCelebrityFrame, text=f"Image: {filePath}", font=("Arial", 16))
        filePathLabel.place(x=120, y=650)
        celebrityName = firstNameField.get() + "_" + lastNameField.get()
        localImagePath = functions.copy_image_to_folder(filePath, celebrityName)

    def editCelebrity():
        firstName = firstNameField.get()
        lastName = lastNameField.get()
        dateOfBirth = dateOfBirthField.get()
        imagePath = localImagePath

        if not firstName or not lastName or not dateOfBirth:
            successMessage = CTkLabel(editCelebrityFrame, text="Please fill in all fields.", font=("Arial", 16), text_color="red")
            successMessage.place(relx=0.5, rely=0.75, anchor="center")
            return

        if editType == "Add":
            # Add the celebrity to the CSV
            celebrityData = {
                "first_name": firstName,
                "last_name": lastName,
                "date_of_birth": dateOfBirth,
                "images_path": imagePath,
                # "date_of_death" : dateOfDeath,
                # "biography" : biography,
                # "achievements" : achievements,
                # "industry" : industry,
                # "family" : family,
                # "associations" : associations,
                # "controversies" : controversies,
                # "discography" : discography,
                # "filmography" : filmography,
                # "genres" : genres,
                # "influence" : influence,
                # "political_orientation" : political,
                # "gender" : gender,
                # "net_worth" : netWorth
            }

            # Add the celebrity to the CSV
            functions.add_data("src/Data/celebrities.csv", celebrityData)

            # Show success message
            successMessage = CTkLabel(editCelebrityFrame, text=f"Successfully added {firstName} {lastName}!", font=("Arial", 16), text_color="green")
            successMessage.place(relx=0.5, rely=0.75, anchor="center")
            app.after(2000, showMainFrame)

        elif editType == "Edit":
            # Update the celebrity's data in the CSV
            functions.edit_data("src/Data/celebrities.csv", "first_name", firstName, dateOfBirth, imagePath)

            # Show success message
            successMessage = CTkLabel(editCelebrityFrame, text=f"Successfully edited {firstName} {lastName}!", font=("Arial", 16), text_color="green")
            successMessage.place(relx=0.5, rely=0.75, anchor="center")
            app.after(2000, showMainFrame)

        else:
            print("Invalid edit type")

    global editCelebrityFrame
    
    editCelebrityFrame = CTkFrame(app, width=1280, height=720)
    editCelebrityFrame.place(relx=0.5, rely=0.5, anchor="center")
    
    # Add a label to inform the user of the action
    editLabel = CTkLabel(editCelebrityFrame, text=f"Please fill in the details to {editType} a celebrity", font=("Arial", 22))
    editLabel.place(relx=0.5, rely=0.1, anchor="center")

    # ~Left Side
    # First Name
    firstNameLabel = CTkLabel(editCelebrityFrame, text="First Name:")
    firstNameLabel.place(x=20, y=110)  # Place the label above the entry field
    firstNameField = CTkEntry(editCelebrityFrame, width=150, placeholder_text="Enter First Name")
    firstNameField.place(x=120, y=110)  # Shift the entry field to the right

    # Last Name
    lastNameLabel = CTkLabel(editCelebrityFrame, text="Last Name:")
    lastNameLabel.place(x=20, y=150)
    lastNameField = CTkEntry(editCelebrityFrame, width=150, placeholder_text="Enter Last Name")
    lastNameField.place(x=120, y=150)

    # Date of Birth
    dateOfBirthLabel = CTkLabel(editCelebrityFrame, text="Date of Birth:")
    dateOfBirthLabel.place(x=20, y=190)
    dateOfBirthField = CTkEntry(editCelebrityFrame, width=150, placeholder_text="ex. October 29, 1955")
    dateOfBirthField.place(x=120, y=190)

    # Date of Death
    dateOfDeathLabel = CTkLabel(editCelebrityFrame, text="Date of Death:")
    dateOfDeathLabel.place(x=20, y=230)
    dateOfDeathField = CTkEntry(editCelebrityFrame, width=150, placeholder_text="ex. June 12, 2022")
    dateOfDeathField.place(x=120, y=230)

    # Industry
    industryLabel = CTkLabel(editCelebrityFrame, text="Industry:")
    industryLabel.place(x=20, y=270)
    industryField = CTkEntry(editCelebrityFrame, width=150, placeholder_text="Enter Industry")
    industryField.place(x=120, y=270)

    # Associations
    associationsLabel = CTkLabel(editCelebrityFrame, text="Associations:")
    associationsLabel.place(x=20, y=310)
    associationsField = CTkEntry(editCelebrityFrame, width=150, placeholder_text="Enter Associations")
    associationsField.place(x=120, y=310)

    # Gender
    genderLabel = CTkLabel(editCelebrityFrame, text="Gender:")
    genderLabel.place(x=20, y=350)
    genderField = CTkComboBox(master=app, values=["Male", "Female", "Other"], width=150)
    genderField.place(x=120, y=350)

    # Biography
    biographyLabel = CTkLabel(editCelebrityFrame, text="Biography:")
    biographyLabel.place(x=20, y=390)
    biographyField = CTkTextbox(editCelebrityFrame, width=450)
    biographyField.place(x=120, y=390)

    # Image
    imageSelectButton = CTkButton(editCelebrityFrame, width=100, text="Select Image", command=getImagePath)
    imageSelectButton.place(x=250, y=650)


    #Right side
    # Net Worth
    netWorthLabel = CTkLabel(editCelebrityFrame, text="Net Worth")
    netWorthLabel.place(x=650, y=110)
    netWorthField = CTkEntry(editCelebrityFrame, width=200, placeholder_text="Enter Net Worth")
    netWorthField.place(x=750, y=110)

    # Family
    familyField = CTkLabel(editCelebrityFrame, text="Family:")
    familyField.place(x=650, y=150)
    familyField = CTkEntry(editCelebrityFrame, width=200, placeholder_text="Enter Family")
    familyField.place(x=750, y=150)

    # Controversies
    controversiesLabel = CTkLabel(editCelebrityFrame, text="Controversies:")
    controversiesLabel.place(x=650, y=190)
    controversiesField = CTkEntry(editCelebrityFrame, width=200, placeholder_text="Enter Controversies")
    controversiesField.place(x=750, y=190)

    # Discography
    discographyLabel = CTkLabel(editCelebrityFrame, text="Controversies:")
    discographyLabel.place(x=650, y=230)
    discographyField = CTkEntry(editCelebrityFrame, width=200, placeholder_text="Enter Discography")
    discographyField.place(x=750, y=230)

    # Films
    filmographyLabel = CTkLabel(editCelebrityFrame, text="Filmography:")
    filmographyLabel.place(x=650, y=270)
    filmographyField = CTkEntry(editCelebrityFrame, width=200, placeholder_text="Enter Filmography")
    filmographyField.place(x=750, y=270)

    # Genre
    genresLabel = CTkLabel(editCelebrityFrame, text="Genres:")
    genderLabel.place(x=650, y=310)
    genresField = CTkEntry(editCelebrityFrame, width=200, placeholder_text="Enter Genres")
    genresField.place(x=750, y=310)

    # Influence
    influenceLabel = CTkLabel(editCelebrityFrame, text="Influcence:")
    influenceLabel.place(x=650, y=350)
    influenceField = CTkEntry(editCelebrityFrame, width=200, placeholder_text="Enter Influence")
    influenceField.place(x=750, y=350)

    # Politics
    politicalLabel = CTkLabel(editCelebrityFrame, text="Political Orientation:")
    politicalLabel.place(x=650, y=390)
    politicalField = CTkEntry(editCelebrityFrame, width=200, placeholder_text="Enter Political Orientation")
    politicalField.place(x=750, y=390)

    # Achievements
    achievementsLabel = CTkLabel(editCelebrityFrame, text="Achievements:")
    achievementsLabel.place(x=650, y=430)
    achievementsField = CTkTextbox(editCelebrityFrame, width=500)
    achievementsField.place(x=750, y=430)

    # Submit button to add celebrity
    submitButton = CTkButton(editCelebrityFrame, text="Add Celebrity", command=editCelebrity, width=100, font=("Arial", 16))
    submitButton.place(relx=0.5, rely=0.9, anchor="center")

    # Go back to main menu
    backButton = CTkButton(editCelebrityFrame, text="Home", command=showMainFrame, width=60)
    backButton.place(relx=0.05, rely=0.05, anchor="center")

def createCelebrityFrame(celebrity):
    global celebrityFrame
    celebrityFrame = CTkFrame(app, width=1280, height=720)
    celebrityFrame.pack(fill="both", expand=True)
    
    # Display full details. For each key in the celebrity dictionary, create a label:
    row = 0
    for key, value in celebrity.items():
        label = CTkLabel(celebrityFrame, text=f"{key}: {value}", font=("Arial", 14))
        label.grid(row=row, column=0, sticky="w", padx=20, pady=5)
        row += 1
    
    # Add a "Back" button to return to the main view
    backButton = CTkButton(celebrityFrame, text="Back", command=showMainFrame)
    backButton.grid(row=row, column=0, pady=20)

createMainFrame()

showMainFrame()
app.mainloop()