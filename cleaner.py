import re
from datetime import datetime
from datetime import timedelta
import logging

DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
DATE_FORMAT = '%Y-%m-%d'
SAMPLE_DATE = '2013-10-19 04:11:00'
SAMPLE_HEADERS = '%24301_points_High_History/,{http://obix.org/ns/schema/1.0}real,2013-10-19 03:21:00,2013-10-25 03:21:00,8640,0:01:00,http://Callida:Callida123@38.100.73.133/obix/histories/Pennzoil_WebSup/%24301_points_High_History/~historyQuery?start=2013-01-01T00:00:00.000-23:59&end=2013-10-25T08:21:47.565-23:59'
OPITIMAL_FREQUENCY = 10

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

class ShouldIngore(Exception):
    pass

class NoPointFound(Exception):
    pass

def _exclude_name(name):
    """
    @param name: str
    @return: bool
    """
    for exc in EXC_NAMES:
        if exc.lower() in name:
            return True
    return False

def _truncate(point, start, end):
    """
    @param point: Point
    @param start: datetime
    @param end: datetime
    @return: Point

    return all the dates and values in between start, end
    """
    dict_, dates, values = point
    date_and_values = [(d, v) for d, v in zip(dates, values) if start < d < end]
    if not date_and_values:
        raise NoPointFound
    truncated_date, truncated_values = map(list, zip(*date_and_values))
    return dict_, truncated_date, truncated_values

def _interpolate(*point):
    """
    At this point, we assume that all the point has been truncated to the
    proper start / end times.

    @param point: (dict, list, list)
    @return: Point
    """
    dict_, dates, values = point
    frequency = dict_.get('frequency')
    if frequency == 10:
        return point
    if frequency == 5:
        return dict_, dates[0::2], values[0::2]
    elif frequency == 15:
        #0,   15,   30,  45, (timestamps we have)
        #  10,   20,  40,    (timesamps to predict)
        import pdb; pdb.set_trace()
        new_dates, new_values = dates[0], values[0]
        x = [1/3., 2/3.]
        for idx, (date, value) in enumerate(zip(dates, values)[1:], 1):
            is_even = idx % 2 == 0
            if is_even:
                new_dates.append(date)
                new_values.append(value)
            previous_value = new_values[idx-1]
            predicted_value = (previous_value * x[is_even] + value * x[is_even-1])/2.
            new_dates.append(date - timedelta(minutes=10))
            new_values.append(predicted_value)
        return dict_, new_dates, new_values

def _convert_datetime(date_str):
    try:
        return datetime.strptime(date_str, DATE_TIME_FORMAT)
    except Exception:
        return datetime.strptime(date_str, DATE_FORMAT)

def _get_point_type(point_type):
    for type in TYPES:
        if type in point_type:
            return type
    raise ValueError

def _get_frequency(frequency):
    """
    @param frequency: str
    @return: int

    0:01:00 -> 1
    """
    return int(frequency.split(':')[1])

def _get_header_dates_and_values(lines):
    """
    @param lines: list(str)
    @return: (dict(headers), list(datetime), list(float))
    """
    headers, dates, values = map(lambda x: re.split(r'(?:\s*,\s*|\n)', x)[:-1],
                                 lines)
    try:
        values = map(float, values)
    except Exception:
        if options.debug:
            print ("ingoring due to wrong type: %s" % values[0])
        raise ShouldIngore
    dates = map(_convert_datetime, dates)
    return headers, dates, values

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
    header, dates, values = _get_header_dates_and_values(lines)
    name, point_type, start_date, end_date, _, frequency, url = header
    point_type = _get_point_type(point_type)
    frequency = _get_frequency(frequency)
    dict_ = {
            'name': name,
            'point_type': point_type,
            'start': _convert_datetime(start_date),
            'end': _convert_datetime(end_date),
            'frequency': frequency,
            'url': url,
    }
    return (dict_, dates, values)

def _should_ignore(point, exclude):
    """
    @param point: (dict, list, list)
    @param exclude: list(str)
    @return: bool
    """
    name = point[0]['name']
    point_type = point[0]['point_type']
    frequency = point[0]['frequency']
    if _exclude_name(name):
        if options.debug: print ("ignoring due to name %s" % name)
        return True
    if point_type in exclude:
        if options.debug: print ("ignoring due to type %s" % point_type)
        return True
    if not point[0]['frequency'] in [5, 10, 15]:
        if options.debug: print ("ignoring due to frequency %s" % frequency)
        return True
    return False

def main():
    define('path', default='/Users/eytan/Downloads/whole_history_repo.csv',
            help='Full path to the file containing the csv',
            )
    define('output', default='output.csv')
    define('end', default='2013-10-26',
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
    define('display_point', type=str,
            help='display data about this particular point',
            )
    define('display_date_range', type=bool,
            help='display the first and last values recorded',
            )
    define('prediction_point',
            default='Total Real Power',
            )
    define('limit', type=int)
    define('debug', type=bool)

    parse_command_line()
    end = _convert_datetime(options.end)
    start = end - timedelta(days=options.lookback)

    file_to_read = open(options.path)
    lines = []
    points = []
    for idx, line in enumerate(file_to_read.readlines()):
        if idx / 3 >= options.limit:
            break
        lines.append(line)
        if len(lines) == 3:
            try:
                point = _parse_point(lines)
            except ShouldIngore:
                continue
            finally:
                lines = []
            if _should_ignore(point, options.exclude):
                continue
            points.append(point)
    print "number of points for analysis %s" % len(points)

    names = [p[0]['name'] for p in points]
    if options.display_point:
        for p in points:
            if p[0]['name'] == options.display_point:
                print p[0]
        return
    if options.display_points:
        import pprint
        pprint.pprint(names)
        return
    if options.display_date_range:
        start = min([p[0]['start'] for p in points])
        end = max([p[0]['end'] for p in points])
        print "data recorded from %s to %s" % (start, end)
        return
    try:
        points = [_truncate(p, start, end) for p in points]
        points = [_interpolate(p, start, end) for p in points]
    except NoPointFound:
        if options.debug:
            print "No points found, try increase --lookback={int}"
        return
    header = ','.join(['date'] + names)
    num_values = len(points[0][0])
    print header
    for idx in range(num_values):
        ts = points[0][1][idx]
        row = [ts]
        for point in points:
            row.append(point[0][2][idx])
        msg = ','.join([str(r) for r in row])
        print msg


if __name__ == "__main__":
    from cmdline import define
    from cmdline import options
    from cmdline import parse_command_line
    exit(main())
