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

EXC_NAMES = [
        # Set point or possible variants: STPT, ST
        'Set Point',
        'STPT',
        'ST',
        # Alarm or possible variants:  ALM, ALRM
        'ALM',
        'ALRM',
        'Alarm',
        # Command or CMD
        'Command',
        'CMD',
        # Control Temp or CONT
        'CONT',
        'Control Temp',
        'Fire',
        'Smoke',
        'Security',
        ]

def _exclude_name(name):
    """
    @param name: str
    @return: bool
    """
    for exc in EXC_NAMES:
        if exc.lower() in name:
            return True
    return False

def _interpolate(points, point_type, name, interval):
    """
    @param points: list(int)
    @param point_type: str
    @param name: str
    @param interval: int
    @return: list(int)
    """
    raise NotImplementedError

def _parse_point(lines, start=None, end=None):
    """
    @param lines: list(str)
    @param start: datetime
    @param end: datetime
    @return: (dict, list(datetime), list(float))

    {
    'name': str,
    'point_type': str,
    'start': datetime,
    'end': datetime,
    'frequency': int,
    'url': str,
    }
    """
    print lines

def _should_ignore(point, exclude):
    """
    @param point: (dict, list, list)
    @param exclude: list(str)
    @return: bool
    """
    if _exclude_name(point[0]['name']):
        return True
    if point[0]['point_type'] in exclude:
        return True
    if not point[0]['frequency'] in [5, 10, 15]:
        return True
    if not any(map(lambda v: v in EXC_VALUES), point[2]):
        return True
    return False

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
    define('limit', type=int)

    parse_command_line()

    foo = open(options.path)
    lines = []
    points = []
    for idx, line in enumerate(foo.readlines()):
        if len(lines) == 3:
            point = _parse_point(lines)
            if _should_ignore(point):
                continue
            lines = []
            points.append(point)
        else:
            lines.append(line)
        if idx / 3 >= options.limit:
            break
    print "number of points for analysis %s" % len(points)

if __name__ == "__main__":
    from cmdline import define
    from cmdline import options
    from cmdline import parse_command_line
    exit(main())
