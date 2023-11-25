from time import time, sleep


class MyContextLogger:
    def __init__(self):
        self.start = None
        self.end = None

    def __enter__(self):
        self.start = time()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = time()
        print(f"took {self.end - self.start}")


class MySupress:
    def __init__(self, *exceptions):
        self._exceptions = exceptions

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_inst, exc_tb):
        if exc_type is None:
            return
        if issubclass(exc_type, self._exceptions):
            return True
        if issubclass(exc_type, BaseExceptionGroup):
            match, rest = exc_inst.split(self._exceptions)
            if rest is None:
                return True
            raise rest
        return False


with MyContextLogger():
    sleep(1)
    print(1)

with MySupress(IndexError):
    a = [1]
    print(a[2])
    print(a[0])
