from src.command import listCommand, addCommand
from src.utils.input_parser import validator
from src.utils.logger_setup import loggerCursor
from src.utils.db_conn import DbConn
import signal


def create_command(command_type, switches):
    """
    A function to create the command
    """

    if command_type == 'l':
        verbose = '-v' in switches
        if '-t' in switches:
            element = switches[switches.index('-t') + 1]
            title_regex = element
        else:
            title_regex = None
        if '-d' in switches:
            element = switches[switches.index('-d') + 1]
            director_regex = element
        else:
            director_regex = None
        if '-a' in switches:
            element = switches[switches.index('-a') + 1]
            actor_regex = element
        else:
            actor_regex = None
        list_asc = '-la' in switches
        list_desc = '-ld' in switches

        return listCommand.ListCommand(verbose=verbose,
                                   title_regex=title_regex,
                                   director_regex=director_regex,
                                   actor_regex=actor_regex,
                                   list_asc=list_asc,
                                   list_desc=list_desc)

    elif command_type == 'a':

        return addCommand.AddCommand(person='-p' in switches, movie='-m' in switches)
    elif command_type == 'd':
        # Add deleteCommand here later
        return None
    else:

        return None


def signal_handler(sig, frame):
    loggerCursor.info("\nProcess terminated by user.")
    exit(0)


def main():
    signal.signal(signal.SIGINT, signal_handler)

    loggerCursor.info('Waiting for instructions...')
    while True:
        try:
            input_data = input()

            error = validator.init_validation(input_data)
            if error:
                loggerCursor.error(error)
                continue

            loggerCursor.debug(f'Instruction received: {input_data}')
            instruction, switches = validator.parse(input_data)
            command = create_command(instruction, switches)
            command()
        except EOFError:
            break


if __name__ == '__main__':

    main()
