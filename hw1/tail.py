import sys


def main(fnames=None):
    if fnames is None:
        lines = sys.stdin.readlines()
        for i, str in enumerate(lines[-17:]):
            print(f'{str.strip('\n')}')
        return 1

    elif len(fnames) == 1:
        fname = fnames[0]
        if not fname[-4:].lower() == '.txt':
            print('not a .txt file')
            return 2
        try:
            with open(fnames[0], 'r') as f:
                lines = f.readlines()
            for i, str in enumerate(lines[-10:]):
                print(f'{str.strip('\n')}')
            return 1
        except:
            print(f'cant read {fname} file')
            return 2

    elif len(fnames) > 1:
        for fname in fnames:
            if not fname[-4:].lower() == '.txt':
                print('not a .txt file')
                return 2
            try:
                with open(fname, 'r') as f:
                    lines = f.readlines()
                print(fname)
                for i, str in enumerate(lines[-10:]):
                    print(f'{str.strip('\n')}')
                print()
            except:
                print(f'cant read {fname} file')
                return 2
        return 1

    else:
        print('forbidden error')
        return 2


if __name__ == '__main__':
    if len(sys.argv) > 2:
        main(sys.argv[1:])
    elif len(sys.argv) == 2:
        main([sys.argv[1]])
    else:
        main()
