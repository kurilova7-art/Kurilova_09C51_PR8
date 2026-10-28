from registry import Registry
from people import Person


def print_table(registry):
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
    filename = registry.ask_file()

    if not registry.load(filename):
        print(f"Файл {filename} не найден")
        return

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

    registry.save_in_accepted()
    registry.save_in_rejected()


if __name__ == "__main__":
    main()


