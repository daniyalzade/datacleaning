TYPES = [
        'bool',
        'enum',
        'str',
        'real',
        ]

EXC_VALUES = [
        'True',
        'False',
        'On',
        'Off',
        'Yes',
        'No',
        ]

"""
Remove the names matching:

o   Set point or possible variants: STPT, ST
o   Alarm or possible variants:  ALM, ALRM
o   Command or CMD
o   Control Temp or CONT
o   Fire
o   Smoke
o   Security
o   These points lists are idiosyncratic and there could be some other abbreviations possible but these are all we could think of so far.
"""

def main():
    define('path', default='/Users/eytan/Downloads/whole_history_repo.csv',
            help='Full path to the file containing the csv',
            )
    define('last_day', default='2013-10-26',
            help='The last day to be used for the analysis',
            )
    define('lookback', default=60, type=int,
            help='The number of days to go back from the last day',
            )
    define('exclude', default=['bool', 'enum', 'str'],
            type=int,
            multiple=True,
            help='The data types to be excluded',
            )
    define('display_points', type=bool,
            help='display the list of points in the data',
            )

    parse_command_line()

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
