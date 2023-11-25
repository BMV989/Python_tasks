#!/usr/bin/env python3

import urllib.request
from collections import Counter


def make_stat(filename: str) -> dict[str, Counter]:
    """
    Функция вычисляет статистику по именам за каждый год с учётом пола.
    """
    with urllib.request.urlopen(
        "http://shannon.usu.edu.ru/ftp/python/hw2/home.html"
    ) as res:
        content = res.read().decode("cp1251")
        stat = {}
        exceptions = {"Никита", "Илья", "Лёва"}
        e = 0
        while e != -1:
            text = content[content.find("<h3>") + len("<h3>"):]
            year = text[: text.find("</h3>")]
            stat[year] = Counter()
            i = 0
            while i != -1:
                names = text[text.find("/>") + len("/>"): text.find("</a>")]
                text = (
                    text[text.find("</a>") +
                         1: text.find("<h3>") + len("<h3>")]
                    if text.find("<h3>") != -1
                    else text[text.find("</a>") + 1:]
                )
                i = text.find("</a>")
                first_name = names.split()[1]
                sex = "FM" if ((first_name[-1] == "а"
                                or first_name[-1] == "я"
                                or first_name[-2:] == "вь")
                               and first_name not in exceptions) else "M"
                name_and_sex = f"{first_name} {sex}"
                if name_and_sex not in stat[year]:
                    stat[year][name_and_sex] = 1
                else:
                    stat[year][name_and_sex] += 1
            content = content[content.find("<h3>") + len("<h3>"):]
            e = content.find("<h3>")
        return stat


def extract_years(stat: dict) -> list[str]:
    """
    Функция принимает на вход вычисленную статистику и выдаёт список годов,
    упорядоченный по возрастанию.
    """
    return list(stat.keys())[::-1]


def extract_general(stat: dict) -> list[tuple[str, int]]:
    """
    Функция принимает на вход вычисленную статистику и выдаёт список tuple'ов
    (имя, количество) общей статистики для всех имён.
    Список должен быть отсортирован по убыванию количества.
    """
    general_counter = sum(stat.values(), Counter())
    ans = []
    for name_and_sex, number in general_counter.most_common(len(general_counter)):
        ans.append((name_and_sex.split()[0], number))
    return ans


def extract_general_male(stat: dict) -> list[tuple[str, int]]:
    """
    Функция принимает на вход вычисленную статистику и выдаёт список tuple'ов
    (имя, количество) общей статистики для имён мальчиков.
    Список должен быть отсортирован по убыванию количества.
    """
    general_counter = sum(stat.values(), Counter())
    ans = []
    for name_and_sex, number in general_counter.most_common(len(general_counter)):
        if name_and_sex.split()[1] == "FM":
            continue
        ans.append((name_and_sex.split()[0], number))
    return ans


def extract_general_female(stat: dict) -> list[tuple[str, int]]:
    """
    Функция принимает на вход вычисленную статистику и выдаёт список tuple'ов
    (имя, количество) общей статистики для имён девочек.
    Список должен быть отсортирован по убыванию количества.
    """
    general_counter = sum(stat.values(), Counter())
    ans = []
    for name_and_sex, number in general_counter.most_common(len(general_counter)):
        if name_and_sex.split()[1] == "M":
            continue
        ans.append((name_and_sex.split()[0], number))
    return ans


def extract_year(stat: dict, year: str) -> list[tuple[str, int]]:
    """
    Функция принимает на вход вычисленную статистику и год.
    Результат — список tuple'ов (имя, количество) общей статистики для всех
    имён в указанном году.
    Список должен быть отсортирован по убыванию количества.
    """
    counter = stat[year]
    ans = []
    for name_and_sex, number in counter.most_common(len(counter)):
        ans.append((name_and_sex.split()[0], number))
    return ans


def extract_year_male(stat: dict, year: str) -> list[tuple[str, int]]:
    """
    Функция принимает на вход вычисленную статистику и год.
    Результат — список tuple'ов (имя, количество) общей статистики для всех
    имён мальчиков в указанном году.
    Список должен быть отсортирован по убыванию количества.
    """
    counter = stat[year]
    ans = []
    for name_and_sex, number in counter.most_common(len(counter)):
        if name_and_sex.split()[1] == "FM":
            continue
        ans.append((name_and_sex.split()[0], number))
    return ans


def extract_year_female(stat: dict, year: str) -> list[tuple[str, int]]:
    """
    Функция принимает на вход вычисленную статистику и год.
    Результат — список tuple'ов (имя, количество) общей статистики для всех
    имён девочек в указанном году.
    Список должен быть отсортирован по убыванию количества.
    """
    counter = stat[year]
    ans = []
    for name_and_sex, number in counter.most_common(len(counter)):
        if name_and_sex.split()[1] == "M":
            continue
        ans.append((name_and_sex.split()[0], number))
    return ans


if __name__ == "__main__":
    pass
