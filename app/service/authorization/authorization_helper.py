import logging
from enum import Enum
from functools import wraps

from flask_jwt_extended import get_current_user, verify_jwt_in_request
from flask_jwt_extended.exceptions import NoAuthorizationError

from app.model.user import User


# @check_access decorator function
def check_access(roles: [Enum] = []):
    def decorator(f):
        @wraps(f)
        def decorator_function(*args, **kwargs):
            # calling @jwt_required()
            verify_jwt_in_request()
            # fetching current user from db
            current_user: User = get_current_user()
            logging.debug(current_user.roles)
            # checking if there is a common role in users roles and necessary roles for function execution
            a_set = set(roles)
            b_set = set(current_user.roles)
            if not a_set & b_set:
                raise NoAuthorizationError(f"Role missing one of following roles needed {roles}")
            return f(*args, **kwargs)

        return decorator_function

    return decorator
