import unittest

from collections import Counter
from datetime import date, datetime


PAGE_POS = 6


class LogLine:
    def __init__(self, log: str):
        self.user = self._parse_user(log)
        self.page = self._parse_page(log)
        self.browser = self._parse_browser(log)
        self.request_time = self._parse_request_time(log)
        self.date = self._parse_date(log)

    @staticmethod
    def _parse_user(log: str) -> str:
        return log[:log.find(" ")]

    @staticmethod
    def _parse_page(log: str) -> str:
        return log.split(" ")[PAGE_POS]

    @staticmethod
    def _parse_date(log: str) -> date:
        string_date = log[log.find("[") + 1:log.find("]")].split(":")[0]
        return datetime.strptime(string_date, "%d/%b/%Y").date()

    @staticmethod
    def _parse_request_time(log: str) -> int:
        return int(log.split(" ")[-1])

    @staticmethod
    def _parse_browser(log: str) -> str:
        most_right_quote = log.rfind("\"")
        return log[log.rfind("\"", 0, most_right_quote) + 1:most_right_quote]


class LogAnalyzer:
    def __init__(self):
        self.__slowest_page = ("", 0)
        self.__fastest_page = ("", float("+inf"))
        self.__popular_page = ""
        self.__page_frequency = Counter()
        self.__page_request_time = Counter()
        self.__popular_browser = ""
        self.__browser_frequency = Counter()
        self.__active_user = ""
        self.__user_frequency = Counter()
        self.__active_user_by_day = {}
        self.__user_by_day_frequency = {}

    def add_line(self, line: str) -> None:
        if line == "":
            return None

        log_line = LogLine(line)

        if self.__fastest_page[1] >= log_line.request_time:
            self.__fastest_page = (log_line.page, log_line.request_time)

        if self.__slowest_page[1] <= log_line.request_time:
            self.__slowest_page = (log_line.page, log_line.request_time)

        self.__user_frequency.update({log_line.user: 1})
        self.__active_user = self._update_most_object(
            self.__active_user, log_line.user, self.__user_frequency
        )

        self.__browser_frequency.update({log_line.browser: 1})
        self.__popular_browser = self._update_most_object(
            self.__popular_browser, log_line.browser, self
            .__browser_frequency
        )

        self.__page_frequency.update({log_line.page: 1})
        self.__popular_page = self._update_most_object(
            self.__popular_page, log_line.page, self.__page_frequency
        )
        self.__page_request_time.update(
            {log_line.page: log_line.request_time})

        if self.__user_by_day_frequency.get(log_line.date) is None:
            self.__active_user_by_day[log_line.date] = ""
            self.__user_by_day_frequency[log_line.date] = Counter()
        self.__user_by_day_frequency[log_line.date].update(
            {log_line.user: 1})

        self.__active_user_by_day[log_line
                                  .date] = self._update_most_object(
            self.__active_user_by_day[log_line.date],
            log_line.user, self.__user_by_day_frequency[log_line
                                                        .date]
        )

    def results(self) -> dict[str, str | dict[date, str]]:
        return {
            'FastestPage': self.__fastest_page[0],
            'SlowestPage': self.__slowest_page[0],
            'MostPopularPage': self.__popular_page,
            'MostActiveClient': self.__active_user,
            'MostPopularBrowser': self.__popular_browser,
            'MostActiveClientByDay': self.__active_user_by_day,
            'SlowestAveragePage': self._get_slowest_avg_page(),
        }

    def _get_slowest_avg_page(self) -> str:
        slowest_avg_page = ("", 0.0)
        for page in self.__page_frequency.keys():
            if page == "/":
                continue

            avg_time = self.__page_request_time[page] / \
                self.__page_frequency[page]
            if slowest_avg_page[1] < avg_time:
                slowest_avg_page = (page, avg_time)
        return slowest_avg_page[0]

    @staticmethod
    def _update_most_object(obj: str, field: str, freq_stat: Counter) -> str:
        if freq_stat[obj] <= freq_stat[field]:
            return (
                min(obj,
                    field) if freq_stat[obj] == freq_stat[field] else field
            )
        return obj


def make_stat() -> LogAnalyzer:
    return LogAnalyzer()


class LogStatTests(unittest.TestCase):
    LOG_LINE_TEXT = ('192.168.65.56 - - [17/Feb/2013:06:37:36 +0600] '
                     '"GET /tv/useUser HTTP/1.1" 200 1046 '
                     '"http://192.168.65.101/pause/index" '
                     '"Mozilla/5.0 (Windows NT 5.1; rv:15.0)' +
                     ' Gecko/20100101 Firefox/15.0" 30349')
    log_line = LogLine(LOG_LINE_TEXT)

    def test_user_parse(self) -> None:
        self.assertEqual("192.168.65.56", self.log_line.user)

    def test_date_parse(self) -> None:
        self.assertEqual(date(2013, 2, 17), self.log_line.date)

    def test_page_parse(self) -> None:
        self.assertEqual("/tv/useUser", self.log_line.page)

    def test_process_request_parse(self) -> None:
        self.assertEqual(30349, self.log_line.request_time)

    def test_browser_parse(self) -> None:
        self.assertEqual(
            "Mozilla/5.0 (Windows NT 5.1; rv:15.0) Gecko/20100101" +
            " Firefox/15.0",
            self.log_line.browser
        )


def parse_args():
    import argparse
    parser = argparse.ArgumentParser(
        description='Log analyzer written as class')
    parser.add_argument("-f", "--file", required=True,
                        help="log file to analyze")
    args = parser.parse_args()
    return args


def main():
    from pprint import pprint
    args = parse_args()
    analyzer = LogAnalyzer()
    with open(args.file, encoding="cp1251", errors="ingore") as file:
        for line in file:
            if "OPTION" in line:
                continue
            analyzer.add_line(line)
        res = analyzer.results()
        pprint(res)


if __name__ == '__main__':
    main()
