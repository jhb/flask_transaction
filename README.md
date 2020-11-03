Flask-Transaction
-----------------
*This package is in early development*


This package provides basic transaction support to flask, using zopes
[transaction package](https://transaction.readthedocs.io/en/latest/) . We use a context local transaction manager, and commit
at the end of the request.

Install:

    # pip install flask_transaction

To use:

    >>> from flask import Flask
    >>> app = Flask(__name__) #would be the real flask app
    >>> import flask_transaction
    >>> flask_transaction.init_transaction(app)

The transaction is automatically commited, unless there is an exception, or the transaction is
doomed.
