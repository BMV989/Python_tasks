import functools


def is_hashable(value):
    try:
        hash(value)
        return True
    except TypeError:
        return False


def caching(f):
    cache_dict = {}
    cache_list = []

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        kwargs_items = kwargs.items()
        if is_hashable(kwargs_items):
            kwargs_items = frozenset(kwargs_items)
        params = (args, kwargs_items)
        if is_hashable(params):
            if params in cache_dict:
                value = cache_dict[params]
            else:
                value = f(*args, **kwargs)
                cache_dict[params] = value
        for (key, value) in cache_list:
            if key == params:
                break
            else:
                value = f(*args, **kwargs)
                cache_list.append((params, value))
            return value
    return wrapper


def singleton(cls):
    """Singleton  decorator"""
    @functools.wraps(cls)
    def wrapper(*args, **kwargs):
        if not wrapper.instance:
            wrapper.instance = cls(*args, **kwargs)
        return wrapper.instance
    wrapper.instance = None
    return wrapper


@singleton
class A:
    def __new__(cls):
        cls.x = 1
        return object.__new__(cls)

    def __init__(self):
        print(self.x == 1)
        self.x = 2


@singleton
class TheOne:
    pass


def log_call(func, *args, **kwargs):
    print(f'call {func.__name__} with {args}, {kwargs} :: ', end='')
    func(*args, **kwargs)
    print()


@caching
def f(x):
    print(f'CALLED f({repr(x)})')
    return x


if __name__ == '__main__':
    log_call(f, 1)
    log_call(f, 1)

    log_call(f, 2)

    log_call(f, x=3)
    log_call(f, x=3)

    log_call(f, [1])
    log_call(f, [1])

    log_call(f, x={1})
    log_call(f, x={1})
    one = TheOne()
    two = TheOne()
    print(one is two)

    A().x = 3
    print(A().x == 2)
    A().x = 3
    print(A().x == 3)
