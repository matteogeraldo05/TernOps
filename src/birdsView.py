import fileHandling

def cli():
    option = 0
    while option != -1:
        print("----------TernOps Bird App----------")
        print("|     0. Exit                      |")
        print("|     1. Add Bird                  |")
        print("|     2. Remove Bird               |")
        print("|     3. Show Birds                |")
        print("|     4. Bird Info                 |")
        print("------------------------------------")
        option = int(input("Please enter your choice: "))
        
        if option == 0:
            option = -1
        elif option == 1:
            print("Bird Added!")
        elif option == 2:
            print("Bird Removed!")
        elif option == 3:
            print("Showing Birds!")
        elif option == 4:
            print("Which Bird would you like to learn more about? ")

if __name__ == "__main__":
    cli()
