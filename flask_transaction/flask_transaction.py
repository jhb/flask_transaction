from transaction import TransactionManager
from flask import g
from werkzeug.local import LocalProxy


def get_tm():
    if 'tm' not in g:
        g.tm = TransactionManager()
    return g.tm

# DMS stands for DataMangerS
def get_dms():
    if not 'dms' in g:
        g.dms = {}
    return g.dms


def before():
    get_tm() #initialize tm

def teardown(error=None):
    if error is None:
        g.tm.commit()
    else:
        g.tm.abort()

    if 'dms' in g:
        for k, v in g.dms.items():
            if hasattr(v, 'close'):
                v.close()
        del g.dms


def init_app(app):
    app.tm = LocalProxy(get_tm)
    app.dms = LocalProxy(get_dms)
    app.before_request(before)
    app.teardown_request(teardown)



