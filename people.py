class AnketaError(Exception):
    """Ошибка заполнения анкеты"""


class Person:
    """Базовый класс - человек, с проверками ФИО, почты и телефона"""
    def __init__(self, fio: str, email: str, phone: str) -> None:
        self.fio = self._validate_fio(fio)
        self.email = self._validate_email(email)
        self.phone = self._validate_phone(phone)

    @staticmethod
    def _validate_fio(fio: str) -> str:
        """Проверяет ФИО, возвращает отформатированную строку"""
        if len(fio.split()) < 2:
            raise AnketaError("В ФИО меньше 2 слов")
        return " ".join(fio.split()).title()

    @staticmethod
    def _validate_email(email: str) -> str:
        """Проверяет почту, возвращает отформатированную строку"""
        email = "".join(email.split()).lower()
        if email.count("@") != 1:
            raise AnketaError("В почте нет @")

        local, domain = email.split("@")
        if not local or not domain:
            raise AnketaError("Локальная часть или домен почты не полные")

        if "." not in domain or domain.startswith(".") or domain.endswith("."):
            raise AnketaError("Точка в домене почты расположена неправильно")
        return email

    @staticmethod
    def _validate_phone(phone: str) -> str:
        """Проверяет телефон, возвращает отформатированную строку"""
        clean = "".join(ch for ch in phone if ch.isdigit())

        if len(clean) != 11:
            raise AnketaError("В номере телефона не 11 цифр")

        if clean[0] not in ("7", "8"):
            raise AnketaError("Номер не начинается с 7 или 8")
        return f"7{clean[1:]}"

    def masked_phone(self) -> str:
        """Возвращает телефон с маской"""
        clean = "7" + self.phone[1:]
        code = clean[1:4]
        last_two = clean[-2:]
        return f"+7 ({code}) ***-**-{last_two}"

    def short_fio(self):
        """Возвращает ФИО в формате Фамилия И. О."""
        fio_lst = self.fio.split()
        surname = fio_lst[0]

        short = []
        for item in fio_lst[1:]:
            short.append(item[0] + ".")
        return f"{surname} {' '.join(short)}"

    def role(self) -> str:
        """Присваивает роль классу"""
        return "Человек"

    def extra(self) -> None:
        """Доп информация"""
        pass

    def __str__(self) -> str:
        return self.fio

    def _sort_key(self) -> str:
        """Ключ для сортировки, ё -> е"""
        return self.fio.lower().replace("ё", "е")

    def __lt__(self, other: "Person") -> bool:
        return self._sort_key() < other._sort_key()


class Student(Person):
    """Дочерний класс, студент"""
    def __init__(self, fio: str, email: str, phone: str, group: str) -> None:
        super().__init__(fio, email, phone)
        group = group.strip().lower()

        if not group:
            raise AnketaError("Группа пустая")
        self.group = group

    def role(self) -> str:
        """Присваивает роль классу"""
        return "Студент"

    def extra(self) -> str:
        """Добавляет группу"""
        return self.group


class Teacher(Person):
    """Дочерний класс, преподаватель"""
    def __init__(self, fio: str, email: str, phone: str, department: str) -> None:
        super().__init__(fio, email, phone)
        department = department.strip()

        if not department:
            raise AnketaError("Кафедра пустая")
        self.department = department

    def role(self) -> str:
        """Присваивает роль классу"""
        return "Преподаватель"

    def extra(self) -> str:
        """Добавляет кафедру"""
        return self.department


if __name__ == "__name__":
    student = Student("белов максим", "belov@yandex.ru", "89113334455", "10а12")

    assert student.phone == "79113334455"
    assert student.fio == "Белов Максим"
    assert student.role() == "Студент"

    assert student.masked_phone() == "+7 (911) ***-**-55"
    assert student.short_fio() == "Белов М."


