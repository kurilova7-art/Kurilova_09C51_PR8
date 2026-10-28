import pytest
from people import Person, AnketaError, Student, Teacher


@pytest.mark.parametrize("fio, expected", [
    ("  ИВАнов иван   ИваНОВИЧ", "Иванов Иван Иванович"),
    ("ВасичКИН   Петр", "Васичкин Петр"),
    ("пушкин  александр сергеевич ", "Пушкин Александр Сергеевич"),
    ("МАМИН-СИБИРЯК   дмитрий", "Мамин-Сибиряк Дмитрий")
])
def test_validate_fio_normalize(fio, expected):
    assert Person._validate_fio(fio) == expected


def test_validate_fio_one_word():
    with pytest.raises(AnketaError):
        Person._validate_fio("Боярова")


@pytest.mark.parametrize("email, expected", [
    ("  TRUCRa utecura-8404@Yopmail.com", "trucrautecura-8404@yopmail.com"),
    ("  koiproKOUjeupeu-4092@yopmail.COM   ", "koiprokoujeupeu-4092@yopmail.com")
])
def test_validate_email_lower_register(email, expected):
    assert Person._validate_email(email) == expected


@pytest.mark.parametrize("email", [
    "botosaprafroi-3812@",
    "caubreribronnu-7378mail.com",
    "@yopmail.com",
    ""
])
def test_validate_email_error(email):
    with pytest.raises(AnketaError):
        Person._validate_email(email)


@pytest.mark.parametrize("phone", [
    " 89113 3344 55 ",
    "8  9113334455     ",
    "79113334455  ",
    "89113334455"
])
def test_validate_phone_one_answer(phone):
    assert Person._validate_phone(phone) == "79113334455"


@pytest.mark.parametrize("phone", [
    "+15126445072",
    "+70831462",
    "284834133",
    ""
])
def test_validate_phone_error(phone):
    with pytest.raises(AnketaError):
        Person._validate_phone(phone)


@pytest.fixture
def temp_student_and_teacher() -> dict:
    student = Student("белов максим", "belov@yandex.ru", "89113334455", "10а12")
    teacher = Teacher("Павлов Никита", "pavlov@voenmeh.ru", "79213334455", "Кафедра И7")
    person_dict = {"student": student, "teacher": teacher}
    return person_dict


def test_masked_phone(temp_student_and_teacher):
    assert temp_student_and_teacher.get("student").masked_phone() == "+7 (911) ***-**-55"


def test_short_fio(temp_student_and_teacher):
    assert temp_student_and_teacher.get("student").short_fio() == "Белов М."


def test_role(temp_student_and_teacher):
    assert temp_student_and_teacher.get("student").role() != temp_student_and_teacher.get("teacher").role()


def test_student_empty_group():
    with pytest.raises(AnketaError):
        Student("белов максим", "belov@yandex.ru", "89113334455", "")


"""
Поскольку все функции, связанные с чтением файлов находятся в модуле registry.py, 
последние два теста из задания были перенесены в test_registry.py
"""