from transaction import TransactionManager
from flask import g, Flask
from werkzeug.local import LocalProxy


def get_tm():
    if 'tm' not in g:
        g.tm = TransactionManager()
    return g.tm

# DMS is a dict of named datamanagers
def get_dms():
    if not 'dms' in g:
        g.dms = {}
    return g.dms


def before():
    get_tm() #initialize tm


def teardown(error):
    if error is None:
        try:
            g.tm.commit()
        except Exception as e:
            g.tm.abort()
    else:
        g.tm.abort()

    if 'dms' in g:
        for k, v in g.dms.items():
            if hasattr(v, 'close'):
                v.close()
        del g.dms


def init_transaction(app: Flask):
    app.tm = LocalProxy(get_tm)
    app.dms = LocalProxy(get_dms)
    app.before_request(before)
    app.teardown_request(teardown)




