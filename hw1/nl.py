import sys


def main(fname=None):

    if fname is None:
        lines = sys.stdin.readlines()
    elif fname[-4:].lower() == '.txt':
        lines = []
        try:
            with open(fname, 'r') as f:
                lines = f.readlines()
        except:
            print('file not found')
            return 2
    else:
        print('not a .txt file')
        return 2

    for i, str in enumerate(lines):
        print(f'{i+1}  {str.strip('\n')}')

    return 1


if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        main()
