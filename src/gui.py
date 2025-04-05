from customtkinter import *
from CTkMessagebox import CTkMessagebox
from PIL import Image, ImageOps
import accounts
import functions
import pytest

app = CTk()
app.title("TERNOPS - Celebrity Bio Application")
app.iconbitmap("src\\Data\\Images\\system\\ternops.ico")
app.geometry("1280x720")
app.resizable(False, False)
app._set_appearance_mode("dark")
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
filterFrame = None

# Hide all frames
def hideAllFrames():
    if mainFrame:
        mainFrame.pack_forget()
    if signInFrame:
        signInFrame.place_forget()
    if editCelebrityFrame:
        editCelebrityFrame.pack_forget()
    if celebrityFrame:
        celebrityFrame.pack_forget()
    if filterFrame:
        filterFrame.pack_forget()

# Show the main frame
def showMainFrame(filteredCelebrities=None):
    hideAllFrames()
    createMainFrame(filteredCelebrities)
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
def showCelebrityFrame(celebrity=None):
    hideAllFrames()
    createCelebrityFrame(celebrity)

# Show the filter frame
def showFilterFrame():
    hideAllFrames()
    createFilterFrame()

#------------------------------------------FUNCTIONS TO BE MOVED------------------------------------------------
def removeCelebrity(firstName, lastName):
        deleteCeleb = CTkMessagebox(message=f"Are you sure you would like to delete {firstName} {lastName}? This action is permenant.", icon="warning", option_1="Yes", option_2="No")
        if deleteCeleb.get() == "Yes":
            functions.delete_data("src\\Data\\celebrities.csv", firstName, lastName)
            showMainFrame()
        else:
            pass

def createCelebrityRow(celebrities, scrollFrame):
    global userAccount
    # Clear the previous celebrity list
    for widget in scrollFrame.winfo_children():
        widget.destroy()

    # Create a row for each celebrity in the CSV file
    for celebrity in celebrities:
        firstName = celebrity["first_name"]
        lastName = celebrity["last_name"]
        dateOfBirth = celebrity["date_of_birth"]
        dateOfDeath = celebrity["date_of_death"]
        industry = celebrity["industry"]
        biography = str(celebrity["biography"])
        image = celebrity["images_path"]

        # Create a a breif bio
        brief_bio = biography[:400] + "..."

        # Create the row using the celebrity data
        rowFrame = CTkFrame(scrollFrame, width=1280, height=150, fg_color=colorPalette["darkGray"])
        rowFrame.pack(fill="x", pady=5)

        try:
            celebrityImage = Image.open(image)
            celebrityImage = ImageOps.fit(celebrityImage, (150, 150), method=0, bleed=0.0, centering=(0.5, 0.5))
            celebrityImage = CTkImage(dark_image=celebrityImage, size=(150, 150))
            celebrityLabel = CTkLabel(rowFrame, image=celebrityImage, text="")
            celebrityLabel.pack(side="left", padx=10, pady=10)
        except Exception as e:
            celebrityImage = CTkImage(dark_image=Image.open("src/Data/Images/user/user_100.png"), size=(150, 150))
            celebrityLabel = CTkLabel(rowFrame, image=celebrityImage, text="")
            celebrityLabel.pack(side="left", padx=10, pady=10)


        # Name, DOB, Industry Labels
        labelFrame = CTkFrame(rowFrame, fg_color=colorPalette["darkGray"])
        labelFrame.pack(side="left", padx=10, pady=10)
        # Name
        nameLabel = CTkLabel(labelFrame, text=f"{firstName} {lastName}", font=("Helvetica", 30))
        nameLabel.grid(row=0, column=0, sticky="w")
        # DOB
        dobLabel = CTkLabel(labelFrame, text=f"{dateOfBirth} - {dateOfDeath}", font=("Helvetica", 18))
        dobLabel.grid(row=1, column=0, sticky="w")
        # Industry
        industryLabel = CTkLabel(labelFrame, text=f"{industry}", font=("Helvetica", 18))
        industryLabel.grid(row=2, column=0, sticky="w")

        # Buttons grouped
        buttonFrame = CTkFrame(rowFrame, fg_color=colorPalette["darkGray"])
        buttonFrame.pack(side="right", padx=5, pady=10)

        fullName = f"{firstName} {lastName}"
        if not isinstance(userAccount, accounts.Guest):
            if fullName not in userAccount.get_favourites():  # Check if the full name is in the favourites list
                # Favorite button
                favoriteButton = CTkButton(buttonFrame, text="FAVOURITE", font=('Helvetica', 14), width=80, height=26, fg_color=colorPalette["veryDarkGray"], hover_color=colorPalette["mediumGray"])
                favoriteButton.configure(command=lambda name=fullName, button_instance=favoriteButton, button_frame_instance=buttonFrame: addFavouriteButtonFunc(button_frame_instance, button_instance, "src\\Data\\accountInfo.csv", name))
                favoriteButton.grid(row=0, column=0, pady=5)
            
            else:  # If the full name is in the favourites list
                # REMOVE from Favourites button
                removeFavouriteButton = CTkButton(buttonFrame, text="UN-FAVOURITE", font=('Helvetica', 14), width=80, height=26, fg_color=colorPalette["veryDarkGray"], hover_color=colorPalette["mediumGray"])
                removeFavouriteButton.configure(command=lambda name=fullName, button_instance=removeFavouriteButton, button_frame_instance=buttonFrame: removeFavouriteButtonFunc(button_frame_instance, button_instance, "src\\Data\\accountInfo.csv", name))
                removeFavouriteButton.grid(row=0, column=0, pady=5)

        # Learn more button
        LearnMoreButton = CTkButton(buttonFrame, text="LEARN MORE", font=('Helvetica', 14), command=lambda celeb=celebrity: showCelebrityFrame(celeb), width=80, height=26, fg_color=colorPalette["veryDarkGray"], hover_color=colorPalette["mediumGray"])
        LearnMoreButton.grid(row=1, column=0, pady=5)

        if userAccount.get_is_admin():
            # Edit button
            editButton = CTkButton(buttonFrame, text="EDIT", font=('Helvetica', 14), command=lambda celeb=celebrity: createEditCelebrityFrame("Edit", celeb["first_name"], celeb["last_name"]), width=80, height=26, fg_color=colorPalette["veryDarkGray"], hover_color=colorPalette["mediumGray"])
            editButton.grid(row=2, column=0, pady=5)
            # Remove button
            removeButton = CTkButton(buttonFrame, text="DELETE", font=("Helvetica", 14), command=lambda firstName=celebrity["first_name"], lastName=celebrity["last_name"]: removeCelebrity(firstName, lastName), width=80, height=26, fg_color=colorPalette["veryDarkGray"], hover_color=colorPalette["mediumGray"])
            removeButton.grid(row=3, column=0, pady=5)

        # Bio
        bioLabel = CTkLabel(rowFrame, text=brief_bio, font=("Helvetica", 16), wraplength=650, justify="left")
        bioLabel.pack(side="right", padx=30, pady=10)
