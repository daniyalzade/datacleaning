SAMPLE_DATE = '2013-10-19 04:11:00'
SAMPLE_HEADERS = '%24301_points_High_History/,{http://obix.org/ns/schema/1.0}real,2013-10-19 03:21:00,2013-10-25 03:21:00,8640,0:01:00,http://Callida:Callida123@38.100.73.133/obix/histories/Pennzoil_WebSup/%24301_points_High_History/~historyQuery?start=2013-01-01T00:00:00.000-23:59&end=2013-10-25T08:21:47.565-23:59'

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

def _interpolate(points, point_type, name, interval):
    """
    @param points: list(int)
    @param point_type: str
    @param name: str
    @param interval: int
    @return: list(int)
    """
    raise NotImplementedError

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
    define('prediction_point',
            default='Total Real Power',
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
