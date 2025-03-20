from address_book_module import AddressBook, Record, save_data, load_data
import pickle

BOOK_FILE = "addressbook.pkl"

address_book = load_data()

def main():
    """Main function to run the assistant bot with a command loop"""
    print("Welcome to the assistant bot!")

    commands = {
        "hello": greet,
        "add": add_contact,
        "change": change_contact,
        "phone": show_phone,
        "all": show_all,
        "add-birthday": add_birthday,
        "show-birthday": show_birthday,
        "birthdays": birthdays,
        "delete": delete_contact,
        "close": goodbye,
        "exit": goodbye
    }

    while True:
        user_input = input("Enter a command: ").strip()  # Убираем пробелы
        if not user_input:  # Проверяем пустой ввод
            continue
        
        cmd, *args = user_input.split()
        cmd = cmd.lower()

        if cmd in commands:
            print(commands[cmd](*args))
            if cmd in ["close", "exit"]:
                save_data(address_book)
                break
        else:
            print("Invalid command.", "Available commands: ", ", ".join(commands.keys()))

def input_error(ValueErrorMessage="Give me name and phone please."):
    """Decorator to handle input errors"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ValueError:
                return ValueErrorMessage
        return wrapper
    return decorator

@input_error()
def add_contact(name, phone):
    """Add a new contact"""
    record = address_book.find(name)
    if record:
        return "Contact already exists."
    else:
        record = Record(name)
        record.add_phone(phone)
        address_book.add_record(record)
        return f"Contact {name} added."

@input_error()
def change_contact(name, old_phone, new_phone):
    """Update phone number"""
    contact = address_book.find(name)
    if not contact:
        return "Contact not found."
    try:
        contact.edit_phone(old_phone, new_phone)
        return f"Phone {old_phone} changed to {new_phone} for {name}."
    except ValueError:
        return f"Phone {old_phone} not found for {name}."

@input_error()
def show_phone(name):
    """Show phone number"""
    contact = address_book.find(name)
    return contact.phones[0].value if contact else "Contact not found."

@input_error()
def add_birthday(name, birthday):
    """Add birthday"""
    contact = address_book.find(name)
    if not contact:
        return "Contact not found."
    contact.add_birthday(birthday)
    return "Birthday added."

@input_error()
def show_birthday(name):
    """Show birthday"""
    contact = address_book.find(name)
    return contact.birthday.value.strftime("%d.%m.%Y") if contact and contact.birthday else "Birthday not set."

def birthdays():
    """Show upcoming birthdays"""
    upcoming = address_book.get_upcoming_birthdays()
    return "\n".join(f"{b['name']} - {b['birthday']}" for b in upcoming) if upcoming else "No upcoming birthdays."

def show_all():
    """Show all contacts"""
    if not address_book.data:
        return "No contacts found."
    return "\n".join(f"{c.name.value} - {', '.join(p.value for p in c.phones)} - {c.birthday.value.strftime('%d.%m.%Y') if c.birthday else 'No birthday'}" for c in address_book.data.values())

@input_error()
def delete_contact(name):
    """Delete contact"""
    if address_book.delete(name):
        return f"Contact {name} deleted."
    return "Contact not found."

def greet():
    """Return greeting message"""
    return "How can I help you?"

def goodbye():
    """Save data and exit"""
    save_data(address_book)
    return "Goodbye!"

if __name__ == "__main__":
    main()