#------------------------------------------FUNCTIONS TO BE MOVED------------------------------------------------

# Create the main frame
def createMainFrame(filteredCelebrities=None):
    def logoutAndShowMain():
        global userAccount
        userAccount = accounts.Guest()
        showMainFrame()
    
    def searchCelebrities(userInput, celebrities, scrollFrame):
        if userInput != "":
            # Store searched celebrities
            filteredCelebrities = []
            # Iterate through all celebrities
            for celeb in celebrities:
                # Converts names to lowercase
                first_name = celeb["first_name"].lower()
                last_name = celeb["last_name"].lower()
                if userInput in first_name or userInput in last_name:
                    filteredCelebrities.append(celeb)
            createCelebrityRow(filteredCelebrities, scrollFrame)
        else:
            createCelebrityRow(celebrities, scrollFrame)

    def showFavourites(favourites, celebrities, scrollFrame):
        # Clear any existing content in the scrollFrame
        for widget in scrollFrame.winfo_children():
            widget.destroy()

        # Filter celebrities by favourites (match full name)
        favouriteCelebrities = []
        for celeb in celebrities:
            full_name = f"{celeb['first_name']} {celeb['last_name']}"
            if full_name in favourites:
                favouriteCelebrities.append(celeb)
        
        # Create a row for each favourite celebrity
        createCelebrityRow(favouriteCelebrities, scrollFrame)

    global mainFrame, userAccount, scrollFrame

    # Frame to house all elements
    mainFrame = CTkFrame(app, width=1280, height=720)
    mainFrame.pack(fill="both", expand=True)

    topFrame = CTkFrame(mainFrame, width=1280, height=70, fg_color=colorPalette["veryDarkGray"], corner_radius=0)
    topFrame.pack(fill="x", side="top")

    if not isinstance(userAccount,accounts.Guest):
        profilePicture = CTkImage(dark_image=Image.open("src\\Data\\Images\\user\\admin_100.png"), size=(30,30))
    else:
        profilePicture = CTkImage(dark_image=Image.open("src\\Data\\Images\\user\\user.png"), size=(30,30))
    profilePictureLabel = CTkLabel(topFrame, image=profilePicture, text="")
    profilePictureLabel.place(x=20, y=20)
    #User info
    userLabel = CTkLabel(topFrame, text=userAccount.get_user_name(), font=("Helvetica", 28))
    userLabel.place(x=70, y=20)
    # If the username is too long replce with ...
    if len(userLabel.cget("text")) > 20:
        userLabel.configure(text=userLabel.cget("text")[:20] + "...")

    if userAccount.get_user_name() == "Guest":
        # Login / Register buttons
        loginButton = CTkButton(topFrame, text="Login", font=("Helvetica", 14), command=lambda: showSignInFrame("Login to Account"), width=60, height=36, fg_color=colorPalette["mediumGray"], hover_color=colorPalette["lightGray"])
        loginButton.place(x=1280 - 60 - 20, y=16)  
        registerButton = CTkButton(topFrame, text="Register", font=("Helvetica", 14), command=lambda: showSignInFrame("Register Account"), width=60, height=36, fg_color=colorPalette["mediumGray"], hover_color=colorPalette["lightGray"])
        registerButton.place(x=1280 - 60 - 20 - 60 - 20, y=16)
    else:
        # Logout button
        logoutButton = CTkButton(topFrame, text="Logout", font=("Helvetica", 14), command=logoutAndShowMain, width=60, height=36, fg_color=colorPalette["mediumGray"], hover_color=colorPalette["lightGray"])
        logoutButton.place(x=1280 - 60 - 20, y=20)

    # Searchbar
    searchbar = CTkEntry(topFrame, width=500, placeholder_text="Search for a celebrity", border_width=4, corner_radius=18, font=("Helvetica", 14), height=46, fg_color=colorPalette["darkGray"])
    searchbar.place(relx=0.5, rely=0.5, anchor="center")
    searchbar.bind("<Return>", lambda event: searchCelebrities(searchbar.get().lower(), celebrities, scrollFrame))
    # Magnifying glass icon
    magnifyIcon = CTkImage(dark_image=Image.open("src\\Data\\Images\\system\\magnify.png"), size=(30, 30))
    # Create a label with the magnify icon and place it inside the search bar
    magnifyLabel = CTkLabel(topFrame, image=magnifyIcon, text="", cursor="hand2")
    magnifyLabel.place(relx=0.715, rely=0.5, anchor="center") 
    magnifyLabel.bind("<Button-1>", lambda event: searchCelebrities(searchbar.get().lower(), celebrities, scrollFrame))

    #TODO Filter
    # Filter icon glass icon
    filterIcon = CTkImage(dark_image=Image.open("src\\Data\\Images\\system\\filter.png"), size=(30, 30))
    # Create a label with the magnify icon and place it inside the search bar
    filterLabel = CTkLabel(topFrame, image=filterIcon, text="", cursor="hand2")
    filterLabel.place(relx=0.8, rely=0.5, anchor="center") 
    filterLabel.bind("<Button-1>", lambda event: showFilterFrame()) 
    
    # Favourites icon glass icon
    FavouritesIcon = CTkImage(dark_image=Image.open("src\\Data\\Images\\system\\favourites.png"), size=(30, 30))
    # Create a label with the magnify icon and place it inside the search bar
    if not isinstance(userAccount,accounts.Guest):
        FavouritesLabel = CTkLabel(topFrame, image=FavouritesIcon, text="", cursor="hand2")
        FavouritesLabel.place(relx=0.845, rely=0.5, anchor="center") 
        FavouritesLabel.bind("<Button-1>", lambda event: showFavourites(userAccount.get_favourites(), celebrities, scrollFrame)) 
    
    # Add Celebrity
    if userAccount.get_is_admin():
        addButton = CTkButton(topFrame, text="+", font=("Helvetica",24), command=lambda: createEditCelebrityFrame("Add"), width=36, height=36, fg_color=colorPalette["darkGray"], hover_color=colorPalette["lightGray"])
        addButton.place(relx=0.75, rely=0.5, anchor="center")

    # Scrollable frame to house list of celebrities
    scrollFrame = CTkScrollableFrame(mainFrame, width=1280, height=660)
    scrollFrame.pack(fill="both")

    # Load all celebrities if no filter applied
    if filteredCelebrities is None:
        celebrities = functions.load_celebrities_file("src/Data/celebrities.csv")
    else:
        celebrities = filteredCelebrities


    # Create a row for each celebrity in the CSV file
    createCelebrityRow(celebrities, scrollFrame)

