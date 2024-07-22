

class input_parser :

    def __init__(self):
        self.commands = {}
        self.allowed_instruction = ['a', 'l']
        self.allowed_switches = ['-v', '-t', '-d', '-a', ]

    def init_validation(self, raw_string):
        """Validates the command string against a regex expression"""
        pass

    def parse(self, input_str: str):
        """splits the input string and populates the commands list"""

        raw_commands = input_str.strip().split()

        for token in raw_commands:
            if token
