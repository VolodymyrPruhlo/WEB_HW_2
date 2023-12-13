from datetime import datetime, timedelta
import pickle
import atexit
import os
import objects
import sorter
import view


def save_data(address_book, notes):
    with open('address_book.pkl', 'wb') as address_book_file:
        pickle.dump(address_book, address_book_file)
    with open('notes.pkl', 'wb') as notes_file:
        pickle.dump(notes, notes_file)


def load_data():
    address_book = objects.AddressBook()
    notes = objects.Notes()

    if os.path.exists('address_book.pkl'):
        with open('address_book.pkl', 'rb') as address_book_file:
            address_book = pickle.load(address_book_file)

    if os.path.exists('notes.pkl'):
        with open('notes.pkl', 'rb') as notes_file:
            notes = pickle.load(notes_file)

    return address_book, notes


def help_func():
    help_text = "Available commands:\n\n"

    commands = {
        "add": "Додати контакт: Ця команда дозволяє вам додати новий контакт до адресної книги. Ви вводите ім'я, номер телефону, електронну пошту (за бажанням), адресу (якщо є) та дату народження (за бажанням) для нового контакту.",
        "search": "Пошук контакту: Ця команда дозволяє вам знайти контакти за ключовим словом. Ви вводите ключове слово, і програма виводить контакти, які містять це слово в імені, телефоні, електронній пошті або адресі.",
        "delete": "Видалити контакт: Ця команда дозволяє вам видалити контакт з адресної книги. Ви вводите ім'я контакту, який потрібно видалити.",
        "add note": "Додати нотатку: Ця команда дозволяє вам додати нову нотатку до своїх нотаток. Ви вводите текст нотатки та теги (якщо є).",
        "search note": "Пошук нотатки: Ця команда дозволяє вам знайти нотатки за ключовим словом. Ви вводите ключове слово, і програма виводить нотатки, які містять це слово в тексті.",
        "sort": "Сортування нотаток за тегами: Ця команда сортує ваші нотатки за тегами. Ви вводите тег, і програма виводить всі нотатки з цим тегом, впорядковані за ним.",
        "sort folder": "Ця команда сортує файли в папці за розширеннями, видаляє пусті папки",
        "hello": "Вивести привітання: Ця команда виводить привітання від бота.",
        "close": "Завершити роботу: Ця команда завершує роботу програми та виводить прощання.",
        "clear": "Видалення данних: Ця команда видаляє всі збережені данні в нотатках та адресної книзі.",
        "change": "Редагування контакту: Ця команда дозволяє змінити будь-яке поле контакту.",
        "all": "Вивід всіх наявних контактів: ця команда виводить список всіх контактів",
        "all notes": "Вивід всіх наявних нотатків: ця команда виводить список всіх нотаток",
        "change note": "Редагування нотатків: ця команда дозволяж редагувати нотатки і теги.",
        "delete note": "Видалення нотатки: ця команда видаляє нотатку",
        "birthday": "Список іменинників: ця команда показує список іменинників на найближчий тиждень",
        "help": "Список всіх команд"
    }

    for command, description in commands.items():
        help_text += f"{command}: {description}\n\n"

    my_print.display(help_text)


def add_contact(address_book):
    while True:
        name = my_input.replace_input("Enter the contact's name: ")
        while True:
            try:
                name = objects.Name(name)
                break
            except ValueError as e:
                my_print.display(f"Error: {e}")
                name = my_input.replace_input("Enter the contact's name: ")

        phone = my_input.replace_input("Enter the contact's phone: ")
        while True:
            try:
                if phone:
                    phone = objects.Phone(phone)
                break
            except ValueError as e:
                my_print.display(f"Error: {e}")
                phone = my_input.replace_input("Enter the contact's phone: ")

        email = my_input.replace_input("Enter the contact's email (if available, otherwise press Enter): ")
        while True:
            try:
                if email:
                    email = objects.Email(email)
                break
            except ValueError as e:
                my_print.display(f"Error: {e}")
                email = my_input.replace_input("Enter the contact's email: ")

        address = my_input.replace_input(
            "Enter the contact's address (if available, format input - city street house, otherwise press Enter): ")
        while True:
            try:
                if address:
                    new_address = address.split()
                    city, street, house = new_address
                    address = objects.Address(city, street, house)
                break
            except (ValueError, IndexError) as e:
                my_print.display(f"Error: {e}")
                address = my_input.replace_input("Enter the contact's address: ")

        birthday = my_input.replace_input("Enter the birthday (if available, otherwise press Enter): ")
        while True:
            try:
                if birthday:
                    birthday = datetime.strptime(birthday, "%Y-%m-%d")
                break
            except ValueError as e:
                my_print.display(f"Error: {e}")
                birthday = my_input.replace_input("Enter a valid birthday in the format YYYY-MM-DD (or press Enter to skip): ")

        contact = objects.Record(name.name, birthday)
        if phone:
            contact.add_phone(phone.phone)
        if email:
            contact.add_email(email.email)
        if address:
            city, street, house = address.city, address.street, address.house
            contact.add_address(city, street, house)
        address_book.add_record(contact)
        my_print.display(f'New contact, {name.name} successfully added')
        break


