import os
import PyDST


def handle_kwargs_test():
    assert PyDST.cutils.handle_kwargs('asd', **{'a':1,'b':2}) == 'asd&a=1&b=2'


if __name__ == '__main__':
    handle_kwargs_test()
