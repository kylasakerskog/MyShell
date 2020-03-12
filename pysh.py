import os
import sys
import signal

def cd(args):
    # cdコマンドの実装
    if len(args) > 1:
        try:
            os.chdir(args[1])
        except:
            sys.stderr.write('-pysh: cd: no such file or directory: ' + args[1] + '\n')
            
    else:
        os.chdir(os.environ['HOME'])

def is_built_in(args):
    # ビルトインコマンド(cd, exit)の実装
    ret = True
    if args[0] == 'cd':
        cd(args)
    elif args[0] == 'exit':
        sys.exit()
    else:
        ret = False
    return ret

def exec_proc(in_args):
    # パイプを分割する処理
    # ls > a.txt > b.txt >> c.txt などを許容しない
    # ls | cat < a.txt を許容しない
    elements = []
    skippable = False
    redir_in = ''
    redir_out = ''
    redir_out_add = ''
    pfd = []
    pipes = 0
    bg_flag = 0
    
    for i, el in enumerate(in_args):
        if skippable == True:
            skippable = False
        elif el in ['<', '>', '>>']:
            if (i+1) < len(in_args):
                skippable = True
                if el == '<':
                    redir_in = in_args[i+1]
                    # sys.stderr.write('redir_in: ' + redir_in + '\n')
                elif el == '>':
                    redir_out = in_args[i+1]
                    # sys.stderr.write('redir_out: ' + redir_out + '\n')
                else:
                    redir_out_add = in_args[i+1]
                    # sys.stderr.write('redir_out_add: ' + redir_out_add + '\n')
            else:
                sys.stderr.write('-pysh: syntax error: ' + in_args[i] + '\n')
                
        elif el == '|':
            pfd[pipes] = os.pipe()
            child_pid = os.fork()
            if child_pid == 0:
                with open(pfd[pipes][0], 'w') as out_file:
                    pfd[pipes][0] = out_file.fileno()
                    os.dup2(pfd[pipes][0], 1)
                with open(pfd[pipes][1], 'r') as in_file:
                    pfd[pipes][1] = in_file.fileno()
                    os.dup2(pfd[pipes][1], 0)
                if redir_in != '':
                    with open(redir_in, 'r') as in_file:
                        fd = in_file.fileno()
                        os.dup2(fd, 0)
                if redir_out != '':
                    with open(redir_out, 'w') as out_file:
                        fd = out_file.fileno()
                        os.dup2(fd, 1)
                if redir_out_add != '':
                    with open(redir_out_add, 'a') as out_file:
                        fd = out_file.fileno()
                        os.dup2(fd, 1)
                try:
                    os.execvp(elements[0], elements)
                    elements = []
                    redir_in = ''
                    redir_out = ''
                    redir_out_add = ''
                except:
                    sys.stderr.write('-pysh: command not found: ' + args[0] + '\n')
            else:
                os.waitpid(child_pid, 0)
            
            pipes += 1

        else:
            elements.append(el)
        
    if elements != []:
        child_pid = os.fork()
        if child_pid == 0:
            if redir_in != '':
                with open(redir_in, 'r') as in_file:
                    fd = in_file.fileno()
                    os.dup2(fd, 0)
            if redir_out != '':
                with open(redir_out, 'w') as out_file:
                    fd = out_file.fileno()
                    os.dup2(fd, 1)
            if redir_out_add != '':
                with open(redir_out_add, 'a') as out_file:
                    fd = out_file.fileno()
                    os.dup2(fd, 1)
            try:
                os.execvp(elements[0], elements)
                elements = []
                redir_in = ''
                redir_out = ''
                redir_out_add = ''
            except:
                sys.stderr.write('-pysh: command not found: ' + args[0] + '\n')
        else:
            os.waitpid(child_pid, 0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    signal.signal(signal.SIGTSTP, signal.SIG_IGN)
    
    while True:
        sys.stderr.write('mysh$ ')
        cmd = input()
        args = cmd.split()

        if is_built_in(args):
            continue

        # parent_pid =  os.getpid()
        exec_proc(args)
