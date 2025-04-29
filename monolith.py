import json
import os

def banner():
    print(r""" /$$$$$$$                  /$$                       /$$           /$$$$$$$                  /$$       /$$                """)
    print(r"""| $$__  $$                | $$                      | $$          | $$__  $$                | $$      | $$                """)
    print(r"""| $$  \ $$ /$$   /$$  /$$$$$$$  /$$$$$$   /$$$$$$  /$$$$$$        | $$  \ $$ /$$   /$$  /$$$$$$$  /$$$$$$$ /$$   /$$      """)
    print(r"""| $$$$$$$ | $$  | $$ /$$__  $$ /$$__  $$ /$$__  $$|_  $$_/        | $$$$$$$ | $$  | $$ /$$__  $$ /$$__  $$| $$  | $$      """)
    print(r"""| $$__  $$| $$  | $$| $$  | $$| $$  \ $$| $$$$$$$$  | $$          | $$__  $$| $$  | $$| $$  | $$| $$  | $$| $$  | $$      """)
    print(r"""| $$  \ $$| $$  | $$| $$  | $$| $$  | $$| $$_____/  | $$ /$$      | $$  \ $$| $$  | $$| $$  | $$| $$  | $$| $$  | $$      """)
    print(r"""| $$$$$$$/|  $$$$$$/|  $$$$$$$|  $$$$$$$|  $$$$$$$  |  $$$$/      | $$$$$$$/|  $$$$$$/|  $$$$$$$|  $$$$$$$|  $$$$$$$      """)
    print(r"""|_______/  \______/  \_______/ \____  $$ \_______/   \___/        |_______/  \______/  \_______/ \_______/ \____  $$      """)
    print(r"""                               /$$  \ $$                                                                   /$$  | $$      """)
    print(r"""                              |  $$$$$$/                                                                  |  $$$$$$/      """)
    print(r"""                               \______/                                                                    \______/       """)
    print("\nMake and maintain your budget using Budget Buddy!")
def startProgram():
    print("\nPlease enter a number to pick an option below:\n[1] New Budget\n[2] Load Budget\n[3] Delete Budget")
    choice = input("Please enter your choice: ")
    match choice:
        case "1":
            newBudget()
            return
        case "2":
            return
        case "3":
            deleteBudget()
            return
        case _:
            print("Invalid choice")

def newBudget():
    #Get information from user
    print("\nYou have chosen to create a new budget, please fill out the following information:")
    income = input("Current Income:")
    limit = input("Please enter your monthly spending limit: ")
    print("Please chose a set of starting categories for your purchase: ")
    print("[1 - Minimal] Rent, Utilities, Car, Groceries, Savings")
    print("[2 - Detailed] Rent, Utilities, Car, Groceries, Savings, Health, Entertainment")
    print("[3 - Maximal] Rent, Utilities, Car, Groceries, Savings, Health, Entertainment, Debt, Emergency Fund")
    category_type = input("Please enter your choice (1-3): ")

    #Create dictionaries for each choice
    minimal_categories = {
        "rent": 0,
        "utilities": 0,
        "car": 0,
        "groceries": 0,
        "savings": 0,
    }
    detailed_categories = {
        "rent": 0,
        "utilities": 0,
        "car": 0,
        "groceries": 0,
        "savings": 0,
        "health": 0,
        "entertainment": 0,
    }
    maximal_categories = {
        "rent": 0,
        "utilities": 0,
        "car": 0,
        "groceries": 0,
        "savings": 0,
        "health": 0,
        "entertainment": 0,
        "debt": 0,
        "emergency fund": 0,
    }

    #Set expenses to chosen category
    match category_type:
        case "1":
            expenses = minimal_categories
        case "2":
            expenses = detailed_categories
        case "3":
            expenses = maximal_categories
        case _:
            print("Invalid choice, using minimal categories")
            expenses = minimal_categories

    #Budget name
    budget_name = input("Please enter your budget's name: ")

    #Create a dictionary of the budget
    current_budget = {
        "income": income,
        "limit": limit,
        "budget_name": budget_name,
        "expenses": expenses
    }

    #Store as a file
    filename = f"{budget_name}.json"

    with open(filename, "w") as budget_file:
        json.dump(current_budget, budget_file, indent=4)

    print(f"'{budget_name}' has been saved to '{filename}'")



def loadBudget():
    #Grab all budgets
    budgets = [i for i in os.listdir() if i.endswith(".json")]

    #If no budgets, return
    if not budgets:
        print("No budget file found")
        return None

    #Print all the budget files found
    print("\nPlease choose a budget to load:")
    for i, file in enumerate(budgets):
        print (f"[{i+1}] {file}")

    #Prompt user for their choice of file
    while True:
        try:
            choice = input("Please enter your choice: ")
            #Make sure entered # is valid
            if 1 <= int(choice) <= len(budgets):
                selection = budgets[int(choice) - 1]
                break
            else:
                raise ValueError
        #If invalid number is entered, try again
        except ValueError:
            print("Invalid choice")

    print("You have chosen to load: ", selection)



def deleteBudget():
    print("Delete budget function is not implemented yet.")

def listBudgets():
    print("List budgets function is not implemented yet.")

#Main - Self explanatory
def main():
    banner()
    startProgram()
    loadBudget()

#Automatically run main
if __name__ == "__main__":
    main()

print("Test")


