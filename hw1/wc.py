import sys


def main(fnames=None):
    if fnames is None:
        lines = sys.stdin.readlines()
        strs, words, bytes = get_stats(' '.join(lines))
        print(f'{strs}  {words}  {bytes}')
        return 1

    elif len(fnames) == 1:
        fname = fnames[0]
        try:
            with open(fname, 'r') as f:
                lines = f.readlines()
                strs, words, bytes = get_stats(' '.join(lines))
            print(f'{strs}  {words}  {bytes}  {fname}')
            return 1
        except:
            print(f'cant read {fname} file')
            return 2

    elif len(fnames) >= 1:
        ts, tw, tb = 0, 0, 0
        for fname in fnames:
            try:
                with open(fname, 'r') as f:
                    lines = f.readlines()
                    strs, words, bytes = get_stats(' '.join(lines))
                print(f'{strs}  {words}  {bytes}  {fname}')
                ts += strs
                tw += words
                tb += bytes
            except:
                print(f'cant read {fname} file')
                return 2
        print(f'{ts}  {tw}  {tb}')
        return 1

    else:
        print('forbidden error')
        return 2


def get_stats(text):
    strs = len(text.split('\n'))
    words = len(text.split(' '))
    bytes = len(text.encode('utf-8'))
    return strs, words, bytes


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        main(sys.argv[1:])
    else:
        main()
