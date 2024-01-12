import datetime

weekdays = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']


def generate_the_date(yest_or_to_day: int=0) -> str:
    today = datetime.date.today()
    return_string = ''

    if(yest_or_to_day>0):
        weekday = datetime.date.weekday(today)-1+yest_or_to_day
    else:
        weekday = datetime.date.weekday(today)+yest_or_to_day

    today = str(today).split("-")
    if(weekday>=len(weekdays)):
        weekday = weekdays[weekday-len(weekdays)]
    else:
        weekday = weekdays[weekday+yest_or_to_day]

    return_string: str = f'{weekday}, {int(today[2])+yest_or_to_day} {months[int(today[1])-1]} {today[0]} г.'

    return return_string

if __name__ == '__main__':
    print(generate_the_date(1))