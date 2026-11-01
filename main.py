import json

from registry import Registry
from people import Student, Teacher, AnketaError
from  client import ServerNedostupen, get_all_anketi, get_statistika, post_mail_proverka


ANKETA_TXT = "anketa.txt"
OTCHET_JSON = "otchet.json"


def anketa_for_class(anketa: dict) -> Student | Teacher:
    """Превращает словарь в объект Student | Teacher"""
    tip = anketa.get("tip")
    fio = anketa.get("fio")
    email = anketa.get("mail")
    phone = anketa.get("phone")

    if tip == "s":
        return Student(fio, email, phone, anketa.get("gruppa"))
    if tip == "t":
        return Teacher(fio, email, phone, anketa.get("kafedra"))
    raise AnketaError(f"Неизвестный тип: {tip}")


def upload_from_server(registry: Registry) -> None:
    """Забирает анкеты с сервера"""
    for a in get_all_anketi():
        try:
            registry.add(anketa_for_class(a))
        except AnketaError as e:
            registry.rejected.append((a.get("nomer"), str(a), str(e)))


def print_stat() -> None:
    """Печатает статистику с сервера"""
    stat = get_statistika()
    if stat:
        print(f"Всего анкет: {stat.get('vsego')}")
        for role, count in (stat.get("po_rolyam") or {}).items():
            print(f"{role}: {count}")
    else:
        raise ServerNedostupen("Статистика с сервера не получена")



def print_table(registry: Registry) -> None:
    """Печатает таблицу принятых анкет"""
    if not registry.accepted:
        print("Принятых нет")
        return

    rows = []
    for i, p in enumerate(sorted(registry.accepted), 1):
        rows.append([str(i), p.fio, p.role(), p.extra(), p.masked_phone()])

    headers = ["№", "ФИО", "Роль", "Группа/кафедра", "Телефон"]

    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(cell))

    def show(cells):
        """Печатает одну строку таблицы, выравнивая ячейки по widths"""
        print("  ".join(c.ljust(w) for c, w in zip(cells, widths)))

    show(headers)
    print("-" * (sum(widths) + 2 * (len(widths) - 1)))
    for row in rows:
        show(row)


def main():
    """Главная функция, логика программы"""
    registry = Registry()

    try:
        upload_from_server(registry)
        source = "server"
        print("Источник данных - сервер")
    except ServerNedostupen as e:
        print(f"Сервер не доступен: {e}")
        print(f"Данные берутся из {ANKETA_TXT}")

        if not registry.load(ANKETA_TXT):
            print(f"Файл {ANKETA_TXT} не найден, программа остановлена")
            return

        source = "file"
        print(f"Источник данных - файл {ANKETA_TXT}")


    print_table(registry)

    if registry.rejected:
        print("\nОтклонено:")
        for n, raw, reason in registry.rejected:
            print(f"  {n}: {reason} -> {raw}")

    print(f"\nПринято: {len(registry)} | Отклонено: {len(registry.rejected)}")

    print("\nПо ролям:")
    for role, count in registry.role_stats().items():
        print(f"  {role}: {count}")

    print("\nПо группам/кафедрам:")
    for name, count in registry.group_stats().items():
        print(f"  {name}: {count}")


    print()
    if source == "server":
        try:
            print("Статистика с сервера:")
            print_stat()
        except ServerNedostupen:
            print("    НЕДОСТУПНО")

    print()
    print("Проверка почт через сервер")
    temp_check_mail = []
    for a in registry.accepted:
        if source != "server":
            temp_check_mail.append((a, None))
            print(f"{a.fio}: пропущено (нет сервера)")
            continue
        try:
            ok = post_mail_proverka(a.email)
        except ServerNedostupen as e:
            temp_check_mail.append((a, None))
            print(f"{a.fio}: не проверено ({e})")
            continue

        temp_check_mail.append((a, ok))
        if ok:
            print(f"{a.fio}: {'принята'}")
        else:
            print(f"{a.fio}: {'отклонена'}")


    otchet = {
        "Источник": source,
        "Принято": len(registry),
        "Отклонено": len(registry.rejected),
        "Принятые": [
            {
                "fio": p.fio, "role": p.role(), "extra": p.extra(),
                "email": p.email, "phone": p.phone, "proverka_pochty": ok,
            }
            for p, ok in temp_check_mail
        ],
        "Отклоненные": [
            {"номер": n, "строка": raw, "причина": reason}
            for n, raw, reason in registry.rejected
        ],
        "Роли": registry.role_stats(),
    }
    with open(OTCHET_JSON, "w", encoding="utf-8") as f:
        json.dump(otchet, f, ensure_ascii=False, indent=2)
    print(f"\nОтчёт сохранён в {OTCHET_JSON}")

    registry.save_in_accepted()
    registry.save_in_rejected()


if __name__ == "__main__":
    main()


