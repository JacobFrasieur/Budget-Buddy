import json
import os
import sys

#LIST TO BE ADDED:
#1. User story requires I add some sort of warning when budget near threshold
#2. User story requires I show the amount that a user is over budget

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
                "Please enter a number to pick an option below:\n[1] New Budget\n[2] Load Budget\n[3] Delete Budget\n[4] Tutorial\n[5] Close Program")
            choice = input("Please enter your choice (1-5): ")
            print("\n<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>\n")
            #We keep load separate from the startProgram - we load it after creation anyways
            match choice:
                case "1":
                    newBudget()
                    return "load"
                case "2":
                    budgets_folder = "Budgets"
                    if os.path.exists(budgets_folder):
                        return "load"
                    else:
                        raise FileNotFoundError
                case "3":
                    deleteBudget()
                    continue
                case "4":
                    tutorial()
                case "5":
                    return "exit"
                case _:
                    raise ValueError
        except ValueError:
            print("Invalid choice")
        except FileNotFoundError:
            print("You don't have any budget to load, please create one first!\n")

def newBudget():
    print(" A quick budget will set your budget name, income, and limit to default values.")
    quick_gen = input("Would you like to generate a quick budget? (Y/N): ")
    if quick_gen == "y" or quick_gen == "Y":
        category_type = "2"
    else:
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

    #Quick budget handling
    if quick_gen == "Y" or quick_gen == "y":
        budget_name = "Budget"
        income = "2000"
        limit = "2000"
    else:
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
    print("Deleting a budget will delete all purchases and categories you have added")
    delete_confirm = input("Do you want to delete this budget? (y/n): ")
    if delete_confirm == "y":
        os.remove(os.path.join(budgets_folder, selection))
        print(f"'{selection}' has been deleted\n")
    else:
        print("Deletion cancelled")

def management(current_budget, budget_name):
    while True:
        try:
            print(budget_name.removesuffix(".json"))

            #Spending total
            categories = current_budget["expenses"]
            threshold = 0.9
            total_spending = 0
            for category, purchases in current_budget["expenses"].items():
                for item, cost in purchases.items():
                    total_spending += cost
            print("$",total_spending, "/", "$",current_budget["limit"])
            if (float(current_budget["limit"]) * threshold) < float(total_spending) < float(current_budget["limit"]):
                print("Reaching spending limit")
            if float(total_spending) > float(current_budget["limit"]):
                print("Over budget by: $", float(total_spending) - float(current_budget["limit"]))

            print("\nPlease choose an option from the list below (1-5): ")
            print("[1] View Expenses")
            print("[2] Add Purchase")
            print("[3] Create Categories")
            print("[4] Settings")
            print("[5] Back")
            choice = input("Please enter your choice (1-5): ")
            match choice:
                case "1":
                    print("\n<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>")
                    expenses(current_budget)
                    print("<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>\n")
                case "2":
                    print("\n<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>")
                    purchase_menu(current_budget)
                    print("<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>\n")
                case "3":
                    print("\n<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>")
                    create_categories(current_budget)
                    print("<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>\n")
                case "4":
                    print("\n<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>")
                    #Handle rename without budget reload
                    budget_rename = settings(current_budget)
                    if budget_rename:
                        budget_name = budget_rename
                        continue
                    print("<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>\n")
                    continue
                case "5":
                    print("\n<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>\n")
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
    print("Total: $",total_spending)

def purchase_menu(current_budget):
    while True:
        print("What category should your purchase be added to?:")

        categories = current_budget["expenses"]
        #Index the categories, print them with their index
        for i, category in enumerate(categories.keys()):
            print(f"[{i+1}] {category.capitalize()}")


        try:
            # Category choice (returns index) + error handling
            cat_choice = input("Choose one: ")
            cat_choice = int(cat_choice) - 1
            if cat_choice < 0 or cat_choice >= len(categories):
                raise ValueError("Invalid choice")

            # Name of item being added & cost
            purchase = input("Purchase: ")
            cost = float(input("Cost: "))
            break

        except ValueError:
            print("Invalid choice, try again")



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

