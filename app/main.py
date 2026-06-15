import sys
import os
import subprocess
def main():
    builtins = ["echo","exit","type"]
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        try:
            command = input().strip()
            if not command:
                continue
        except EOFError:
            break
        if command == "exit" or command == "exit 0":
            sys.exit(0)
        elif command.startswith("echo "):
            message = command[5:]
            print(message)
        elif command.startswith("type "):
            target_command = command[5:].strip()
            if target_command in builtins:
                print(f"{target_command} is a shell builtin")
            else:
                path_env = os.environ.get("PATH","")
                paths = path_env.split(os.pathsep)
                found = False
                for path_dir in paths:
                    full_path = os.path.join(path_dir,target_command)
                    if os.path.isfile(full_path) and os.access(full_path,os.X_OK):
                        print(f"{target_command} is {full_path}")
                        found = True
                        break
                if not found:
                    print(f"{target_command}: not found")
        else:
            args = command.split()
            program_name = args[0]
            path_env = os.environ.get("PATH","")
            paths = path_env.split(os.pathsep)
            found_path = None
            for path_dir in paths:
                full_path = os.path.join(path_dir,program_name)
                if os.path.isfile(full_path) and os.access(full_path,os.X_OK):
                    found_path = full_path
                    break
                if found_path:
                    args[0] = found_path
                    subprocess.run(args)
                else:
                    print(f"{program_name}: not found")
        
        
if __name__ == "__main__":
    main()
