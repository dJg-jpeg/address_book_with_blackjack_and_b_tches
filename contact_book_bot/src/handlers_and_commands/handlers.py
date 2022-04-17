from .bot_classes_and_exceptions.bot_classes import AddressBook, ContactOutput
from .bot_classes_and_exceptions.bot_exceptions import ExistContactError, \
    LiteralsInDaysError, ZeroDaysError, UnknownFieldError, InvalidDirectoryPathError
from .dir_sort_scrypt.dir_sorter import sort_dir
from typing import Optional

COMMANDS = (
    ('hello', 'help'),
    ('goodbye', 'exit', 'close'),
    ('add_contact', 'find_contact', 'delete_contact', 'show_all', 'edit_contact', 'add_info'),
    'birthdays_from_now',
    ('see_notes', 'add_note', 'delete_note', 'add_tag', 'find_notes_with_tag', 'change_note', 'search_for_notes'),
    'sort_dir',
)


def greetings() -> str:
    return f"Hi!\n" \
           f"Here are the commands , separated by categories :\n" \
           f"Need some help? : {', '.join(COMMANDS[0])}\n" \
           f"Contact commands : {', '.join(COMMANDS[2])}\n" \
           f"See contacts birthdays in inputted amount of days: {COMMANDS[3]}\n" \
           f"Notes commands : {', '.join(COMMANDS[4])}\n" \
           f"To sort directory by given path : {COMMANDS[5]}\n" \
           f"Stop bots work : {', '.join(COMMANDS[1])}\n"


def add_contact(contact: dict, contacts_book: AddressBook) -> str:
    if contact['name'] in contacts_book.keys():
        raise ExistContactError
    contact_for_output = contacts_book.add_record(contact)
    return f"You successfully added:\n" \
           f"\t{contact_for_output.prepare_data_for_output()}"


def find_contact(find_string: str, contacts_book: AddressBook) -> str:
    found_contacts = contacts_book.find_record(find_string)
    return f"By the '{find_string}' request bot found contacts :\n" \
           f"\n\tIn name :" \
           f"\n{''.join(found_contacts['by_name']) if len(found_contacts['by_name']) > 0 else 'Nothing found'}\n" \
           f"\n\tIn phone number/numbers :" \
           f"\n{''.join(found_contacts['by_phone']) if len(found_contacts['by_phone']) > 0 else 'Nothing found'}\n" \
           f"\n\tIn email :" \
           f"\n{''.join(found_contacts['by_email']) if len(found_contacts['by_email']) > 0 else 'Nothing found'}\n" \
           f"\n\tIn address/addresses :" \
           f"\n{''.join(found_contacts['by_address']) if len(found_contacts['by_address']) > 0 else 'Nothing found'}\n"


def dir_sort(path_to_dir: str) -> str:
    message = sort_dir(path_to_dir)
    if not message:
        raise InvalidDirectoryPathError
    return message


def show_all(contacts_book: AddressBook) -> str:
    return contacts_book.see_all_contacts()


def delete_contact(name: str, contacts_book: AddressBook) -> str:
    contacts_book.delete_record(name)
    return f"Successfully deleted {name} contact"


def goodbye() -> str:
    return 'Good bye!'


def add_note(
        name: str,
        note: str,
        contacts_book: AddressBook,
        tag: list[str] or list,
) -> str:
    contact = contacts_book.get_record_by_name(name)
    contact_in_record = contacts_book.convert_to_record(contact)
    contact_in_record.add_note(note, contact, tag)
    return f"Successfully added '{note}' to {name} contact"


def delete_note(name: str, note: str, contacts_book: AddressBook) -> str:
    contact = contacts_book.get_record_by_name(name)
    contact_in_record = contacts_book.convert_to_record(contact)
    contact_in_record.delete_note(note, contact)
    return f"You've successfully deleted '{note}' note for the {name} contact"


