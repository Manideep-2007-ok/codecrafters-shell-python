import sys
import os
import subprocess
def parse_arguments(cmd_arg):
    args = []
    current_arg = []
    in_single_quotes = False
    in_double_quotes = False
    is_escaping = False
    for char in cmd_arg:
        if is_escaping:
            if in_double_quotes:
                if char in ['"','\\','$','`','\n']:
                    current_arg.append(char)
                else:
                    current_arg.append('\\')
                    current_arg.append(char)
            else:
                current_arg.append(char)
            is_escaping = False
        elif char == "\\" and not in_single_quotes:
            is_escaping = True
        elif char == "'" and not in_double_quotes:
            in_single_quotes = not in_single_quotes
        elif char == '"' and not in_single_quotes:
            in_double_quotes = not in_double_quotes
        elif char.isspace() and not in_single_quotes and not in_double_quotes:
            if current_arg:
                args.append("".join(current_arg))
                current_arg = []
        else:
            current_arg.append(char)
    if current_arg:
        args.append("".join(current_arg))
    return args
def main():
    builtins = ["echo","exit","type","pwd","cd","jobs"]
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        try:
            command = input().strip()
            if not command:
                continue
        except EOFError:
            break
        args = parse_arguments(command)
        if not args:
            continue
        redirect_stdout = None
        redirect_stderr = None
        mode_stdout = "w"
        mode_stderr = "w"
        if "2>" in args:
            idx = args.index("2>")
            redirect_stderr = args[idx+1]
            args = args[:idx]+args[idx+2:]
        if "2>>" in args:
            idx = args.index("2>>")
            redirect_stderr = args[idx+1]
            args = args[:idx]+args[idx+2:]
            mode_stderr = "a"
        if ">>" in args:
            idx = args.index(">>")
            redirect_stdout = args[idx+1]
            args = args[:idx]+args[idx+2:]
            mode_stdout = "a"
        if "1>>" in args:
            idx = args.index("1>>")
            redirect_stdout = args[idx+1]
            args = args[:idx]+args[idx+2:]
            mode_stdout = "a"
        if ">" in args:
            idx = args.index(">")
            redirect_stdout = args[idx+1]
            args = args[:idx]+args[idx+2:]
        if "1>" in args:
            idx = args.index("1>")
            redirect_stdout = args[idx+1]
            args = args[:idx]+args[idx+2:]
        out_fp = open(redirect_stdout,mode_stdout) if redirect_stdout else sys.stdout
        err_fp = open(redirect_stderr,mode_stderr) if redirect_stderr else sys.stderr
        cmd = args[0]
        if cmd == "exit" or cmd == "exit 0":
            if redirect_stdout:
                out_fp.close()
            if redirect_stderr:
                err_fp.close()
            sys.exit(0)
        elif cmd=="echo":
            print(" ".join(args[1:]), file=out_fp)
        elif cmd=="type":
            if len(args)>1:
                target_command = args[1]
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
        elif cmd == "pwd":
            print(os.getcwd())
        elif cmd=="cd":
            if len(args)>1:
                directory = args[1]
                if directory == "~":
                    directory = os.environ.get("HOME","")
                if os.path.exists(directory):
                    os.chdir(directory)
                else:
                    print(f"cd: {directory}: No such file or directory", file=err_fp)
        elif cmd == "jobs":
            pass
        else:
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
                subprocess.run(args, executable=found_path, stdout = out_fp, stderr = err_fp)
            else:
                print(f"{program_name}: command not found")
        if redirect_stdout:
            out_fp.close()
        if redirect_stderr:
            err_fp.close()
        
if __name__ == "__main__":
    main()
