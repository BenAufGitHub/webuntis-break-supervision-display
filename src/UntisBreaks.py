import datetime
import webuntis


def _group_by_start(break_superv: list) -> dict:
    result = {}
    for bs in break_superv:
        if bs.start not in result.keys():
            result[bs.start] = []
        result[bs.start].append(bs)
    return result


def _todays_supervisions(session: webuntis.Session) -> set:
    all_supervisions = set()
    today = datetime.datetime.today()
    current_day = datetime.datetime(today.year,today.month,today.day)
    for teacher in session.teachers():
        break_superv = session.timetable(teacher=teacher.id, start=current_day, end=current_day).filter(type='bs')
        for bs in break_superv:
            all_supervisions.add(bs)
    return all_supervisions


'''
@param session: containing server, username, password, school and useragent information
@return dict-keys: datetime (always from current day) / dict-values: list of all break-supervisions (webuntis.objects.PeriodObject)
'''
def get_todays_supervisions(session: webuntis.Session) -> dict:
    supervisions = _todays_supervisions(session)
    return _group_by_start(supervisions)

             