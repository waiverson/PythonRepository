__author__ = 'xyc'

import functools


"""
a decorator is a function that takes a function as its sole argument
and returns a new function with the same name as the original function but
with enhanced functionality. Decorators are often used by frameworks (e.g.,
web frameworks) to make it easy to integrate our own functions within the
framework.
"""

def float_args_and_return(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        args = [float(arg) for arg in args]
        return float(function(*args, **kwargs))
    return wrapper

@float_args_and_return
def mean(first, second, *rest):
    numbers = (first, second) + rest
    return sum(numbers) / len(numbers)


# this wrapper can checks the number and types of all the positional arguments
def statically_typed(*types, return_type=None):
    def decorator(function):
        @functools.wraps(function)
            def wrapper(*args, **kwargs):
                if len(args) > len(types):
                    raise ValueError("too many arguments")
                elif len(args) < len(types):
                    raise ValueError("too few arguments")
                for i, (arg, type_) in enumerate(zip(args, types)):
                    if not isinstance(arg, type_):
                        raise ValueError("argument {} must be of type {}"
                                                .format(i, type_.__name__))
                result = function(*args, **kwargs)
                if (return_type is not None and
                    not isinstance(result, return_type)):
                        raise ValueError("return value must be of type {}".format(return_type.__name__))
            return result
        return wrapper
    return decorator


@statically_typed(str, str, return_type=str)
def make_tagged(text, tag):
    return "<{0}>{1}</{0}>".format(tag, escape(text))


# web application sample:

def ensure_logged_in(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        username = bottle.request.get_cookie(COOKIE,secret=secret(bottle.request))
        if username is not None:
            kwargs["username"] = username
        return function(*args, **kwargs)
        bottle.redirect("/login")
    return wrapper

@application.post("/mailinglists/add")
@Web.ensure_logged_in
def person_add_submit(username):
    name = bottle.request.forms.get("name")
    try:
        id = Data.MailingLists.add(name)
        bottle.redirect("/mailinglists/view")
    except Data.Sql.Error as err:
        return bottle.mako_template("error", url="/mailinglists/add", text="Add Mailinglist", message=str(err))