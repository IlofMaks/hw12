from collections import UserDict
from datetime import date, datetime


class Field:
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def __str__(self):
        return f'{self.value}'

    def __repr__(self):
        return f'{self.value}'


class Name(Field):
    def __init__(self, value=None):
        super().__init__(value)
    def __repr__(self) -> str:
        return f"Name(value = {self.value})"


class Phone(Field):

    @Field.value.setter
    def value(self, value):
        if not value.isnumeric():
            raise ValueError('Wrong phones.')
        if len(value) != 10:
            raise ValueError("Phone must contains 10 symbols.")
        self._value = value

    def __eq__(self, other):
        return self.value == other.value

class Birthday(Field):
    @Field.value.setter
    def value(self, value):
        day_today = datetime.today()
        try:
            b_day = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Incorrect date format, should be `DD.MM.YYYY`")
        if b_day.date() > day_today.date():
            raise ValueError("Birthday can't be more than current year and date.")
        self._value = b_day



    def __str__(self):
        return datetime.strftime(self.value, "%d.%m.%Y")

    def __repr__(self):
        return f"Birthday(value = {self.value})"


class Record:
    def __init__(self, name: Name, birthday:Birthday = None):
        self.name = name
        self.phones = []
        self.birthday = birthday
        
    def add_phone(self, phone: Phone):
        self.phones.append(phone)
        
    def edit_phone(self, new_phone: Phone):
        self.phones = new_phone
        
    def delete_phone(self, phone_index: int):
        del self.phones[phone_index]
    
    def add_birthday(self, birthday: Birthday):
        self.birthday = birthday

    def days_to_birthdays(self):
        if self.birthday:
            return self.birthday.days_to_birthdays()
        else:
            return None
    def __str__(self)-> str:
        if self.birthday:
            return f'{", ".join([ph.value for ph in self.phones])} Birthday: {self.birthday}'
        return f'{", ".join([ph.value for ph in self.phones])}' 
    
    def __repr__(self) -> str:
        return f'{self.name}: {", ".join([str(phone) for phone in self.phones])}, {self.birthday}'

class AddressBook(UserDict):
    def add_record(self, record: Record) -> Record | None:
        if not self.data.get(record.name.value):
            self.data[record.name.value] = record
            return record
    
    def search_contacts(self, search_string):
        matching_contacts = []
        for record in self.data.values():
            if search_string.lower() in record.name.value.lower():
                matching_contacts.append(record)
            else:
                for phone in record.phones:
                    if search_string in phone.value:
                        matching_contacts.append(record)
                        break
        return matching_contacts


    def iterator(self, count=3):
        records = []
        i = 0
        for record in self.data.values():
            records.append(record)
            i += 1
            if i == count:
                yield records
                records = []
                i = 0
        if records:
            yield records

                

    def __str__(self):
        return f'{self.data}'

    def __repr__(self):
        return f'{self.data}'

