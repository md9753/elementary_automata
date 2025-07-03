from random import choices
from sys import argv
from subprocess import run
from time import sleep
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('rule', nargs=1, help="automata rule in wolfram notation", type=int)
parser.add_argument('--init_row', '-i', choices=["?", "l", "m", "r"],
                    help="define initial row")
args = parser.parse_args()


height, width = [ int(i) for i in run(["stty", "size"],
                                      capture_output=True,text=True)
                                      .stdout.strip().split(' ') ]


def int_to_bits(num, length=8):
    num = int(num)
    bits = list(f"{num:0>{length}b}".format(num))
    return [ int(i) for i in bits ]


patterns = [ int_to_bits(i, 3) for i in reversed(range(8)) ]
def genericrule(rulenum, a,b,c):
    rule = int_to_bits(rulenum)
    return rule[patterns.index([a,b,c])]


def next(prev):
    return [ genericrule(argv[1], prev[i-1], prev[i], prev[(i+1) % len(prev)])
        for i in range(len(prev)) ]


def init(row_size = 2000):
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
                        
    return row, upper, lower


def main(wait=.0333333333):
    row, upper, lower = init()
    while True:
        print("".join("\033[34m█\033[00m" if i else " " for i in row[lower:upper]))
        row = next(row)
        sleep(float(wait))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