# removes favourite celebrity and then destroys the instance of the button as well as creating a new instance of the opposite button
def removeFavouriteButtonFunc(buttonFrame, buttonInstance, file_path, celeb_name):
    userAccount.remove_favourite(file_path, celeb_name)
    buttonInstance.destroy()
    # create a new instance of REMOVE from Favourites button
    addFavouriteButton = CTkButton(buttonFrame, text="FAVOURITE", font=('Helvetica', 14), width=80, height=26, fg_color=colorPalette["veryDarkGray"], hover_color=colorPalette["mediumGray"])
    addFavouriteButton.configure(command=lambda name=celeb_name, button_instance=addFavouriteButton: addFavouriteButtonFunc(buttonFrame, button_instance, "src\\Data\\accountInfo.csv", name))
    addFavouriteButton.grid(row=0, column=0, pady=5)

# adds favourite celebrity and then destroys the instance of the button as well as creating a new instance of the opposite button
def addFavouriteButtonFunc(buttonFrame, buttonInstance, file_path, celeb_name):
    userAccount.add_favourite(file_path, celeb_name)
    buttonInstance.destroy()
    # create a new instance of REMOVE from Favourites button
    removeFavouriteButton = CTkButton(buttonFrame, text="UN-FAVOURITE", font=('Helvetica', 14), width=80, height=26, fg_color=colorPalette["veryDarkGray"], hover_color=colorPalette["mediumGray"])
    removeFavouriteButton.configure(command=lambda name=celeb_name, button_instance=removeFavouriteButton: removeFavouriteButtonFunc(buttonFrame, button_instance, "src\\Data\\accountInfo.csv", name))
    removeFavouriteButton.grid(row=0, column=0, pady=5)
    
