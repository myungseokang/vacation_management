import datetime


def get_using_date(start_date: datetime.datetime, end_date: datetime.datetime) -> float:
    """
    :param start_date: 휴가 시작일
    :param end_date: 휴가 종료일
    :return: 휴가 사용일수를 반환한다
    """
    time_d = end_date - start_date
    days, hours = int(time_d.days), int(time_d.seconds // 3600)
    print(days, hours)

    if hours == 9:
        # 업무시간이 9시간이라 9시간 단위로 추가해줌
        days += 1
    elif hours in [4, 5]:
        # 반차
        days = 0.5

    days = float(days)
    return days
