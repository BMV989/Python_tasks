from io import TextIOWrapper
from collections import Counter


def get_most_active_user(file: TextIOWrapper) -> str:
    ans = Counter()
    for line in file:
        content = line.split(", ")[0]
        if content not in ans:
            ans[content] = 1
        else:
            ans[content] += 1
    return ans.most_common(1)[0][0]


def get_most_popular_resource(file: TextIOWrapper) -> str:
    ans = Counter()
    for line in file:
        content = line.split(", ")
        content = content[len(content) - 2]
        if content not in ans:
            ans[content] = 1
        else:
            ans[content] += 1
    return ans.most_common(1)[0][0]


def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description='Log analyzer')
    parser.add_argument("-f", "--file", help="log file to analyze")
    parser.add_argument("-u", "--user", default=False, action="store_true",
                        help="most active user statistic")
    parser.add_argument("-r", "--resource", default=False, action="store_true",
                        help="most popular resource statistic")
    args = parser.parse_args()
    return args


def main():
    from sys import exit
    from os import path
    args = parse_args()
    if not args.file or not path.exists(args.file):
        print("[*] ERROR: Invalid file." +
              " Please, provide valid log file to analyze (-h for help)")
        exit(1)
    if not args.user and not args.resource:
        print("[*] ERROR: Abscence of flags." +
              " Please, provide flags: -u for most active user" +
              " or -r for most popular resource (-h for help)")
        exit(2)
    if args.user:
        with open(args.file, encoding="cp1251", errors="ignore") as file:
            print(f"most actvie user -> {get_most_active_user(file)}")
    if args.resource:
        with open(args.file, encoding="cp1251", errors="ignore") as file:
            print(
                f"most popular resource -> {get_most_popular_resource(file)}"
            )


if __name__ == "__main__":
    main()
