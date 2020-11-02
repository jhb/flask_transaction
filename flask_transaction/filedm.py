"""
A simple transactional file writer.

An adaption of the MockDataManager in https://repozetm2.readthedocs.io/en/latest/

Lets do some imports first
    >>> import transaction
    >>> import tempfile
    >>> import os

We want to create some files in a temporary directory
    >>> basedir = tempfile.TemporaryDirectory()
    >>> basename = basedir.name

We need a transaction manager. We use an non-threading tm here, because flask
works on contexts (which can be threads or processes, but don't have to), so
the normal ThreadingTransactionManager is not suitable

    >>> tm = transaction.TransactionManager()

Lets create two files that are to be written to the tempdir
    >>> file1 = FileDM('foo',os.path.join(basename,'foo1.txt'),tm)
    >>> file2 = FileDM('bar',os.path.join(basename,'bar1.txt'),tm)

Nothing is written without a commit
    >>> len(os.listdir(os.path.normpath(basename)))
    0

Lets commit, two files should be created
    >>> tm.commit()
    >>> sorted(os.listdir(os.path.normpath(basename)))
    ['bar1.txt', 'foo1.txt']

Now, lets try with two new files, but we trigger the second file (only) to fail
    >>> file3 = FileDM('foo',os.path.join(basename,'foo2.txt'),tm)
    >>> file4 = FileDM('please_fail',os.path.join(basename,'bar2.txt'),tm,fail=True)
    >>> tm.commit()
    Traceback (most recent call last):
       ...
    ValueError: we were supposed to fail

Neiter file3 or file4 were created
    >>> sorted(os.listdir(os.path.normpath(basename)))
    ['bar1.txt', 'foo1.txt']

"""

import tempfile
import os


class FileDM:


    transaction_manager = None

    def __init__(self, data, path, tm, fail=False):
        self.data = data
        self.path = path
        self.tm = tm
        self.fail = fail
        self.join()

    def join(self):
        tx = self.tm.get()
        tx.join(self)

    def abort(self, transaction):
        pass

    def tpc_begin(self, transaction):
        pass

    def commit(self, transaction):
        fd, self.tempfn = tempfile.mkstemp()
        with open(self.tempfn, 'w') as temp:
            temp.write(self.data)
            temp.flush()
        os.close(fd)

    def tpc_vote(self, transaction):
        if not os.path.exists(self.tempfn):
            raise ValueError('%s doesnt exist' % self.tempfn)
        if os.path.exists(self.path):
            raise ValueError('file already exists')
        if self.fail:
            raise ValueError('we were supposed to fail')

    def tpc_finish(self, transaction):
        os.rename(self.tempfn, self.path)

    def tpc_abort(self, transaction):
        try:
            os.remove(self.tempfn)
        except OSError:
            pass

    def sortKey(self):
        return f'MockDataManager: {id(self)}'