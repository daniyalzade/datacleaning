def main():
    define('path', default='/Users/eytan/Downloads/whole_history_repo.csv')

    foo = open(options.path)
    for idx, line in enumerate(foo.readlines()):
        if 'NT_DD_East_10_06_CD' in line:
            print line

        if not idx % 3 - 2:
            print line
        if idx > 1000:
            break

if __name__ == "__main__":
    from cmdline import define
    from cmdline import options
    from cmdline import parse_command_line
    exit(main())