def show_contacts(address_book):
    if not address_book.data:
        my_print.display("Address book is empty.")
    else:
        for name, records in address_book.data.items():
            for record in records:
                contact_info = f"Contact name: {record.name.value},"
                if record.emails and record.emails is not None:
                    contact_info += f" Email: {', '.join(email.value for email in record.emails)},"
                else:
                    contact_info += " Email: N/A,"
                if record.phones and record.phones is not None:
                    contact_info += f" Phone: {', '.join(phone.value for phone in record.phones)},"
                else:
                    contact_info += " Phone: N/A,"
                if record.addresses and record.addresses is not None:
                    contact_info += f" Address: {', '.join(str(address) for address in record.addresses)},"
                else:
                    contact_info += " Address: N/A,"
                if record.birthday and record.birthday.birthday is not None:
                    contact_info += f" Birthday: {record.birthday.birthday.strftime('%Y-%m-%d')}"
                else:
                    contact_info += " Birthday: N/A"
                my_print.display(contact_info)


def show_notes(notes):
    if not notes.notes:
        my_print.display("No notes available.")
    else:
        my_print.display("List of all notes:")
        for index, note in enumerate(notes.notes, start=1):
            my_print.display(f"{index}. Text: {note.text}")
            if note.tags:
                my_print.display(f"   Tags: {', '.join(note.tags)}")
            else:
                my_print.display("   Tags: N/A")


