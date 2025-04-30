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
    print("<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>\n")

def startProgram():
    while True:
        try:
            print(
                "Please enter a number to pick an option below:\n[1] New Budget\n[2] Load Budget\n[3] Delete Budget")
            choice = input("Please enter your choice: ")
            print("\n<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>\n")
            #We keep load separate from the startProgram - we load it after creation anyways
            match choice:
                case "1":
                    newBudget()
                    return
                case "2":
                    budgets_folder = "Budgets"
                    if os.path.exists(budgets_folder):
                        return
                    else:
                        raise FileNotFoundError
                case "3":
                    deleteBudget()
                    return
                case _:
                    raise ValueError
        except ValueError:
            print("Invalid choice")
        except FileNotFoundError:
            print("You don't have any budget to load, please create one first!\n")

def newBudget():
    #Get information from user
    print("You have chosen to create a new budget, please fill out the following information:")
    income = input("Current Income:")
    limit = input("Please enter your monthly spending limit: ")
    print("Please choose a set of starting categories for your purchase: ")
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

    #Create folder for budgets if one doesnt already exist, then store new budget in it
    budgets_folder = "Budgets"
    os.makedirs(budgets_folder, exist_ok=True)
    filename = os.path.join(budgets_folder, f"{budget_name}.json")

    #Open and write to file
    with open(filename, "w") as budget_file:
        json.dump(current_budget, budget_file, indent=4)

    print(f"'{budget_name}' has been saved to '{filename}'")
    print("<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>\n")

def loadBudget():
    #Grab all budgets
    budgets_folder = "Budgets"
    budgets = [i for i in os.listdir(budgets_folder) if i.endswith(".json")]

    #If no budgets, return
    if not budgets:
        print("No budget file found")
        return None

    #Print all the budget files found
    print("Please choose a budget to load:")
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
    print("<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>\n")
    return selection

def deleteBudget():
    #Grab all budgets
    budgets_folder = "Budgets"
    budgets = [i for i in os.listdir(budgets_folder) if i.endswith(".json")]

    #If no budgets, return
    if not budgets:
        print("No budget file found")
        return None

    #Print all the budget files found
    print("\nPlease choose a budget to delete:")
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

    #Confirm deletion to prevent accidents
    print("You have chosen to delete:",selection)
    delete_confirm = input("Do you want to delete this budget? (y/n): ")
    if delete_confirm == "y":
        os.remove(selection)
        print(f"'{selection}' has been deleted")
    else:
        print("Deletion cancelled")

#This is where we will actually do budget manipulation
def management(current_budget):
    while True:
        try:
            print(current_budget.removesuffix(".json"))
            print("Spending: ") #Insert spending / limit here
            print("\nPlease choose an option from the list below (1-5): ")
            print("[1] View Expenses")
            print("[2] Add Purchase")
            print("[3] Create Categories")
            print("[4] Settings")
            print("[5] Return to Main Menu") #Find a way to return back to loadbudget
            choice = input("Please enter your choice: ")
            match choice:
                case "1":
                    purchases()
                case "2":
                    add_purchase()
                case "3":
                    create_categories()
                case "4":
                    settings()
                case "5":
                    return
                case _:
                    print("Invalid choice")
                    raise ValueError
        #Handle invalid choice
        except ValueError:
            print("Invalid choice")

def purchases():
    print("Currently in development")

def add_purchase():
    print("currently in development")

def create_categories():
    print("currently in development")

def settings():
    print("currently in development")

#Main - Self explanatory
def main():
    while True:
        try:
            banner()
            #Create/Load/Delete
            startProgram()
            #Load current budget for use in management
            current_budget = loadBudget()
            #Bulk of budget manipulation done here
            management(current_budget)
        except:
            print("Something went wrong, please report this to the developer\n")

#Automatically run main
if __name__ == "__main__":
    main()



