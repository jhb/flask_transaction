import pytest
from flask import Flask, current_app, g, request
from flask_transaction import init_transaction
from flask_transaction.filedm import FileDM
import os

import tempfile

app = Flask(__name__)
app.config['TESTING'] = True
init_transaction(app)


@app.route('/action')
def action():
    text1 = request.values['text1']
    text2 = request.values['text2']
    fail = request.values.get('fail',None) is not None
    basedir = tempfile.TemporaryDirectory()
    basename = os.path.normpath(basedir.name)
    print(basename)
    g.basedir = basedir
    file1 = FileDM(text1,os.path.join(basename,'foo1.txt'),current_app.tm)
    file2 = FileDM(text2, os.path.join(basename, 'bar1.txt'), current_app.tm, fail=fail)
    return 'fini'



def test_good_transaction():
    basedir = None
    with app.test_client() as client:
        client.get('/action?text1=foo&text2=foo')
        basedir = g.basedir
    contents = os.listdir(os.path.normpath(basedir.name))
    assert sorted(contents) == ['bar1.txt', 'foo1.txt']

def test_bad_transaction():
    basedir = None
    with app.test_client() as client:
        client.get('/action?text1=foo&text2=foo&fail=1')
        basedir = g.basedir
    contents = os.listdir(os.path.normpath(basedir.name))
    assert sorted(contents) == []