def see_notes(name: str, contacts_book: AddressBook) -> str:
    contact = contacts_book.get_record_by_name(name)
    contact_in_record = contacts_book.convert_to_record(contact)
    all_notes_by_contact = '\n'.join([str(c_note) for c_note in contact_in_record.note])
    return f"All notes for {name} contact : \n\n" \
           f"{all_notes_by_contact}"


def change_note(
        name: str,
        old_note: str,
        contacts_book: AddressBook,
        new_note: list[str],
) -> str:
    note_to_add = new_note[0]
    contact = contacts_book.get_record_by_name(name)
    contact_in_record = contacts_book.convert_to_record(contact)
    contact_in_record.modify_note(old_note, note_to_add, contact)
    return f"Successfully modified '{old_note}' to '{note_to_add}' for {name} contact"


def add_tag(
        name: str,
        note: str,
        contacts_book: AddressBook,
        tag: list[str],
) -> str:
    tag_to_add = tag[0]
    contact = contacts_book.get_record_by_name(name)
    contact_in_record = contacts_book.convert_to_record(contact)
    contact_in_record.add_tag_to_note(tag_to_add, note, contact)
    return f"Successfully added '{tag_to_add}' to '{note}' of the {name} contact"


def find_notes_with_tag(
        name: str,
        tag: str,
        contacts_book: AddressBook,
        sort_type: Optional[str] = None,
) -> str:
    contact = contacts_book.get_record_by_name(name)
    contact_in_record = contacts_book.convert_to_record(contact)
    found_notes = []
    for note in contact_in_record.note:
        merged_tags = ' '.join([this_tag.value for this_tag in note.tag])
        if tag in merged_tags:
            found_notes.append(note.value)
    if sort_type:
        if sort_type[0] == 'newest':
            found_notes.reverse()
        elif sort_type[0] == 'name':
            found_notes.sort(reverse=True)
        elif sort_type[0] == 'length':
            found_notes.sort(key=len, reverse=False)
    return f"Here are the list of the notes for the " \
           f"{name} contact with '{tag}' tag: \n {' / '.join(found_notes)}"


def search_for_notes(name: str, search_symbols: str, contacts_book: AddressBook) -> str:
    contact = contacts_book.get_record_by_name(name)
    contact_in_record = contacts_book.convert_to_record(contact)
    found_notes = contact_in_record.search_for_notes(search_symbols)
    found_notes = '\n\n' + '\n'.join([str(find_note)
                                      for find_note in found_notes])
    return f"Here are the list of the notes for the " \
           f"{name} contact with '{search_symbols}' symbols: " \
           f"{found_notes}"


def get_birthdays_by_days(days: str, contacts_book: AddressBook) -> str:
    try:
        days = int(days)
    except ValueError:
        raise LiteralsInDaysError
    if days < 0:
        raise ZeroDaysError
    return contacts_book.get_birthdays_by_days(days)


def edit_contact(
        name: str,
        field: str,
        new_value: str,
        contacts_book: AddressBook,
        old_value: Optional[str] = None,
) -> str:
    contact = contacts_book.get_record_by_name(name)
    contact_in_record = contacts_book.convert_to_record(contact)
    if field == 'phone':
        contact_in_record.modify_phone(old_value, new_value, contact)
    elif field == 'birthday':
        contact_in_record.modify_birthday(new_value, contact)
    elif field == 'address':
        contact_in_record.modify_address(old_value, new_value, contact)
    elif field == 'email':
        contact_in_record.modify_email(new_value, contact)
    else:
        raise UnknownFieldError
    return f"Successfully modified {field} from '{old_value}' to '{new_value}' of the {name} contact"


def add_info(
        name: str,
        field: str,
        contacts_book: AddressBook,
        new_value: list[str],
) -> str:
    contact = contacts_book.get_record_by_name(name)
    contact_in_record = contacts_book.convert_to_record(contact)
    if field == 'phone':
        contact_in_record.add_phone(new_value[0], contact)
    elif field == 'address':
        contact_in_record.add_address(new_value[0], contact)
    else:
        raise UnknownFieldError
    return f"Successfully added '{new_value[0]}' to {field} field of the {name} contact"
