from random import choices
from subprocess import run
from time import sleep, time
import argparse

def int_to_bits(num, length=8):
    num = int(num)
    bits = bin(num)[2:].zfill(length)
    return [ int(i) for i in bits ]


patterns = [ int_to_bits(i, 3) for i in reversed(range(8)) ]
def generate_rule(rulenum):
    rule = int_to_bits(rulenum)
    def specific_rule(a,b,c):
        return rule[patterns.index([a,b,c])]
    def next(prev_list):
        return [ specific_rule(
                               prev_list[i-1],
                               prev_list[i],
                               prev_list[(i+1) % len(prev_list)]
                              )
                for i in range(len(prev_list))
                ]
    return next


def init(row_size = 2000):
    parser = argparse.ArgumentParser()
    parser.add_argument('rule', help="automata rule in wolfram notation", type=int)
    parser.add_argument('--init_row', '-i', choices=["?", "l", "m", "r"],
                        help="define initial row")
    args = parser.parse_args()


    height, width = [ int(i) for i in run(["stty", "size"],
                                          capture_output=True,text=True)
                                          .stdout.strip().split(' ') ]
    padding = [ 0 for _ in range(row_size//2) ]
    if args.init_row == "?":
        row = choices((0,1), k=row_size)
        upper = min(len(row)//2 + width//2, len(row))
        lower = max(len(row)//2 - width//2, 0)
    elif args.init_row == "l":
        row = [1] + padding + padding
        upper = min(width, len(row))
        lower = 0
    elif args.init_row == "r":
        row = padding + padding + [1]
        upper = len(row)
        lower = max(len(row) - width, 0)
    else:
    # this makes middle default. surely there is a better way to do all of this
        row = padding + [1] + padding
        upper = min(len(row)//2 + width//2, len(row))
        lower = max(len(row)//2 - width//2, 0)
                        
    return row, upper, lower, args.rule


def main(wait=.0333333333333):
    row, upper, lower, rulenum = init()
    next = generate_rule(rulenum)
    while True:
        start = time()
        print("".join("\033[34m█\033[00m" if i else " " for i in row[lower:upper]))
        row = next(row)
        attempt_framerate = wait - (time()-start)
        if attempt_framerate > 0:
            sleep(attempt_framerate)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