# Create the sign in frame
def createSignInFrame(signInType):
    def printToLabel():
        global userAccount
        username = str(usernameField.get())
        password = str(passwordField.get())
        # Only get admin code if registering
        adminCode = str(adminCodeField.get()) if signInType == "Register Account" else None

        if signInType == "Login to Account":    
            successfulRegister, newUserAccount, successText = accounts.login(username, password, "src\\Data\\accountInfo.csv")

        elif signInType == "Register Account":
            # If the adminCode is empty, register user without admin privileges
            if adminCode == "":
                successfulRegister, newUserAccount, successText = accounts.register_user(username, password, False, "src\\Data\\accountInfo.csv")
            elif adminCode == "admin123":  # If admin code is correct
                successfulRegister, newUserAccount, successText = accounts.register_user(username, password, True, "src\\Data\\accountInfo.csv")
            else:  # If admin code is incorrect
                successfulRegister = False
                newUserAccount = None
                successText = "Incorrect admin code."
        else:
            print("Invalid sign in type")
            
        if successfulRegister:
            userAccount = newUserAccount
            # Check if the admin code is correct
            if adminCode == "admin123": #set for demo purposes
                userAccount.set_is_admin(True)  # Grant admin rights
                successText += "\nAdmin permisions enabled!!"
            else:
                pass

            successLabel = CTkLabel(signInFrame, text=f"Successfuly {successText}\n Redirecting Home", font=("Helvetica", 18), width=640, text_color="green")
            successLabel.place(relx=0.5, rely=0.3, anchor="center")
            app.after(2000, showMainFrame)
        else:
            successLabel = CTkLabel(signInFrame, text=successText, font=("Helvetica", 18), width=640, text_color="red")
            successLabel.place(relx=0.5, rely=0.3, anchor="center")
    
    global signInFrame
    signInFrame = CTkFrame(app, width=1280, height=720)
    signInFrame.place(relx=0.5, rely=0.5, anchor="center")  

    loginLabel = CTkLabel(signInFrame, text=signInType, font=("Helvetica", 22))
    loginLabel.place(relx=0.5, rely=0.2, anchor="center")

    #Username
    usernameField = CTkEntry(signInFrame, width=500, placeholder_text="Enter your username...", height=60, font=("Helvetica", 20))
    usernameField.place(relx=0.5, rely=0.5, anchor="center")
    #Password
    passwordField = CTkEntry(signInFrame, width=500, placeholder_text="Enter your password...", show="*", height=60, font=("Helvetica", 20))
    passwordField.place(relx=0.5, rely=0.6, anchor="center")
    passwordField.bind("<Return>", lambda event: printToLabel())
    #Admin Code
    if signInType == "Register Account":
        adminCodeField = CTkEntry(signInFrame, width=500, placeholder_text="Enter admin password...", show="*", height=60, font=("Helvetica", 20))
        adminCodeField.place(relx=0.5, rely=0.7, anchor="center")
    #Submit
    submitButton = CTkButton(signInFrame, text=signInType, command=printToLabel, width=80, font=("Helvetica", 16), fg_color=colorPalette["darkGray"], hover_color=colorPalette["lightGray"])
    submitButton.place(relx=0.5, rely=0.8, anchor="center")

    #go back to main menu
    backButton = CTkButton(signInFrame, text="HOME", command=showMainFrame, width=60, font=("Helvetica", 16), fg_color=colorPalette["darkGray"], hover_color=colorPalette["lightGray"])
    backButton.place(relx=0.05, rely=0.05, anchor="center")

