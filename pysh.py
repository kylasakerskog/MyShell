import os
import sys

def cd(args):
    if len(args) > 1:
        try:
            os.chdir(args[1])
        except:
            sys.stderr.write('-pysh: cd: no such file or directory: ' + args[1] + '\n')
            
    else:
        os.chdir(os.environ['HOME'])

def is_built_in(args):
    ret = True
    if args[0] == 'cd':
        cd(args)
    elif args[0] == 'exit':
        sys.exit()
    else:
        ret = False
    return ret

if __name__ == "__main__":
    while True:
        sys.stderr.write('mysh$ ')
        cmd = input()
        args = cmd.split()

        if is_built_in(args):
            continue
        
        # parent_pid =  os.getpid()
        child_pid = os.fork()

        # os.fork()は子プロセスのときは0, それ以外はchild_pidを返す
        if child_pid == 0:
            try:
                os.execvp(args[0], args)
            except:
                sys.stderr.write('-pysh: command not found: ' + args[0] + '\n')
        else:
            os.waitpid(child_pid, 0)
                
