from collections import UserDict
from datetime import datetime, timedelta
import pickle

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Please enter a valid name")
        super().__init__(value)

class Phone(Field):
    def __init__(self, value):
        if not self.validate(value):
            raise ValueError("Phone must be 10 digits")
        super().__init__(value)
    
    def validate(self, phone) -> bool:
        return len(phone) == 10 and phone.isdigit()
    
class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone) -> None:
        """Adds a new phone to the record"""
        self.phones.append(Phone(phone))

    def remove_phone(self, phone) -> bool:
        """Removes a phone from the record"""
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return True
        return False

    def edit_phone(self, old_phone, new_phone) -> bool:
        """Edits an existing phone"""
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return True
        raise ValueError(f"Phone {old_phone} not found in contact")
    
    def add_birthday(self, birthday) -> None:
        """Adds a birthday to the record"""
        self.birthday = Birthday(birthday)

    def find_phone(self, phone) -> Phone | None:
        """Finds a phone in the list of phones in the record"""
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record):
        """Adds a record to the address book"""
        self.data[record.name.value] = record

    def find(self, name) -> Record | None:
        """Finds a record by name"""
        return self.data.get(name)

    def delete(self, name) -> bool:
        """Removes by name"""
        if name in self.data:
            del self.data[name]
            return True
        return False
    
    def get_upcoming_birthdays(self, days_ahead: int = 7) -> list[dict]:
        """Get upcoming birthdays"""
        today = datetime.now()
        upcoming_birthdays = []
        for user in self.data.values():
            if user.birthday:
                upcoming_birthdays.append({
                    "name": user.name.value,
                    "birthday": user.birthday.value.strftime("%d.%m.%Y")
                })
        return upcoming_birthdays

def save_data(book, filename="addressbook.pkl"):
    """Save address book to file"""
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    """Load address book from file"""
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()
