Flask-Transaction
-----------------
*This package is in early development*


This package provides basic transaction support to flask, using zopes
transaction package. We use a context local transaction manager, and commit
at the end of the request.

Install:

    # pip install flask_transaction

To use:

    >>> app = object() #would be the real flask app
    >>> import flask_transaction
    >>> flask_transaction.init_app(app)