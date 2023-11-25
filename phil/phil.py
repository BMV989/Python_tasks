#!/usr/bin/env python3

from urllib.error import URLError
from urllib.request import urlopen, HTTPError
from urllib.parse import quote, unquote
from collections import deque
import re

RE_LINK = re.compile(r'/wiki/([^:# ]+)[\"\']', flags=re.IGNORECASE)
RE_BODY_START = re.compile(
    r'<div class="mw-content-ltr mw-parser-output" lang="ru" dir="ltr">')
RE_BODY_END = re.compile(r'\<\!\-\-esi')


def get_content(name: str) -> str | None:
    """
    Функция возвращает содержимое вики-страницы name из русской Википедии.
    В случае ошибки загрузки или отсутствия страницы возвращается None.
    """
    try:
        with urlopen(f'https://ru.wikipedia.org/wiki/{quote(name)}') as page:
            content = page.read().decode("utf-8")
            return content
    except (URLError, HTTPError):
        return None


def extract_content(page: str | None) -> tuple[int, int]:
    """
    Функция принимает на вход содержимое страницы и возвращает 2-элементный
    tuple, первый элемент которого — номер позиции, с которой начинается
    содержимое статьи, второй элемент — номер позиции, на котором заканчивается
    содержимое статьи.
    Если содержимое отсутствует, возвращается (0, 0).
    """
    if page is None:
        return (0, 0)
    body_start = re.search(RE_BODY_START, page)

    if body_start is None:
        return (0, 0)

    body_end = re.search(RE_BODY_END, page)

    if body_end is None:
        return (0, 0)

    return (body_start.end(), body_end.start())


def extract_links(page: str | None, begin: int, end: int) -> list[str]:
    """
    Функция принимает на вход содержимое страницы и начало и конец интервала,
    задающего позицию содержимого статьи на странице и возвращает все имеющиеся
    ссылки на другие вики-страницы без повторений и с учётом регистра.
    """
    if page is None:
        return []
    links = RE_LINK.findall(page[begin:end])
    links = set(links)
    return [unquote(link) for link in links]


def find_chain(start: str, finish: str) -> list[str] | None:
    """
    Функция принимает на вход название начальной и конечной статьи и возвращает
    список переходов, позволяющий добраться из начальной статьи в конечную.
    Первым элементом результата должен быть start, последним — finish.
    Если построить переходы невозможно, возвращается None.
    """
    if get_content(start) is None or get_content(finish) is None:
        return None
    queue = deque([start])
    paths = {start: []}
    while len(queue) > 0:
        name = queue.pop()
        page = get_content(name)
        page_begin, page_end = extract_content(page)
        links = extract_links(page, page_begin, page_end)
        if len(links) == 0:
            continue
        for link in links:
            if link == finish:
                return paths[name] + [name, finish]

            if link in paths.keys():
                continue

            paths[link] = paths[name] + [name]
            queue.appendleft(link)
    return None


def main():
    from sys import argv
    if len(argv) < 2:
        print("Please provide start path")
        exit(-1)
    print(find_chain(argv[1], "Философия"))


if __name__ == '__main__':
    main()
