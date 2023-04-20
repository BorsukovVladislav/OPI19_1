#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
from pydantic import BaseModel, ValidationError


class School(BaseModel):
    name: str
    group: int
    marks: list


def validating(req):
    try:
        School(**req)
    except ValidationError as e:
        print(e.json())
        return False, e
    message = "JSON файл коректен"
    return True, message


def help_info():
    """
    Вывод информации о командах
    """
    print("Список команд:")
    print("add - добавить студента")
    print("list - вывести список студентов")
    print("filter list - список студентов со средним баллом больше 4")
    print("load - загрузить данные из файла")
    print("save - сохранить данные в файл")
    print("exit - завершить работу с программой")


def add_student():
    """
    Добавление студента в список
    """
    name = input("Фамилия и инициалы студента: ")
    group = int(input("Номер группы: "))
    marks = list(map(int, input("Пять оценок студента: ").split()))

    if len(marks) != 5:
        print("Неверное количество оценок", file=sys.stderr)
        return

    return {
        'name': name,
        'group': group,
        'marks': marks,
    }


def out_students(list_stud):
    """
    Вывод списка студентов
    """
    if list_stud:
        line = '+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 14,
        )
        print(line)
        print(
            '| {:^4} | {:^30} | {:^14} |'.format(
                "№",
                "Ф.И.О.",
                "Номер группы",
            )
        )
        print(line)

        for idx, student in enumerate(list_stud, 1):
            print(
                '| {:>4} | {:<30} | {:<14} |'.format(
                    idx,
                    student.get('name', ''),
                    student.get('group', ''),
                )
            )
        print(line)
    else:
        print("Список студентов пустой.")


def students_filter(list_s):
    """
    Вывод списка студентов со средним баллом больше 4
    """
    if len(list_s) > 0:
        filter_s = []
        for student in list_s:
            if sum(student.get('marks')) / 5 > 4:
                filter_s.append(student)
        return filter_s
    else:
        print("Список студентов пустой.")


def save_students(file_name, students):
    """
    Сохранение всех студентов в файл JSON.
    """
    with open(file_name, "w", encoding="utf-8") as fout:
        json.dump(students, fout, ensure_ascii=False, indent=4)


def load_students(file_name):
    """
    Загрузка всех студентов из файла JSON.
    """
    with open(file_name, "r", encoding="utf-8") as fin:
        return json.load(fin)


def main():
    """
    Главная функция
    """

    students = []

    while True:
        command = input(">>> ").lower()

        if command == 'exit':
            break

        elif command == 'help':
            help_info()

        elif command == 'add':
            student = add_student()
            students.append(student)

            if len(students) > 1:
                students.sort(key=lambda item: item.get('group', ''))

        elif command == 'list':
            out_students(students)

        elif command == "filter list":
            filter_list = students_filter(students)
            out_students(filter_list)

        elif command.startswith("save "):
            parts = command.split(maxsplit=1)
            file_name = parts[1] + ".json"
            save_students(file_name, students)

        elif command.startswith("load "):
            parts = command.split(maxsplit=1)
            file_name = parts[1] + ".json"
            students = load_students(file_name)

            for smt in students:
                check, announce = validating(smt)
                if check:
                    students = load_students(file_name)
                else:
                    print(announce)
                    break

        else:
            print(f"Неизвестная команда {command}", file=sys.stderr)


if __name__ == '__main__':
    main()
