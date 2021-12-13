import bot_classes
from typing import Optional
import dir_sorter


def greetings() -> str:
    return f"Hi!\n" \
           f"My list of commands is : {', '.join(list(COMMANDS.keys()))}\n" \
           f"How can I help you?"


def add_contact(contact: dict, contacts_book: bot_classes.AddressBook) -> Optional[str]:
    if contact['name'] in contacts_book.keys():
        raise bot_classes.ExistContactError
    contacts_book.add_record(contact)
    return f"You successfully added {contact['name']} contact " \
           f"with {','.join(contact['numbers'])} numbers, " \
           f"{contact['birthday']} birthday, " \
           f"{','.join(contact['address'])} address, " \
           f"{contact['email']} email"


def find_contact(find_string: str, contacts_book: bot_classes.AddressBook) -> str:
    findings = contacts_book.find_record(find_string)
    return f"By the '{find_string}' request bot founded contacts :\n" \
           f"\n\tIn name :" \
           f"\n\n{''.join(findings['by_name']) if len(findings['by_name']) > 0 else 'Nothing found'}\n" \
           f"\n\tIn phone number/numbers :" \
           f"\n\n{''.join(findings['by_phone']) if len(findings['by_phone']) > 0 else 'Nothing found'}\n" \
           f"\n\tIn email :" \
           f"\n\n{''.join(findings['by_email']) if len(findings['by_email']) > 0 else 'Nothing found'}\n" \
           f"\n\tIn address/addresses :" \
           f"\n\n{''.join(findings['by_address']) if len(findings['by_address']) > 0 else 'Nothing found'}\n"


def dir_sort(path_to_dir: str) -> str:
    return dir_sorter.sort_dir(path_to_dir)


def show_all(contacts_book: bot_classes.AddressBook) -> str:
    return contacts_book.see_all_contacts()


def delete_contact(name: str, contacts_book: bot_classes.AddressBook) -> str:
    contacts_book.delete_record(name)
    return f"Successfully deleted {name} contact"


def goodbye() -> str:

    return 'Good bye!'


def add_note(name: str, note: str, tag: str, contacts_book: bot_classes.AddressBook) -> str:
    contact = contacts_book.get_record_by_name(name)
    contact.add_note(note, tag)
    return f"Successfully added '{note}' to {contact['name']} contact"


def delete_note(name: str, note: str, contacts_book: bot_classes.AddressBook) -> str:
    contact = contacts_book.get_record_by_name(name)
    contact.delete_note(note)
    return f"You've successfully deleted '{note}' note for the {contact['name']} contact"


def find_note(name: str, note: str, contacts_book: bot_classes.AddressBook) -> Optional[bot_classes.Note]:
    contact = contacts_book.get_record_by_name(name)
    found_note = contact.get_note(note)
    return found_note


def change_note(name: str, note: str, new_note: str, contacts_book: bot_classes.AddressBook) -> str:
    contact = contacts_book.get_record_by_name(name)
    contact.modify_note(note, new_note)
    return f"Successfully modified '{note}' to '{new_note}' for {contact['name']} contact"


def add_tag(name: str, note: str, tag: str, contacts_book: bot_classes.AddressBook) -> str:
    contact = contacts_book.get_record_by_name(name)
    note = contact.get_note(note)
    note.add_tag(tag)
    return f"Successfully added '{tag}' to '{note}' of the {contact['name']}contact"


def find_notes_with_tag(name: str, tag: str, contacts_book: bot_classes.AddressBook) -> str:
    contact = contacts_book.get_record_by_name(name)
    notes = list(contact.note.values())
    found_notes = []
    for note in notes:
        merged_tags = ' '.join([p.value for p in note.tag])
        if tag in merged_tags:
            found_notes.add(note)
    return f"Here are the list of the notes for the {contact['name']} contact with '{tag}' tag: {found_notes}"


def search_notes(name: str, search_symbols: str, contacts_book: bot_classes.AddressBook) -> str:
    contact = contacts_book.get_record_by_name(name)
    found_notes = contact.search_for_notes(search_symbols)
    return f"Here are the list of the notes for the {contact['name']} contact with '{search_symbols}' symbols: {found_notes}"


def get_birthdays_list(days: str, contacts_book: bot_classes.AddressBook) -> str:
    try:
        days = int(days)
    except ValueError:
        raise bot_classes.LiteralsInDaysError
    if days < 0:
        raise bot_classes.ZeroDaysError
    return contacts_book.birthday_list(days)


COMMANDS = {
    'hello': [greetings, 'none_argument_commands'],
    'help': [greetings, 'none_argument_commands'],
    'add_contact': [add_contact, 'contact_commands'],
    'find_contact': [find_contact, 'one_argument_book_commands'],
    'delete_contact': [delete_contact, 'one_argument_book_commands'],
    'birthdays_from_now': [get_birthdays_list, 'one_argument_book_commands'],
    'sort_dir': [dir_sort, 'sort_commands'],
    'show_all': [show_all, 'only_book_commands'],
    'goodbye': [goodbye, 'none_argument_commands'],
    'exit': [goodbye, 'none_argument_commands'],
    'close': [goodbye, 'none_argument_commands'],
    'add_note': [add_note, '3args_note_commands'],
    'delete_note': [delete_note, '2args_note_commands'],
    'find_note': [find_note, '2args_note_commands'],
    'add_tag': [add_note, '3args_note_commands'],
    'find_notes_with_tag': [find_notes_with_tag, '2args_note_commands'],
    'change_note': [change_note, '3args_note_commands'],
    'search_notes': [search_notes, '2args_note_commands'],
}

COMMAND_ARGS = {
    'hello': None,
    'help': None,
    'add_contact': 'name, '
                   'phone number/numbers(optional), '
                   'birthday(optional), '
                   'address/addresses(optional), '
                   'email(optional) separating them by ,',
    'find_contact': 'find request',
    'sort_dir': 'path to directory you want to sort',
    'delete_contact': 'name of the contact you want to delete',
    'birthdays_from_now': 'how many days from now would you like to lookup birthdays for?',
    'show_all': None,
    'goodbye': None,
    'exit': None,
    'close': None,
    'add_note': 'name of the contact, note, tag',
    'delete_note': 'name of the contact, note',
    'find_note': 'name of the contact, note',
    'add_tag': 'name of the contact, note, tag to add',
    'find_notes_with_tag': 'name of the contact, tag',
    'change_note': 'name of the contact, note, new note',
    'search_notes': 'name of the contact, searched symbols',
}