# Create the edit celebrity frame
def createEditCelebrityFrame(editType, originalFirstName=None, originalLastName=None):
    global localImagePath
    localImagePath = None

    def getImagePath():
        global localImagePath
        filePath = filedialog.askopenfilename(title="Select an Image",filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;")])
        # Only store the path, don't copy yet
        localImagePath = filePath  
        filePathLabel = CTkLabel(editCelebrityFrame, text=f"Image: {filePath[:35]}", font=("Helvetica", 14))
        filePathLabel.place(x=260, y=390)  

    def editCelebrity():
        firstName = firstNameField.get()
        lastName = lastNameField.get()
        dateOfBirth = dateOfBirthField.get()
        dateOfDeath = dateOfDeathField.get()
        industry = industryField.get()
        associations = associationsField.get() 
        gender = genderDropdown.get() 
        biography = biographyTextbox.get("1.0", "end-1c") 
        netWorth = netWorthField.get() 
        family = familyField.get() 
        controversies = controversiesField.get() 
        discography = discographyField.get() 
        filmography = filmographyField.get() 
        genres = genresField.get() 
        influence = influenceField.get() 
        political = politicalField.get() 
        achievements = achievementsTextbox.get("1.0", "end-1c") 
        
        imagePath = None
        # now we copy
        if localImagePath: 
            celebrityName = f"{firstName}_{lastName}"
            imagePath = functions.copy_image_to_folder(localImagePath, celebrityName)

        #Initialize errorMessage
        errorMessage = None
        
        if editType == "Add":
            # Check if the required fields are filled
            if not firstNameField.get().strip() or not lastNameField.get().strip() or not industryField.get().strip():
                errorMessage  = CTkLabel(editCelebrityFrame, text="Please make sure First Name, Last Name, and Industry are filled", font=("Helvetica", 16), text_color="red")
                errorMessage.place(relx=0.5, rely=0.75, anchor="center")
                app.after(2000, lambda: errorMessage.destroy())
                return
        
            # Add the celebrity to the CSV
            celebrityData = {
                "first_name": firstName,
                "last_name": lastName,
                "date_of_birth": dateOfBirth,
                "images_path": imagePath,
                "date_of_death" : dateOfDeath,
                "biography" : biography,
                "achievements" : achievements,
                "industry" : industry,
                "family" : family,
                "associations" : associations,
                "controversies" : controversies,
                "discography" : discography,
                "filmography" : filmography,
                "genres" : genres,
                "influence" : influence,
                "political_orientation" : political,
                "gender" : gender,
                "net_worth" : netWorth
            }

            # Add the celebrity to the CSV
            functions.add_data("src/Data/celebrities.csv", celebrityData)

            # Show success message
            successMessage = CTkLabel(editCelebrityFrame, text=f"Successfully added {firstName} {lastName}!", font=("Helvetica", 16), text_color="green")
            successMessage.place(relx=0.5, rely=0.75, anchor="center")
            app.after(2000, showMainFrame)

        elif editType == "Edit":
            celebrities = functions.load_celebrities_file("src/Data/celebrities.csv")
            # Locate the record using the original first and last names
            # Locate the matching celebrity using next()
            celeb = next((c for c in celebrities if c.get("first_name") == originalFirstName and c.get("last_name") == originalLastName), None)

            if not celeb:
                errorLabel = CTkLabel(editCelebrityFrame, text="Celebrity not found.", font=("Helvetica", 16), text_color="red")
                errorLabel.place(relx=0.5, rely=0.75, anchor="center")
                return

            # Update the record with new or existing values
            if firstName != originalFirstName:  # Update first name
                functions.edit_data("src/Data/celebrities.csv", "first_name", originalFirstName, "first_name", firstName)
            if lastName != originalLastName:  # Update last name
                functions.edit_data("src/Data/celebrities.csv", "last_name", originalLastName, "last_name", lastName)
            if dateOfBirth:  # Update date of birth
                functions.edit_data("src/Data/celebrities.csv", "first_name", originalFirstName, "date_of_birth", dateOfBirth)
            if dateOfDeath:  # Update date of death
                functions.edit_data("src/Data/celebrities.csv", "first_name", originalFirstName, "date_of_death", dateOfDeath)
            if biography:  # Update biography
                functions.edit_data("src/Data/celebrities.csv", "first_name", originalFirstName, "biography", biography)
            if achievements:  # Update achievements
                functions.edit_data("src/Data/celebrities.csv", "first_name", originalFirstName, "achievements", achievements)
            if industry:  # Update industry
                functions.edit_data("src/Data/celebrities.csv", "first_name", originalFirstName, "industry", industry)
            if family:  # Update family
                functions.edit_data("src/Data/celebrities.csv", "first_name", originalFirstName, "family", family)
            if associations:  # Update associations
                functions.edit_data("src/Data/celebrities.csv", "first_name", originalFirstName, "associations", associations)
            if controversies:  # Update controversies
                functions.edit_data("src/Data/celebrities.csv", "first_name", originalFirstName, "controversies", controversies)
            if discography:  # Update discography
                functions.edit_data("src/Data/celebrities.csv", "first_name", originalFirstName, "discography", discography)
            if filmography:  # Update filmography
                functions.edit_data("src/Data/celebrities.csv", "first_name", originalFirstName, "filmography", filmography)
            if genres:  # Update genres
                functions.edit_data("src/Data/celebrities.csv", "first_name", originalFirstName, "genres", genres)
            if influence:  # Update influence
                functions.edit_data("src/Data/celebrities.csv", "first_name", originalFirstName, "influence", influence)
            if political:  # Update political orientation
                functions.edit_data("src/Data/celebrities.csv", "first_name", originalFirstName, "political_orientation", political)
            if gender:  # Update gender
                functions.edit_data("src/Data/celebrities.csv", "first_name", originalFirstName, "gender", gender)
            if netWorth:  # Update net worth
                functions.edit_data("src/Data/celebrities.csv", "first_name", originalFirstName, "net_worth", netWorth)
            if imagePath:
                functions.edit_data("src/Data/celebrities.csv", "first_name", originalFirstName, "images_path", imagePath)
            
            successLabel = CTkLabel(editCelebrityFrame, text=f"Successfully edited {firstName} {lastName}!", font=("Helvetica", 16), text_color="green")
            successLabel.place(relx=0.5, rely=0.75, anchor="center")
            app.after(2000, showMainFrame)

        else:
            print("Invalid edit type")

    def createLabelAndField(label_text, x, y, fieldType="entry", options=None):
        label = CTkLabel(editCelebrityFrame, text=label_text)
        label.place(x=x, y=y)
        if fieldType == "entry":
            field = CTkEntry(editCelebrityFrame, width=150, placeholder_text=f"Enter {label_text}")
        elif fieldType == "combo":
            field = CTkComboBox(master=app, values=options, width=150)
        elif fieldType == "text":
            field = CTkTextbox(editCelebrityFrame, width=450)
        field.place(x=x + 120, y=y)
        return field
    
    global editCelebrityFrame
    
    editCelebrityFrame = CTkFrame(app, width=1280, height=720)
    editCelebrityFrame.place(relx=0.5, rely=0.5, anchor="center")
    
    # Add a label to inform the user of the action
    editLabel = CTkLabel(editCelebrityFrame, text=f"Please fill in the details to {editType} a celebrity", font=("Helvetica", 22))
    editLabel.place(relx=0.5, rely=0.1, anchor="center")

    # Left Side Fields
    firstNameField = createLabelAndField("First Name:", 20, 110)
    lastNameField = createLabelAndField("Last Name:", 20, 150)
    dateOfBirthField = createLabelAndField("Date of Birth:", 20, 190)
    dateOfDeathField = createLabelAndField("Date of Death:", 20, 230)
    industryField = createLabelAndField("Industry:", 20, 270)
    associationsField = createLabelAndField("Associations:", 20, 310)
    genderDropdown = createLabelAndField("Gender:", 20, 350, fieldType="combo", options=["Male", "Female", "Other"])
    #image
    imageLabel = CTkLabel(editCelebrityFrame, text="Image: ", font=("Helvetica", 14))
    imageLabel.place(x=20, y=390)
    imageButton = CTkButton(editCelebrityFrame, text="Select Image", command=getImagePath, width=100, font=("Helvetica", 14), fg_color=colorPalette["darkGray"], hover_color=colorPalette["lightGray"])
    imageButton.place(x=140, y=390)
    biographyTextbox = createLabelAndField("Biography:", 20, 430, fieldType="text")

    # Right Side Fields
    netWorthField = createLabelAndField("Net Worth:", 620, 110)
    familyField = createLabelAndField("Family:", 620, 150)
    controversiesField = createLabelAndField("Controversies:", 620, 190)
    discographyField = createLabelAndField("Discography:", 620, 230)
    filmographyField = createLabelAndField("Filmography:", 620, 270)
    genresField = createLabelAndField("Genres:", 620, 310)
    influenceField = createLabelAndField("Influence:", 620, 350)
    politicalField = createLabelAndField("Political Orientation:", 620, 390)
    achievementsTextbox = createLabelAndField("Achievements:", 620, 430, fieldType="text")

    # Pre-populate fields if editing
    if editType == "Edit" and (originalFirstName != None) and (originalLastName != None):
        celebrities = functions.load_celebrities_file("src/Data/celebrities.csv")
        celeb = next((c for c in celebrities if c["first_name"] == originalFirstName and c["last_name"] == originalLastName), None)
        if celeb:
            firstNameField.insert(0, celeb.get("first_name", ""))
            lastNameField.insert(0, celeb.get("last_name", ""))
            dateOfBirthField.insert(0, celeb.get("date_of_birth", ""))
            dateOfDeathField.insert(0, celeb.get("date_of_death", ""))
            industryField.insert(0, celeb.get("industry", ""))
            associationsField.insert(0, celeb.get("associations", ""))
            genderDropdown.set(celeb.get("gender", ""))  
            biographyTextbox.insert("1.0", celeb.get("biography", ""))
            netWorthField.insert(0, celeb.get("net_worth", ""))
            familyField.insert(0, celeb.get("family", ""))
            controversiesField.insert(0, celeb.get("controversies", ""))
            discographyField.insert(0, celeb.get("discography", ""))
            filmographyField.insert(0, celeb.get("filmography", ""))
            genresField.insert(0, celeb.get("genres", ""))
            influenceField.insert(0, celeb.get("influence", ""))
            politicalField.insert(0, celeb.get("political_orientation", ""))
            achievementsTextbox.insert("1.0", celeb.get("achievements", ""))

    # Submit button to add celebrity
    submitButton = CTkButton(editCelebrityFrame, text="Add Celebrity" if editType == "Add" else "Edit Celebrity", command=editCelebrity, width=100, font=("Helvetica", 16), fg_color=colorPalette["darkGray"], hover_color=colorPalette["lightGray"])
    submitButton.place(relx=0.5, rely=0.9, anchor="center")

    # Go back to main menu
    backButton = CTkButton(editCelebrityFrame, text="HOME", command=showMainFrame, width=60, font=("Helvetica", 16), fg_color=colorPalette["darkGray"], hover_color=colorPalette["lightGray"])
    backButton.place(relx=0.05, rely=0.05, anchor="center")

def createCelebrityFrame(celebrity=None):
    global celebrityFrame
    celebrityFrame = CTkFrame(app, width=1280, height=720)
    celebrityFrame.pack(fill="both", expand=True)

    # Top frame for the back button and celebrity Name
    headerFrame = CTkFrame(celebrityFrame, width=1280, height=100, fg_color=colorPalette["darkGray"])
    headerFrame.pack(fill="x", side="top")

    # Add a Back button to return to the main view
    backButton = CTkButton(headerFrame, text="BACK", font=("Helvetica", 16), command=showMainFrame, fg_color=colorPalette["veryDarkGray"], hover_color=colorPalette["lightGray"])
    backButton.place(relx=0.05, rely=0.5, anchor="w")

    # Display celebrity's full name
    celebrityLabel = CTkLabel(headerFrame, text=f"{celebrity['first_name']} {celebrity['last_name']}", font=("Helvetica", 30))
    celebrityLabel.place(relx=0.5, rely=0.5, anchor="center")

    # scrollable frame for celebrity details
    scrollFrame = CTkScrollableFrame(celebrityFrame, width=1280, height=620, fg_color=colorPalette["mediumGray"])
    scrollFrame.pack(fill="both", expand=True)

    # Wrapper to hold image + columns
    topContentFrame = CTkFrame(scrollFrame, fg_color=colorPalette["mediumGray"])
    topContentFrame.pack(fill="x", padx=20, pady=20)

    # Image
    try:
        celebrityImage = Image.open(celebrity["images_path"])
        celebrityImage = ImageOps.fit(celebrityImage, (300, 300), centering=(0.5, 0.5))
        celebrityImage = CTkImage(dark_image=celebrityImage, size=(300, 300))
    except Exception:
        celebrityImage = CTkImage(dark_image=Image.open("src/Data/Images/user/user_100.png"), size=(300, 300))

    CTkLabel(topContentFrame, image=celebrityImage, text="").pack(side="left", padx=10, pady=10)

    # Columns container
    columnsFrame = CTkFrame(topContentFrame, fg_color=colorPalette["mediumGray"])
    columnsFrame.pack(side="left", fill="both", expand=True, padx=20)

    leftColumn = CTkFrame(columnsFrame, fg_color=colorPalette["mediumGray"])
    leftColumn.pack(side="left", anchor="n", padx=10, pady=10)

    rightColumn = CTkFrame(columnsFrame, fg_color=colorPalette["mediumGray"])
    rightColumn.pack(side="left", anchor="n", padx=10, pady=10)

    # Left Column Info
    info = [
        ("Achievements", 'achievements'),
        ("Net Worth", 'net_worth'),
        ("Industry", 'industry'),
        ("Family", 'family'),
        ("Associations", 'associations'),
        ("Controversies", 'controversies'),
    ]
    for label_text, key in info:
        CTkLabel(leftColumn, text=f"{label_text}:", font=("Helvetica", 18)).pack(anchor="w", pady=(10, 0))
        CTkLabel(leftColumn, text=celebrity.get(key, ""), font=("Helvetica", 14), wraplength=400, justify="left").pack(anchor="w")

    # Right Column Media Info
    media_info = [
        ("Filmography", 'filmography'),
        ("Discography", 'discography'),
        ("Genres", 'genres'),
        ("Influence", 'influence'),
        ("Political Orientation", 'political_orientation'),
        ("Gender", 'gender'),
    ]
    for label_text, key in media_info:
        CTkLabel(rightColumn, text=f"{label_text}:", font=("Helvetica", 18)).pack(anchor="w", pady=(10, 0))
        CTkLabel(rightColumn, text=celebrity.get(key, ""), font=("Helvetica", 14), wraplength=400, justify="left").pack(anchor="w")

    # Biography (bottom full-width)
    CTkLabel(scrollFrame, text="Biography:", font=("Helvetica", 22)).pack(anchor="w", pady=(20, 0), padx=20)
    CTkLabel(scrollFrame, text=celebrity.get("biography", ""), font=("Helvetica", 18), wraplength=1200, justify="left").pack(anchor="w", padx=20, pady=(0, 20))
    
def createFilterFrame():
    # Create a dictionary of fields with StringVar for each filter.
    fields = {
        "first_name": StringVar(),
        "last_name": StringVar(),
        "date_of_birth": StringVar(),
        "date_of_death": StringVar(),
        "biography": StringVar(),
        "achievements": StringVar(),
        "industry": StringVar(),
        "family": StringVar(),
        "associations": StringVar(),
        "controversies": StringVar(),
        "discography": StringVar(),
        "filmography": StringVar(),
        "genres": StringVar(),
        "influence": StringVar(),
        "political_orientation": StringVar(),
        "gender": StringVar(),
        "net_worth": StringVar()
    }

    checkbox_vars = {field: StringVar(value="off") for field in fields}
    entry_vars = {field: StringVar() for field in fields}

    # check which filters are enabled and add celebs
    def filterCelebrities():
        import pandas as pd
        # Load the CSV file as a DataFrame.
        df = pd.read_csv("src/Data/celebrities.csv")
        
        # For each field that is enabled (checkbox on):
        for field in fields:
            if checkbox_vars[field].get() == "on":
                search_text = entry_vars[field].get().strip()
                if search_text:
                    if field == "gender":
                        df = df[df[field].str.lower() == search_text.lower()]  # Exact match for gender
                    else:
                        # For other fields, retain substring match (case insensitive)
                        df = df[df[field].fillna("").str.contains(search_text, case=False)]
                else:
                    # If the entry is empty, only keep rows where this field is not empty
                    df = df[df[field].fillna("").str.strip() != ""]
        
        # Convert the resulting DataFrame back to a list of dictionaries
        # so that createCelebrityRow can process it.
        filtered_celebrities = df.to_dict("records")
        print(f"Filtered Celebrities: {len(filtered_celebrities)} found")
        return filtered_celebrities
    
    def checkbox_event(var, label):
        print(f"Checkbox for {label} toggled, current value:", var.get())

    global filterFrame
    filterFrame = CTkFrame(app, width=1280, height=720)
    filterFrame.pack(fill="both", expand=True)
    
    # select filter options label
    filterLabel = CTkLabel(filterFrame, text="Select Filter Options:", font=("Helvetica", 20))
    filterLabel.place(relx=0.5, rely=0.05, anchor="center")

    # Split fields into two columns
    leftFields = [
        "first_name", "last_name", "date_of_birth", "date_of_death", "achievements",
        "industry", "family", "associations"
    ]
    rightFields = [
        "controversies", "discography", "filmography", "genres", "influence", 
        "political_orientation", "gender", "net_worth", "biography"
    ]

    # LEFT SIDE: for each field, create a checkbox and an entry next to it.
    for idx, field in enumerate(leftFields):
        checkbox = CTkCheckBox(
            filterFrame, 
            text=field.replace("_", " ").title(), 
            variable=checkbox_vars[field], 
            onvalue="on", 
            offvalue="off", 
            command=lambda var=checkbox_vars[field], label=field: checkbox_event(var, label)
        )
        checkbox.place(x=200, y=90 + idx * 40, anchor="w")

        entry = CTkEntry(filterFrame, width=200, textvariable=entry_vars[field], placeholder_text="Search...")
        entry.place(x=400, y=90 + idx * 40, anchor="w")
    
    # RIGHT SIDE: for each field, create a checkbox and an entry next to it.
    for idx, field in enumerate(rightFields):
        checkbox = CTkCheckBox(
            filterFrame, 
            text=field.replace("_", " ").title(), 
            variable=checkbox_vars[field], 
            onvalue="on", 
            offvalue="off", 
            command=lambda var=checkbox_vars[field], label=field: checkbox_event(var, label)
        )
        checkbox.place(x=650, y=90 + idx * 40, anchor="w")

        entry = CTkEntry(filterFrame, width=200, textvariable=entry_vars[field], placeholder_text="Search...")
        entry.place(x=850, y=90 + idx * 40, anchor="w")
    
    # "Home" button to go back to the main view
    backButton = CTkButton(filterFrame, text="HOME", font=("Helvetica", 16), command=showMainFrame, fg_color=colorPalette["darkGray"], hover_color=colorPalette["lightGray"], width=60)
    backButton.place(relx=0.05, rely=0.05, anchor="center")
    
    # "Filter Search" button to apply the filters
    submitButton = CTkButton(filterFrame, text="Search With Filter Terms", command=lambda: showMainFrame(filterCelebrities()), width=100, font=("Helvetica", 18), fg_color=colorPalette["darkGray"], hover_color=colorPalette["lightGray"])
    submitButton.place(relx=0.5, rely=0.8, anchor="center")

createMainFrame()

showMainFrame()
app.mainloop()