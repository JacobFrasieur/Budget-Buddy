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
            choice = input("Please enter your choice (1-3): ")
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
                    #ADD HANDLING - If no budgets remain, newBudget() must be ran to avoid loading no budgets message
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
    print("[1 - Minimal] Rent, Utilities, Car, Groceries, Savings, Misc.")
    print("[2 - Detailed] Rent, Utilities, Car, Groceries, Savings, Health, Entertainment, Misc.")
    print("[3 - Maximal] Rent, Utilities, Car, Groceries, Savings, Health, Entertainment, Debt, Emergency Fund, Misc.")
    category_type = input("Please enter your choice (1-3): ")

    #Create dictionaries for each choice
    minimal_categories = {
        "rent": {},
        "utilities": {},
        "car": {},
        "groceries": {},
        "savings": {},
        "misc": {},
    }
    detailed_categories = {
        "rent": {},
        "utilities": {},
        "car": {},
        "groceries": {},
        "savings": {},
        "health": {},
        "entertainment": {},
        "misc": {},
    }
    maximal_categories = {
        "rent": {},
        "utilities": {},
        "car": {},
        "groceries": {},
        "savings": {},
        "health": {},
        "entertainment": {},
        "debt": {},
        "emergency fund": {},
        "misc": {},
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

    #Return the budget dictionary
    with open(os.path.join(budgets_folder, selection), "r") as budget_file:
        current_budget = json.load(budget_file)
    return current_budget, selection

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

def management(current_budget, budget_name):
    while True:
        try:
            print(budget_name.removesuffix(".json"))

            #Spending total
            categories = current_budget["expenses"]
            total_spending = 0
            for category, purchases in current_budget["expenses"].items():
                for item, cost in purchases.items():
                    total_spending += cost
            print("$",total_spending, "/", "$",current_budget["limit"])

            print("\nPlease choose an option from the list below (1-5): ")
            print("[1] View Expenses")
            print("[2] Add Purchase")
            print("[3] Create Categories")
            print("[4] Settings")
            print("[5] Return to Main Menu") #Find a way to return back to loadbudget
            choice = input("Please enter your choice: ")
            match choice:
                case "1":
                    print("\n<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>")
                    expenses(current_budget)
                    print("<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>\n")
                case "2":
                    purchase_menu(current_budget)
                case "3":
                    create_categories(current_budget)
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

def expenses(current_budget):
    print("Current Purchases:\n")
    # Index the categories, print them with their index
    categories = current_budget["expenses"]
    total_spending = 0
    for i, (category, purchases) in enumerate(categories.items()):
        for item, cost in purchases.items():
            print(f"{category.capitalize()}: ${cost} - {item}")
            total_spending += cost
    print("Total Spent: $",total_spending)

def purchase_menu(current_budget):
    print("What category should your purchase be added to?:")

    categories = current_budget["expenses"]
    #Index the categories, print them with their index
    for i, category in enumerate(categories.keys()):
        print(f"[{i+1}] {category.capitalize()}")

    #Category choice (returns index) + error handling
    try:
        cat_choice = input("Choose one: ")
        cat_choice = int(cat_choice) - 1
        if cat_choice < 0 or cat_choice >= len(categories):
            raise ValueError("Invalid choice")
    except ValueError:
        print("Invalid choice")
        return

    #Name of item being added + cost
    purchase = input("Purchase: ")
    cost = float(input("Cost: "))

    #Whatever category matches the index from before gets ran in add_purchase()
    for i, category in enumerate(categories.keys()):
        if cat_choice == i:
            add_purchase(current_budget, category, purchase, cost)

def add_purchase(current_budget, category, purchase, cost):
    # Create new dic with purchase in it. Create the filename, open the file at that name, write the new dict in

    #Create the new dictionary entry for the item
    print("Adding", purchase, "to", category, "with the price", cost, "\n")
    current_budget["expenses"][category][purchase] = cost

    #Create filename w/ the dir, filename and json file extension
    budgets_folder = "Budgets"
    filename = os.path.join(budgets_folder, current_budget["budget_name"] + ".json")
    #Open file with filename
    with open(filename, "w") as budget_file:
        json.dump(current_budget, budget_file, indent=4)

def create_categories(current_budget):
    #Was very easy to implement, just copied from add_purchase(). Ask for name, write to dict, open json, write to it.
    #Ask for cat name, put it in the dict (made it lower just in case)
    cat_name = input("What should the new category be: ").lower()
    current_budget["expenses"][cat_name] = {}
    #Create filename w/ the dir, filename and json file extension
    budgets_folder = "Budgets"
    filename = os.path.join(budgets_folder, current_budget["budget_name"] + ".json")
    #Open file with filename
    with open(filename, "w") as budget_file:
        json.dump(current_budget, budget_file, indent=4)

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
            current_budget, budget_name = loadBudget()
            #Bulk of budget manipulation done here
            management(current_budget, budget_name)
        except:
            print("Something went wrong, please report this to the developer\n")


main()