def change_contact(address_book, contact_name):
    found_contacts = address_book.find_contact(contact_name)

    if not found_contacts:
        my_print.display(f"Contact '{contact_name}' not found.")
        return

    if len(found_contacts) > 1:
        my_print.display("Found multiple contacts:")
        for i, contact in enumerate(found_contacts):
            my_print.display(f"{i + 1}. {contact.name.value}")
        while True:
            choice = my_input.replace_input("Enter the number of the contact you want to change: ")
            try:
                choice = int(choice) - 1
                if 0 <= choice < len(found_contacts):
                    contact = found_contacts[choice]
                    break
                else:
                    my_print.display("Invalid choice.")
            except ValueError:
                my_print.display("Invalid input.")
    else:
        contact = found_contacts[0]

    if contact.name:
        contact_info = f"Contact found: Contact name: {contact.name.value},"
    else:
        contact_info = "Contact found: Contact name: N/A,"

    if contact.emails and contact.emails is not None:
        contact_info += f" Email: {', '.join(email.value for email in contact.emails)},"
    else:
        contact_info += " Email: N/A,"

    if contact.phones and contact.phones is not None:
        phone_values = [phone.value for phone in contact.phones]
        contact_info += f" Phone: {', '.join(phone_values)},"
    else:
        contact_info += " Phone: N/A,"

    if contact.addresses and contact.addresses is not None:
        contact_info += f" Address: {', '.join(map(str, contact.addresses))}"
    else:
        contact_info += " Address: N/A,"

    if contact.birthday and contact.birthday.birthday is not None:
        contact_info += f" Birthday: {contact.birthday.birthday.strftime('%Y-%m-%d')}"
    else:
        contact_info += " Birthday: N/A"

    my_print.display(contact_info)

    while True:
        field_to_change = my_input.replace_input("Enter the field you want to change (name, phone, email, address, birthday) or 'cancel' to exit: ").lower()

        if field_to_change == 'cancel' or field_to_change in 'cancel':
            my_print.display("Change canceled.")
            break
        if field_to_change == 'name' or field_to_change in 'name':
            new_name = my_input.replace_input("Enter the new name: ")
            contact.name.value = new_name
            my_print.display(f"Contact name changed to {new_name}")
            continue
        elif field_to_change == 'phone' or field_to_change in 'phone':
            if contact.phones:
                old_phone = my_input.replace_input("Enter the old phone number: ")
            else:
                old_phone = None

            new_phone = my_input.replace_input("Enter the new phone number: ")

            if new_phone:
                try:
                    objects.Phone(new_phone)

                    if old_phone:
                        contact.remove_phone(old_phone)
                        contact.add_phone(new_phone)
                        my_print.display(f"Phone number changed from {old_phone} to {new_phone}")
                    else:
                        contact.add_phone(new_phone)
                        my_print.display(f"Phone number {new_phone} added")
                    continue
                except ValueError as e:
                    my_print.display(f"Error: {e}")
            else:
                my_print.display("New phone number cannot be empty.")
        elif field_to_change == 'email' or field_to_change in 'email':
            if contact.emails:
                old_email = my_input.replace_input("Enter the old email address: ")
            else:
                old_email = None

            new_email = my_input.replace_input("Enter the new email address: ")

            if new_email:
                try:
                    objects.Email(new_email)

                    if old_email:
                        contact.emails = [email for email in contact.emails if email.value != old_email]
                        contact.add_email(new_email)
                        my_print.display(f"Email address changed from {old_email} to {new_email}")
                    else:
                        contact.add_email(new_email)
                        my_print.display(f"Email address {new_email} added")
                    continue
                except ValueError as e:
                    my_print.display(f"Error: {e}")
            else:
                my_print.display("New email address cannot be empty.")
        elif field_to_change == 'address' or field_to_change in 'address':
            if contact.addresses:
                old_address = my_input.replace_input("Enter the old address (format: city street house): ")
            else:
                old_address = None

            new_address = my_input.replace_input("Enter the new address (format: city street house): ")

            if new_address:
                try:
                    new_address_parts = new_address.split()
                    if len(new_address_parts) == 3:
                        new_city, new_street, new_house = new_address_parts
                        if old_address:
                            old_address_parts = old_address.split()
                            if len(old_address_parts) == 3:
                                old_city, old_street, old_house = old_address_parts
                                contact.addresses = [
                                    address for address in contact.addresses if
                                    address.city != old_city or address.street != old_street or address.house != old_house
                                ]
                                contact.add_address(new_city, new_street, new_house)
                                my_print.display(f"Address changed from {old_address} to {new_address}")
                            else:
                                my_print.display("Invalid old address format.")
                        else:
                            contact.add_address(new_city, new_street, new_house)
                            my_print.display(f"Address {new_address} added")
                        continue
                    else:
                        my_print.display("Invalid new address format.")
                except (ValueError, IndexError) as e:
                    my_print.display(f"Error: {e}")
            else:
                my_print.display("New address cannot be empty.")
        elif field_to_change == 'birthday' or field_to_change in 'birthday':
            new_birthday = my_input.replace_input("Enter the new birthday (format: YYYY-MM-DD): ")
            if new_birthday:
                try:
                    new_birthday = datetime.strptime(new_birthday, "%Y-%m-%d")
                    contact.birthday.birthday = new_birthday
                    my_print.display(f"Birthday changed to {new_birthday.strftime('%Y-%m-%d')}")
                except ValueError:
                    my_print.display("Invalid date format.")
            else:
                contact.birthday = None
                my_print.display("Birthday cleared.")
            continue
        else:
            my_print.display("Invalid field to change.")


def show_birthday_this_week(address_book):
    current_date = datetime.now()
    end_of_week = current_date + timedelta(days=(6 - current_date.weekday()) + 7)  # Find the end of the current week

    birthday_contacts = []

    for records in address_book.values():
        for contact in records:
            if contact.birthday and contact.birthday.birthday:
                birthday_date = contact.birthday.birthday.replace(year=current_date.year)  # Assume the birthday is in the current year
                if current_date <= birthday_date <= end_of_week:
                    birthday_contacts.append(contact)

    if birthday_contacts:
        my_print.display("Birthday persons this week:")
        for contact in birthday_contacts:
            my_print.display(f"Name: {contact.name.value}, Birthday: {contact.birthday.birthday.strftime('%Y-%m-%d')}")
    else:
        my_print.display("No birthdays this week.")


