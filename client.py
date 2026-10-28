import requests


BASE = "http://127.0.0.1:5000"


class ServerNedostupen(Exception):
    """Исключение при отсутствии доступа к серверу"""
    pass


def _zapros(method, adress, *args, **kwargs):
    """Внутренняя функция через которую проходят все запросы"""
    try:
        r = requests.request(method, BASE + adress, *args, **kwargs, timeout=3)
    except requests.exceptions.ConnectionError:
        raise ServerNedostupen("Сервер не отвечает")
    except requests.exceptions.Timeout:
        raise ServerNedostupen("Сервер не отвечает дольше 3 секунд")

    if r.status_code >= 500:
        raise ServerNedostupen(f"ошибка сервера: {r.status_code}")
    return r


def get_all_anketi():
    """Забирает все анкеты"""
    r = _zapros("GET", "/anketi")
    return r.json()


def get_anketa_by_nomer(nomer):
    """Забирает одну анкету по номеру, если ее нет - None"""
    r = _zapros("GET", f"/anketi/{nomer}")
    if r.status_code == 404:
        return None
    return r.json()


def post_mail_proverka(mail):
    """Отправляет почту на проверку"""
    r = _zapros("POST", "/proverka", json={"mail": mail})
    if r.status_code >= 400:
        return False
    return bool(r.json().get('prinyato'))


def get_statistika():
    """Забирает статистику сервера"""
    r = _zapros("GET", "/statistika")
    return r.json()