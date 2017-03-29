from functools import wraps
from air import session
from sqlalchemy.exc import SQLAlchemyError, DBAPIError

def attempt_db_modification(f):
    """
    Simple wrapper to handle any errors which
    occur when you're modifying the db.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            f(*args, **kwargs)
        except (SQLAlchemyError, DBAPIError) as e:
            print(e)
            session.rollback()
            # add logging stuff here
    return wrapper
