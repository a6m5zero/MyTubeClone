import datetime as dt


def year_to_template(request):
    """
    Добавляет в шаблон переменную с текущим годом
    """
    return {'year': dt.datetime.now().year}