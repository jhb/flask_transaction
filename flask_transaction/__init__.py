from transaction import TransactionManager
from flask import g, Flask, current_app
from werkzeug.local import LocalProxy
from flask import request_tearing_down


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

#def teardown(*args,exc=None,**kwargs):
def teardown(error):
    debug = 0
    if debug: print('in teardown')
    #print(repr(exc))
    if debug: print('the error:', error)
    # print(repr(args))
    # print(repr(kwargs))

    if error is None:
        try:
            if debug: print('commit')
            g.tm.commit()
        except Exception as e:
            if debug: print('abort after commit')
            g.tm.abort()
    else:
        if debug: print('abort')
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
    #request_tearing_down.connect(teardown,app)
    #app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False




