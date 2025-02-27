from customtkinter import *
import accounts
app = CTk()
app.title("Celebrity Bio Application")
app.geometry("1280x720")
app.resizable(False, False)

def registerAccount():
    pass

def loginToAccount():
    pass

#Login / Register buttons
loginButton = CTkButton(app, text="Login", command=loginToAccount, width=60) #keep the same width as the register button
loginButton.place(relx=0.96, rely=0.05, anchor="center")
registerButton = CTkButton(app, text="Register", command=registerAccount, width=15)
registerButton.place(relx=0.91, rely=0.05, anchor="center")

def addCelebrity():
    pass

def removeCelebrity():
    pass

def editCelebrity():
    pass

#Celebrity management buttons
addButton = CTkButton(app, text="Add", command=addCelebrity, width=60)
addButton.place(relx=0.4, rely=0.5, anchor="center")
removeButton = CTkButton(app, text="Remove", command=removeCelebrity, width=60)
removeButton.place(relx=0.5, rely=0.5, anchor="center")
editButton = CTkButton(app, text="Edit", command=editCelebrity, width=60)
editButton.place(relx=0.6, rely=0.5, anchor="center")

#Searchbar
searchbar = CTkEntry(app, width=500, placeholder_text="Search for a celebrity")
searchbar.place(relx=0.5, rely=0.05, anchor="center")

app.mainloop()