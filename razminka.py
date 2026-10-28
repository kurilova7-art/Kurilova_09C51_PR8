import requests


BASE = "http://127.0.0.1:5000"


# H1
r = requests.get(BASE + "/")
print(f"Код ответа: {r.status_code}")
print(f"Тип значения r.text: {type(r.text)}")
print(f"Тип значения r.json(): {type(r.json())}")
print(f"Название сервиса: {r.json().get('servis')}")
print()


# H2
r = requests.get(BASE + "/anketi")
print(f"Пришло анкет: {len(r.json())}")
print(f"ФИО первой анкеты: {r.json()[0].get('fio')}")
print()


# H3
r = requests.get(BASE + "/anketi/<99>")
print(f"Код ответа: {r.status_code}")
print(f"Значение r.ok: {r.ok}")
print(f"Текст ошибки: {r.text}")
print()


# H4
r = requests.get(BASE + "/anketi", params={"tip": "t"})
print(f"URL: {r.url}")
for t in r.json():
    print(f"ФИО: {t.get('fio')}, Кафедра: {t.get('kafedra')}")
print()


# H5
r = requests.post(BASE + "/proverka", json={"mail": "ivanov@mail.ru"})
r2 = requests.post(BASE + "/proverka", json={"mail": "kuznetsov.mail.ru"})

print(f"Первый запрос: ivanov@mail.ru - {r.status_code} - {r.json().get('prinyato')}")
print(f"Второй запрос: kuznetsov.mail.ru - {r2.status_code} - {r2.json().get('prinyato')}")

