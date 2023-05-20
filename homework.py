from datetime import datetime, date
from adressbook import AddressBook, Record, Phone, Name, Birthday
import pickle

USERS = AddressBook()


def save_contacts(filename):
    try:
        with open(filename, "wb") as file:
            pickle.dump(USERS.data, file)
        print(f"Контакти збережено в файлі '{filename}'.")
    except IOError as e:
        print(f"Помилка: Не вдалося зберегти контакти у файл '{filename}': {str(e)}")

def load_contacts(filename):
    try:
        with open(filename, 'rb') as file:
            USERS.data = pickle.load(file)
        print("Loaded successfully")
    except (IOError, pickle.UnpicklingError):
        print("Error, failed to load")
        # Створити файл, якщо він не існує
        with open(filename, 'wb') as file:
            pickle.dump({}, file)
        print(f"Created a new file '{filename}'.")



def handle_error(func):
    def inner(*args):
        try:
            result = func(*args)
            return result
        except KeyError:
            return "No user"
        except ValueError:
            return 'Give me name and phone please'
        except IndexError:
            return 'Enter user name'
    return inner



def hello_user():
    return "Whats up"

def unknown_command(user_input):
    return f"unknown_command {user_input}"

def close_app():
    exit('Good Bye')

def add_user(name: str, phone: str) -> str:
    name_field = Name(name)
    phone_field = Phone(phone)
    if name in USERS:
        record = USERS[name]
        record.add_phone(phone_field)
        return f"Phone {phone} added for {name}"
    else:
        record = Record(name_field)
        record.add_phone(phone_field)
        USERS.add_record(record)
        return f"User {name} added with phone {phone}"

def add_birthday(name: Name, birthday: Birthday) -> str:
    record = USERS.data.get(name)
    if not record:
        return f"No record found with name {name.value}."
    record.add_birthday(birthday)
    return f"Birthday added to record {name}."


def change_phone(name: Name, new_phone: Phone) -> str:
    if name in USERS:
        record = USERS[name]
        old_phone = record.phones[0]
        record.phones[0] = new_phone
        USERS[name] = record
        return f'User {name} has new number: {new_phone}, old phone number: {old_phone}'
    else:
        return f'This user: {name} is not in your phone book'
    

def show_all() -> str:
    if not USERS:
        return 'Contacts are empty'
    records = 'List of contacts:\n'
    for records_chunk in USERS.iterator():
        for record in records_chunk:
            phones = ', '.join(str(phone) for phone in record.phones)
            record_str = f"{record.name}: {phones}"
            if record.birthday:
                record_str += f" Birthday: {record.birthday}"
            records += record_str + '\n'
    return records
    


def show_phone(name_str: str) -> str:
    name_field = Name(name_str)
    if name_field.value in USERS:
        record = USERS[name_field.value]
        return f"{name_field.value}'s phone number is {record.phones[0]}"
    else:
        return f"No phone number found for {name_field.value}"
    

def days_to_birthdays(name):
    record = USERS.data.get(name)
    if not record:
        return f'User {name} not found'
    
    today = date.today()
    dob = datetime.strptime(record.birthday, '%d.%m.%Y').date()
    dob_this_year = dob.replace(year=today.year)
    
    if dob_this_year < today:
        dob_this_year = dob_this_year.replace(year=today.year + 1)
        
    days = (dob_this_year - today).days
    if days == 0:
        return 'Happy birthday!'
    elif days == 1:
        return f'1 day until {name}\'s birthday'
    else:
        return f'{days} days until {name}\'s birthday'

def search(user_input):
    return USERS.search_contacts(user_input)

UI_HANDLERS = {
    'hello': hello_user,
    'add': add_user,
    'change': change_phone,
    'phone': show_phone,
    'show all': show_all,
    'exit': close_app,
    'good bye': close_app,
    'close': close_app,
    'birth': add_birthday,
    'bd': days_to_birthdays,
    'search': search
}

@handle_error
def parse_input(user_input):
    parts = user_input.split(' ')
    user_input_name = parts[0]
    if user_input_name == 'show' and 'all' in parts:
        user_input_name = 'show all'
        user_input_args = []
    elif user_input_name == 'good' and 'bye' in parts:
        user_input_name = 'good bye'
        user_input_args = []
    elif len(parts)>1:
        user_input_args = parts[1:]
    else:
        user_input_args=[]
    return user_input_name, user_input_args

def main():
    print("Hello")
    load_contacts("address_book.pickle")
    while True:
        user_input = input("Enter command: ")
        if not user_input:
            continue
        command, args = parse_input(user_input)
        if command not in UI_HANDLERS:
            print(unknown_command(user_input))
        else:
            result = UI_HANDLERS[command](*args)
            print(result)
            save_contacts("address_book.pickle")
        

if __name__ == '__main__':
    main()
