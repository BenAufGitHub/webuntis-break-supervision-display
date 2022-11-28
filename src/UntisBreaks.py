import datetime
import webuntis


def _group_by_start(break_supervisions: list) -> dict:
    result = {}
    for bs in break_supervisions:
        if bs.start not in result.keys():
            result[bs.start] = []
        result[bs.start].append(bs)
    return result


def _todays_supervisions(session: webuntis.Session) -> list:
    all_supervisions = []
    today = datetime.datetime.today()
    current_day = datetime.datetime(today.year,today.month,today.day)

    for teacher in session.teachers():
        periods = session.timetable(teacher=teacher.id, start=current_day, end=current_day)
        teachers_supervisions = filter(lambda p: p.type == 'bs', periods)
        all_supervisions += teachers_supervisions
    return all_supervisions


'''
@param session: containing server, username, password, school and useragent information (do not login with the session)
@return dict-keys: datetime (always from current day) / dict-values: list of all break-supervisions (webuntis.objects.PeriodObject)
'''
def get_todays_supervisions(session: webuntis.Session) -> dict:
    with session.login() as s:
        supervisions = _todays_supervisions(s)
        return _group_by_start(supervisions)

             