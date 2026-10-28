import pytest
from registry import Registry
from people import Student, AnketaError


@pytest.fixture
def temp_registry(tmp_path) -> Registry:
    content = "\n".join([
        # верные
        "student;ёлкин максим;belov@yandex.ru;89113334455;10а12",
        "teacher;Павлов Никита;pavlov@voenmeh.ru;79213334455;Кафедра И7",
        "s;абрамов-петров иван;ivanov@mail.ru;89113334455;10б34",
        # бракованные
        "alien;Иванов Иван;ivanov@mail.ru;89113334455;10а12",
        "student;Иванов Иван;ivanov@mail.ru",
        "student;Иванов;ivanov@mail.ru;89113334455;10а12",
    ]) + "\n"
    path = tmp_path / "temp_registry.txt"
    path.write_text(content, encoding="utf-8")

    registry = Registry()
    assert registry.load(str(path)) is True, "Файл не загрузился в фикстуре"
    return registry


def test_parse_line_person_type():
    person = Registry._parse_line("student;белов максим;belov@yandex.ru;89113334455;10а12")
    assert isinstance(person, Student)


@pytest.mark.parametrize("lines", [
    "alien;Иванов Иван;ivanov@mail.ru;89113334455;10а12",
    "student;Иванов Иван;ivanov@mail.ru",
    ""
])
def test_parse_line_error(temp_registry, lines):
    with pytest.raises(AnketaError):
        temp_registry._parse_line(lines)


def test_len_empty_registry():
    registry = Registry()
    assert len(registry) == 0


def test_len_done_registry(temp_registry):
    assert len(temp_registry) == 3


def test_len_rejected_registry(temp_registry):
    assert len(temp_registry.rejected) == 3


def test_load_rejected_lines(temp_registry):
    lines = [n for n, _, _ in temp_registry.rejected]
    assert lines == [4, 5, 6]


def test_load_false(temp_registry):
    assert temp_registry.load("file_not_exist") is False


def test_role_stats(temp_registry):
    assert temp_registry.role_stats() == {"Студент": 2, "Преподаватель": 1}


def test_group_stats(temp_registry):
    assert temp_registry.group_stats() == {"10а12": 1, "10б34": 1}


def test_registry_is_iterable(temp_registry):
    result = [p.fio for p in temp_registry]
    assert result == ["Ёлкин Максим", "Павлов Никита", "Абрамов-Петров Иван"]


def test_sort_for_fio(temp_registry):
    result = [p.fio for p in sorted(temp_registry.accepted)]
    assert result == ["Абрамов-Петров Иван", "Ёлкин Максим", "Павлов Никита"]


def test_save_in_accepted(temp_registry, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    temp_registry.save_in_accepted()

    lines = (tmp_path / "ok.txt").read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 3


@pytest.mark.parametrize("errors, line", [
    ("Неизвестный тип", 0),
    ("Полей не 5", 1),
    ("В ФИО меньше 2 слов", 2)
])
def test_save_in_rejected(temp_registry, tmp_path, monkeypatch, errors, line):
    monkeypatch.chdir(tmp_path)
    temp_registry.save_in_rejected()

    lines = (tmp_path / "errors.txt").read_text(encoding="utf-8").strip().splitlines()
    assert errors in lines[line]