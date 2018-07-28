import os
import PyDST


def handle_kwargs_test():
    assert PyDST.cutils.handle_kwargs('asd', **{'a':1,'b':2}) == 'asd&a=1&b=2'
    print('cutils.handle_kwargs is working')


def connection_gets_data():
    try:
        conn = PyDST.connection()
        print('established connection object')
        conn.get_data('FOLK1A')
        print('received data')
    except:
        raise ValueError('Connection cannot get data')


def connection_verbose():
    try:
        conn = PyDST.connection(language = 'da', verbose = True)
        resp = conn.get_data('FOD', 'Tid,barnkon')
    except:
        raise ValueError('Verbose seems to be not working')


def test_get_topics():
    try:
        conn = PyDST.connection()
        print('established connection')
        conn.get_topics('02')
        print('recieved a topic')
    except:
        raise ValueError('get_topics() is not working')


if __name__ == '__main__':
    print('Testing cutils.handle_kwargs()')
    handle_kwargs_test()
    print('testing if connection can get data')
    connection_gets_data()
    print('testing verbose mode')
    connection_verbose()
    print('testing get_topics()')
    test_get_topics()

    print('FINISHED TESTING')