def change_note(notes, note_text):
    found_notes = []
    for note in notes.notes:
        if note_text.lower() in note.text.lower():
            found_notes.append(note)

    if not found_notes:
        my_print.display(f"Note with text '{note_text}' not found.")
        return

    if len(found_notes) > 1:
        my_print.display("Found multiple notes:")
        for i, note in enumerate(found_notes):
            my_print.display(f"{i + 1}. {note.text}")
        while True:
            choice = my_input.replace_input("Enter the number of the note you want to change: ")
            try:
                choice = int(choice) - 1
                if 0 <= choice < len(found_notes):
                    note = found_notes[choice]
                    break
                else:
                    my_print.display("Invalid choice.")
            except ValueError:
                my_print.display("Invalid input.")
    else:
        note = found_notes[0]

    my_print.display(f"Note found: Text: {note.text}, Tags: {', '.join(note.tags)}")

    while True:
        field_to_change = my_input.replace_input("Enter the field you want to change (text, tags): ").lower()

        if field_to_change == 'text':
            new_text = my_input.replace_input("Enter the new text for the note: ")
            note.text = new_text
            my_print.display(f"Note text changed to '{new_text}'")
            break
        elif field_to_change == 'tags':
            new_tags = my_input.replace_input("Enter the new tags (comma-separated): ").split(',')
            note.tags = new_tags
            my_print.display(f"Tags updated to: {', '.join(new_tags)}")
            break
        else:
            my_print.display("Invalid field to change.")


def search_contact(address_book):
    query = my_input.replace_input("Enter the search keyword: ")
    found_contacts = address_book.find_contact(query)
    if found_contacts:
        my_print.display("Found contacts:")
        for contact in found_contacts:

            contact_info = f"Name: {contact.name.value}"
            if contact.emails and contact.emails is not None:
                contact_info += f", Email: {', '.join(email.value for email in contact.emails)}"
            else:
                contact_info += f", Email: N/A"
            if contact.phones and contact.phones is not None:
                contact_info += f", Phone: {', '.join(phone.value for phone in contact.phones)}"
            else:
                contact_info += f", Phone: N/A"
            if contact.addresses and contact.addresses is not None:
                contact_info += f", Address: {', '.join(str(address) for address in contact.addresses)}"
            else:
                contact_info += f", Address: N/A"
            if contact.birthday and contact.birthday.birthday is not None:
                contact_info += f", Birthday: {contact.birthday.birthday.strftime('%Y-%m-%d')}"
            else:
                contact_info += f", Birthday: N/A"
            my_print.display(contact_info)
    else:
        my_print.display("Contacts not found.")


def delete_contact(address_book, name):
    if name in address_book.data:
        address_book.delete(name)
        my_print.display(f"Contact '{name}' deleted.")
    else:
        my_print.display("Contact not found.")


def delete_note(notes, keyword):
    found_notes = []

    for i, note in enumerate(notes.notes):
        if keyword.lower() in note.text.lower() or keyword in note.tags:
            found_notes.append((i, note))

    if not found_notes:
        my_print.display(f"No notes found with the keyword '{keyword}'.")
        return

    if len(found_notes) > 1:
        my_print.display("Found multiple notes:")
        for i, note in enumerate(found_notes):
            my_print.display(f"{i + 1}. Text: {note[1].text}")
            if note[1].tags:
                my_print.display(f"   Tags: {', '.join(note[1].tags)}")
            else:
                my_print.display("   Tags: N/A")
        while True:
            choice = my_input.replace_input("Enter the number of the note you want to delete: ")
            try:
                choice = int(choice) - 1
                if 0 <= choice < len(found_notes):
                    note_index = found_notes[choice][0]
                    break
                else:
                    my_print.display("Invalid choice.")
            except ValueError:
                my_print.display("Invalid input")
    else:
        note_index = found_notes[0][0]

    note = notes.notes[note_index]
    my_print.display("Found note:")
    my_print.display(f"Text: {note.text}")
    if note.tags:
        my_print.display(f"Tags: {', '.join(note.tags)}")
    else:
        my_print.display("Tags: N/A")

    confirm_delete = my_input.replace_input("Do you want to delete this note? (yes/no): ").lower()
    if confirm_delete == 'yes' or confirm_delete == 'y':
        del notes.notes[note_index]
        my_print.display(f"Note with the keyword '{keyword}' deleted successfully.")
    else:
        my_print.display("Deletion canceled.")


