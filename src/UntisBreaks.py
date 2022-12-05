import datetime
import webuntis


def _group_by_start(break_superv: list) -> dict:
    result = {}
    for bs in break_superv:
        if bs.start not in result.keys():
            result[bs.start] = []
        result[bs.start].append(bs)
    return result


def _supervisions_from_day(session: webuntis.Session, offset_to_current_day) -> set:
    all_supervisions = set()
    today = datetime.datetime.today()
    current_day = datetime.datetime(today.year,today.month,today.day) + datetime.timedelta(days=offset_to_current_day)
    for teacher in session.teachers():
        break_superv = session.timetable(teacher=teacher.id, start=current_day, end=current_day).filter(type='bs')
        for bs in break_superv:
            all_supervisions.add(bs)
    return all_supervisions


'''
@param session: containing server, username, password, school and useragent information
@param offset: examples: 0 => today  |  1 => tomorrow  |  -1 => yesterday
@return dict-keys: datetime (always from current day) / dict-values: list of all break-supervisions (webuntis.objects.PeriodObject)
'''
def get_offset_supervisions(session: webuntis.Session, offset: int) -> dict:
    supervisions = _supervisions_from_day(session, offset)
    return _group_by_start(supervisions)


'''
@param session: containing server, username, password, school and useragent information
@return dict-keys: datetime (always from current day) / dict-values: list of all break-supervisions (webuntis.objects.PeriodObject)
'''
def get_todays_supervisions(session: webuntis.Session) -> dict:
    return get_offset_supervisions(session, 0)


'''
@param datetime_options: all breaks in question, usually invoked with data.keys() from data=get_todays_supervisions(session)
@return next break considering local time. If there is no upcoming break-datetime, this method returns the last available break
'''
def next_break_time(datetime_options: list[datetime.datetime], current:datetime.datetime=None) -> datetime.datetime:
    if not datetime_options:
        return None
    current = current if current else datetime.datetime.now()
    sorted_dates = sorted(list(datetime_options)+[current])
    index = sorted_dates.index(current)
    if index == len(sorted_dates)-1: return sorted_dates[-2]
    return sorted_dates[index+1]


'''
@param selected_datetime
@param datetime_options: all break-times
@param offset: how many breaks to fast-forward to
@return: the datetime of the break at specified offset. If the resulting index is invalid (e.g. < 0) -> returns None (No IndexError)
'''
def get_relative_break(selected_datetime: datetime.datetime, datetime_options: list[datetime.datetime], offset) -> datetime.datetime:
    if not selected_datetime: return None
    if selected_datetime not in datetime_options:
        raise ValueError('Selected_datetime must itself be from datetime_options')
    sdates = sorted(datetime_options)
    index = sdates.index(selected_datetime)
    if 0 <= index+offset < len(sdates):
        return sdates[index+offset]
    return None
