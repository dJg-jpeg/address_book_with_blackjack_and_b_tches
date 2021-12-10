from functools import wraps
import handlers
import bot_classes
import re
from typing import List


def input_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            answer = func(*args, **kwargs)
        except bot_classes.ExistContactError:
            return "This contact already exists, " \
                   "if you want to change number please use command change"
        except bot_classes.PhoneError:
            return "Phone number must starts from + " \
                   "and phone must contain only digits" \
                   ", please try again"
        except bot_classes.BirthdayError:
            return "Data must match pattern 'day.month.year', " \
                   "please try again"
        except bot_classes.EmailError:
            return "You are trying to input invalid email address, " \
                   "please try again"
        except bot_classes.InvalidDirectoryPathError:
            return 'It is not a directory , ' \
                   'please insert a valid directory path'
        return answer

    return wrapper


@input_error
def get_handler(contacts: bot_classes.AddressBook, command: str, arguments: List[str] = None) -> str:
    if arguments is None:
        necessary_handler = handlers.COMMANDS[command][0]
        return necessary_handler()
    necessary_handler = handlers.COMMANDS[command]
    if necessary_handler[1] == 'find_commands':
        return necessary_handler[0](arguments[0], contacts)
    elif necessary_handler[1] == 'sort_commands':
        return necessary_handler[0](arguments[0])
    elif necessary_handler[1] == 'contact_commands':
        return necessary_handler[0](parse_user_input(arguments), contacts)


def parse_user_input(raw_contact: list) -> dict:
    parsed_contact = {'name': raw_contact[0],
                      'numbers': [],
                      'birthday': None,
                      'address': [],
                      'email': None,
                      }
    for attribute in raw_contact[1:]:
        if attribute.startswith('+'):
            parsed_contact['numbers'].append(attribute)
        elif '@' in attribute:
            parsed_contact['email'] = attribute
        elif re.search(r'\d{1,4}[.\s\\/]\d{1,4}[.\s\\/]\d{1,4}', attribute) is not None:
            parsed_contact['birthday'] = attribute
        else:
            parsed_contact['address'].append(attribute)
    return parsed_contact


def main() -> None:
    bot_answer = ''
    address_book = bot_classes.AddressBook()
    print('Welcome! '
          'Please separate arguments using the , character.\n'
          'For example : \n add \n name , phones, birthday\n')
    while bot_answer != 'Good bye!':
        command = ((input("Input command :")).lower()).strip()
        try:
            args_for_command = handlers.COMMAND_ARGS[command]
        except KeyError:
            print("I don't know such command, please try again(")
            continue
        if args_for_command is not None:
            user_args = (input(f"Input {args_for_command} :")).split(',')
            user_args = [arg.strip() for arg in user_args]
            bot_answer = get_handler(address_book, command, user_args)
        else:
            bot_answer = get_handler(address_book, command)
        print(bot_answer)


if __name__ == '__main__':
    main()