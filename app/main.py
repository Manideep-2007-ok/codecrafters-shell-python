import sys


def main():
    builtins = ["echo","exit","type"]
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        try:
            command = input()
        except EOFError:
            break
        if command == "exit" or command == "exit0":
            sys.exit(0)
        elif command.startswith("echo "):
            message = command[5:]
            print(message)
        elif command.startswith("type "):
            target_command = command[5:]
            if target_command in builtins:
                print(f"{target_command} is a shell builtin")
            else:
                print(f"{target_command} not found")
        else:
            print(f"{command}: command not found")
        
        
if __name__ == "__main__":
    main()
