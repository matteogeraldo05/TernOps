import csv
import pandas as pd





def readAllBirds(filename):
    df = pd.read_csv(filename)
    pd.set_option("display.max_columns", None) # display ALL columns
    if not df.empty: # make sure the db is not empty
        print("Showing all birds!")
        print(df)
    else:
        print("Database is empty!")






def addBird(filename):
    # genus: string
    # mass(g): int
    # name: string
    # location: string
    # size: int
    # endangered: bool

    genus = input("Genus: ")

    try:
        mass = int(input("Mass in grams: "))
    except ValueError:
        mass = 0
        print("Invalid mass.")

    name = input("Name: ")

    geologicalLocation = input("Geological Location: ")

    try:
        population = int(input("Population size: "))
    except ValueError:
        population = 0
        print("Invalid population.")

    endangered = input("Endangered? Y/N: ")
    while (endangered.upper() != "Y" and endangered.upper() != "N"): # make sure the endangered value is valid
        print("Please enter either Y or N.")
        endangered = input("Endangered? Y/N: ")

    new_row = [genus, mass, name, geologicalLocation, population, endangered]
    try:
        with open(filename, "a") as file:
            csv.writer(file).writerow(new_row)
    except:
        with Exception as e:
            print(f"An error occurred {e}")








def readBird(filename):
    # read the csv file into a dataframe
    df = pd.read_csv(filename)

    name = input("Enter a bird name to see more details: ")

    # Filter rows that contain the target name
    filtered_df = df[df["name"] == name]

    if filtered_df.empty:
        print(f"No bird named {name} found in the database!")
        return

    # Print the rows that contain the name
    print(filtered_df)






def removeBird(filename):
    df = pd.read_csv(filename)

    name = input("Enter a bird name to remove: ")

    if name in df['name'].values:
        df.drop(df[df["name"] == name].index, inplace=True)
        df.to_csv(filename, index=False)
        print(f"Bird '{name}' removed from {filename}.")
    else:
        print(f"No bird named {name} found in the database!")
