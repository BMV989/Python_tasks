import os
import sys
import itertools
import operator
import functools


def project_stats(path, extensions):
    """
    Вернуть число строк в исходниках проекта.

    Файлами, входящими в проект, считаются все файлы
    в папке ``path`` (и подпапках), имеющие расширение
    из множества ``extensions``.
    """
    files_with_extension = with_extensions(extensions, iter_filenames(path))
    return total_number_of_lines(files_with_extension)


def total_number_of_lines(filenames):
    """
    Вернуть общее число строк в файлах ``filenames``.
    """
    return sum(map(number_of_lines, filenames))


def number_of_lines(filename):
    """
    Вернуть число строк в файле.
    """
    with open(filename, encoding="utf-8", errors="ignore") as f:
        return sum(map(lambda _: 1, f))


def iter_filenames(path):
    """
    Итератор по именам файлов в дереве.
    """
    if os.path.isfile(path):
        return [path]
    files = map(lambda name: f'{path}/{name}', os.listdir(path))
    return functools.reduce(operator.add, map(iter_filenames, files), [])


def with_extensions(extensions, filenames):
    """
    Оставить из итератора ``filenames`` только
    имена файлов, у которых расширение - одно из ``extensions``.
    """
    return list(itertools
                .filterfalse(lambda x: get_extension(x) not in extensions,
                             filenames))


def get_extension(filename):
    """ Вернуть расширение файла """
    return os.path.splitext(filename)[1]


def print_usage():
    print("Usage: python project_sourse_stats_3.py <project_path>")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print_usage()
        sys.exit(1)

    project_path = sys.argv[1]
    print(project_stats(project_path, {'.cs'}))