def add_note(notes):
    text = my_input.replace_input("Enter note text: ")
    tags = my_input.replace_input("Enter tags (comma-separated): ").split(',')
    note = objects.Note(text, tags)
    notes.add_note(note)


def search_note(notes):
    keyword = my_input.replace_input("Enter a keyword to search for: ")
    tag_search = my_input.replace_input("Do you want to search by tag (yes or no)? ").lower()

    found_notes = []
    for note in notes.notes:
        if keyword.lower() in note.text.lower() and (not tag_search or tag_search == "no" or tag_search == "n"):
            found_notes.append(note)
        elif tag_search and tag_search in ["yes", "y"] and keyword.lower() in note.tags:
            found_notes.append(note)

    if found_notes:
        my_print.display("Found notes:")
        for note in found_notes:
            my_print.display(f"Note text: {note.text}")
            my_print.display(f"Tags: {', '.join(note.tags)}")
    else:
        my_print.display("Notes not found.")


def sort_notes_by_tags(notes):
    tag = my_input.replace_input("Enter a tag for sorting: ")
    sorted_notes = notes.sort_notes_by_tags(tag)
    if sorted_notes:
        my_print.display(f"Sorted notes by tag '{tag}':")
        for note in sorted_notes:
            my_print.display(f"Note text: {note.text}")
            my_print.display(f"Tags: {', '.join(note.tags)}")
    else:
        my_print.display(f"No notes with the tag '{tag}' found.")


def user_error(func):
    def inner(*args):
        try:
            return func(*args)
        except IndexError:
            return "Not enough params."
        except KeyError:
            return "Unknown record_id."
        except ValueError:
            return "Error: Invalid value format."

    return inner


def hello():
    return f"Welcome to assist bot"


def clear_data(address_book, notes):
    confirmation = input("Are you sure you want to clear all data? (yes or no): ").lower()
    if confirmation == "yes" or confirmation == "y":
        address_book.clear()
        notes.clear()
        my_print.display("All data has been cleared.")
    else:
        my_print.display("Clearing data canceled.")


COMMANDS = {'add': add_contact, 'search': search_contact, 'delete': delete_contact}


def process_command(command, address_book):
    if command in COMMANDS:
        COMMANDS[command](address_book)
    else:
        my_print.display("Invalid command")


@user_error
def main():
    address_book, notes = load_data()
    atexit.register(save_data, address_book, notes)
    my_print.display('Welcome to assist bot')
    my_print.display('If you need list of commands, write "help" and press ENTER.')
    while True:

        user_input = my_input.replace_input("Enter a command: ")
        if user_input == 'hello':
            my_print.display('Hello how can i help you')

        elif user_input == 'close':
            my_print.display("Good bye")
            break
        elif user_input == 'delete':
            name = my_input.replace_input("Enter the contact's name to delete: ")
            delete_contact(address_book, name)
        elif user_input == 'add note':
            add_note(notes)
        elif user_input == 'search note':
            search_note(notes)
        elif user_input == 'sort':
            sort_notes_by_tags(notes)
        elif user_input == 'help':
            help_func()
        elif user_input == 'clear':
            clear_data(address_book, notes)
        elif user_input == 'change':
            contact_name = my_input.replace_input("Enter a keyword to find a contact: ")
            change_contact(address_book, contact_name)
        elif user_input == 'all':
            show_contacts(address_book)
        elif user_input == 'change note':
            note_text = my_input.replace_input("Enter the text of the note you want to change: ")
            change_note(notes, note_text)
        elif user_input == "all notes":
            show_notes(notes)
        elif user_input == 'sort folder':
            folder_path = my_input.replace_input("Enter the path to the folder you want to sort: ")
            sorter.sort_files(folder_path)
        elif user_input == 'delete note':
            keywords = my_input.replace_input('Enter keyword to search note: ')
            delete_note(notes, keywords)
        elif user_input == 'birthday' or user_input == 'bd':
            show_birthday_this_week(address_book)
        else:
            process_command(user_input, address_book)


if __name__ == "__main__":
    my_input = view.UserInputAdapter()
    my_print = view.ConsoleDisplayAdapter()
    main()
