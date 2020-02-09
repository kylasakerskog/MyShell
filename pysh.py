import os
import sys

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

def split_proc(in_args):
    # パイプを分割する処理
    in_piped = []
    elements = []
    skippable = False
    redir_in = ''
    redir_out = ''
    redir_out_add = ''
    counts = 0
    
    for i, el in enumerate(in_args):
        if skippable == True:
            skippable = False
            # continue
        elif el in ['<', '>', '>>']:
            if (i+1) < len(in_args):
                skippable = True
                if el == '<':
                    redir_in = in_args[i+1]
                    sys.stderr.write('redir_in: ' + redir_in + '\n')
                elif el == '>':
                    redir_out = in_args[i+1]
                    sys.stderr.write('redir_out: ' + redir_out + '\n')
                else:
                    redir_out_add = in_args[i+1]
                    sys.stderr.write('redir_out_add: ' + redir_out_add + '\n')
            else:
                sys.stderr.write('-pysh: syntax error: ' + in_args[i] + '\n')
                continue
        elif el == '|':
            in_piped.append(elements)
            sys.stderr.write('element' + str(counts) + ' : '  + str(in_piped[counts]) + '\n\n')
            counts += 1
            elements = []
        else:
            elements.append(el)

    if elements != []:
        in_piped.append(elements)
        sys.stderr.write('element' + str(counts) + ' : '  + str(in_piped[counts]) + '\n\n')
                
            
if __name__ == "__main__":
    while True:
        sys.stderr.write('mysh$ ')
        cmd = input()
        args = cmd.split()

        split_proc(args)
        """
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
                
        """