def settings(current_budget):
    while True:
        try:
            print("What would you like to do? (1-4):")
            print("\n[1] Change budget name")
            print("[2] Change budget limit")
            print("[3] Create budget backup")
            print("[4] Back")
            settings = input("Please enter your choice: ")
            match settings:
                case "1":
                    #Save old filename
                    budgets_folder = "Budgets"
                    old_filename = os.path.join(budgets_folder, current_budget["budget_name"] + ".json")
                    #Change budgets json name
                    new_name = input("\nPlease enter new name: ")
                    current_budget["budget_name"] = new_name

                    # Open file with filename
                    with open(old_filename, "w") as budget_file:
                        json.dump(current_budget, budget_file, indent=4)

                    # Create filename w/ the dir, filename and json file extension
                    filename = os.path.join(budgets_folder, current_budget["budget_name"] + ".json")
                    #Apply new filename
                    os.rename(old_filename, filename)

                    return new_name

                case "2":
                    #Change budget limit
                    new_limit = float(input("\nPlease enter new limit: "))
                    current_budget["limit"] = new_limit

                    # Create filename w/ the dir, filename and json file extension
                    budgets_folder = "Budgets"
                    filename = os.path.join(budgets_folder, current_budget["budget_name"] + ".json")
                    # Open file with filename
                    with open(filename, "w") as budget_file:
                        json.dump(current_budget, budget_file, indent=4)

                case "3":
                    print("Creating backup...")
                    budgets_folder = "Budgets"
                    filename = os.path.join(budgets_folder, current_budget["budget_name"] + "_backup" + ".json")
                    # Open file with filename
                    with open(filename, "w") as budget_file:
                        json.dump(current_budget, budget_file, indent=4)
                    print("Backup created successfully")
                case "4":
                    return
                case _:
                    raise ValueError
        except ValueError:
            print("Invalid choice")

def tutorial():
    while True:
        try:
            info = input("What would you like to know about?:\n[1] How do I create a budget?\n[2] How do I add a purchase?\n[3] How do I add a category?\n[4] Where do I see my purchases?\n[5] How do I change my budget name or limit?\n[6] Exit tutorial\nPlease enter your choice: ")
            match info:
                case "1":
                    print("\nTo create a budget, simply type 1 while in the main menu and fill out the required fields.\n")
                case "2":
                    print("\nTo add a purchase, load a budget by typing 2 while in the main menu and then pick a budget. Once you do this, you will now see various options\nfor your budget. Type 2 to add a purchase and fill out the required fields.\n")
                case "3":
                    print("\nTo add a new category, load a budget by typing 2 while in the main menu and then pick a budget. Once you do this, you will now see various options\nfor your budget. Type 3 to add a new category and fill out the required fields.\n")
                case "4":
                    print("\nTo see your purchases, load a budget by typing 2 while in the main menu and then pick a budget. Once you do this, you will now see various options\nfor your budget. Click 1 to view your expenses.\n")
                case "5":
                    print("\nTo change your budget name or limit, first load a budget by typing 2 while in the main menu and then pick a budget. Once you do this, you will now see\n various options for your budget. Type 4 for settings, and choose the relevant option from the menu.\n")
                case "6":
                    print("\n<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>\n")
                    return
                case _:
                    raise ValueError
        except ValueError:
            print("Invalid choice, try again")
            return
#Main - Self explanatory
def main():
        banner()
        #Create/Load/Delete
        while True:
            #Changed to return instructions - things broke in a normal while loop
            instructions = startProgram()
            if instructions == "load":
                #Load current budget for use in management
                current_budget, budget_name = loadBudget()
                #Bulk of budget manipulation done here
                management(current_budget, budget_name)
            elif instructions == "exit":
                sys.exit()


main()


