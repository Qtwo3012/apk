from menu import Menu
from controller import Controller

menu = Menu()
controller = Controller()

while True:

    choice = menu.show()

    if choice == "1":
        controller.import_txt()

    elif choice == "2":
        controller.show_database()

    elif choice == "3":
        controller.analyze()

    elif choice == "4":
        controller.export()

    elif choice == "5":
        print("Good Bye Partner 😎")
        break

    else:
        print("Invalid Menu")