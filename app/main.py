import sys


def main():
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
        print(f"{command}: command not found")
        
        
if __name__ == "__main__":
    main()
