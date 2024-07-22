import shlex


class input_parser :

    def init_validation(self, raw_string):
        try:
            # Split the input string, respecting quoted substrings
            parts = shlex.split(raw_string)

            if not parts:
                return "Empty input"

            command = parts[0].lower()

            if command == 'l':
                return self.validate_list_command(parts[1:])
            elif command == 'a':
                return self.validate_add_command(parts[1:])
            elif command == 'd':
                return self.validate_delete_command(parts[1:])
            else:
                return f"Unknown command: {command}"

        except ValueError as e:
            return f"Error parsing input: {str(e)}"

    def validate_list_command(self, args):

        i = 0
        order = None
        while i < len(args):
            if args[i] == '-v':
                i += 1
                continue
            elif args[i] in ['-t', '-d', '-a']:
                if i + 1 >= len(args):
                    return f"Missing argument for {args[i]} switch"
                i += 1
            elif args[i] in ['-la', '-ld']:
                if order:
                    return "Cannot specify both -la and -ld"
                order = args[i][1:]
            else:
                return f"Unknown switch: {args[i]}"
            i += 1

        return None

    def parse(self, input_str: str):
        """splits the input string and populates the commands list"""

        raw_commands = input_str.strip().split()

        instruction = raw_commands[0].lower()
        switches = raw_commands[1:]

        return instruction, switches


    def validate_add_command(self, args):
        if len(args) != 1:
            return "Invalid 'a' command format. Use 'a -p' or 'a -m'"

        if args[0] not in ['-p', '-m']:
            return "Invalid 'a' command format. Use 'a -p' or 'a -m'"

        return None

    def validate_delete_command(self, args):
        if len(args) != 2 or args[0] != '-p':
            return "Invalid 'd' command format. Use 'd -p <person_name>'"

        return None


validator = input_parser()
