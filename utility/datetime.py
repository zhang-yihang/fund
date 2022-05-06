import datetime


def GetDateTime():
    curr_time = datetime.datetime.now()
    return curr_time.year*365+curr_time.month*31+curr_time.day
