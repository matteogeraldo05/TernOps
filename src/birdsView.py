import pandas as pd
csv = pd.read_csv("src/bird_data.csv")

def addBird():
    print("bird added")

def removeBird():
    print("bird removed")

def getBirdInfo(csv):
    userChoice = input("Which bird would you like to know more about? ")
    birdInfo = csv.loc[csv["name"] == userChoice]
    if birdInfo.empty:
        print("Sorry, that bird is not in our database.")
    else:
        print()
        print(birdInfo.to_string(index=False))
        print()

def editBirdInfo(csv):
    userChoice = input("Which bird would you like to edit? ")
    birdInfo = csv.loc[csv["name"] == userChoice]
    if birdInfo.empty:
        print("Sorry, that bird is not in our database.")
    else:
        print()
        print("Bird Edited!")
        print()


def cli():
    while True:
        print("----------TernOps Bird App----------")
        print("|     0. Exit                      |")
        print("|     1. Add Bird                  |")
        print("|     2. Remove Bird               |")
        print("|     3. Show Birds                |")
        print("|     4. Bird Info                 |")
        print("|     5. Edit Bird                 |")
        print("------------------------------------")
        option = int(input("Please enter your choice: "))
        
        if option == 0:
            break
        #elif option == 1:
        #    addBird()
        elif option == 2:
            print("Bird Removed!")
        elif option == 3:
            print(csv.name.to_string(index=False))
            print()
        elif option == 4:
            getBirdInfo(csv)
        elif option == 5:
            editBirdInfo(csv)
            

if __name__ == "__main__":
    cli()
