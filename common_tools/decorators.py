#!/usr/bin/env python
# encoding: UTF-8

import sys
import time
from functools import wraps

def trans(op):
    def deco(f):
        @wraps(f)
        def _(*a, **kw):
            r = f(*a, **kw)
            if r is not None:
                return op(r)
        return _
    return deco

def ptrans(op):
    def deco(f):
        @wraps(f)
        def _(*a, **kw):
            return [op(r) for r in f(*a, **kw)]
        return _
    return deco

def retry(func):
    def _(*args, **kwargs):
        tries = 3 
        while tries:
            try:
                return func(*args, **kwargs)
            except Exception, e:
                print >>sys.stderr, 'error while %s' %func.func_name, tries, e, args, kwargs
                tries -= 1
                if tries == 0:
                    raise
                time.sleep(0.1)
    return _ 

# A decorator without arguments
def decorator(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        results = f(*args, **kwargs)
        # do something
        return results
    return wrapped


# A Decorator with arguments
def decorator_args(a, b, c):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            results = f(*args, **kwargs)
            # do something
            return results
        return wrapped
    return decorator

#The email decorator
def email(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        envelope = f(*args, **kwargs)
        envelope.from_addr = api.config['SYSTEM_EMAIL']
        def task():
            smtp().send(envelope)
        gevent.spawn(task)
        return jsonify({"status": "OK"})
    return wrapped

# building the limit decorator
def limit(requests=100, window=60, by="ip", group=None):
    if not callable(by):
        by = { 'ip': lambda: request.headers.remote_addr }[by]

    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            group = group or request.endpoint
            key = ":".join(["rl", group, by()])

            try:
                remaining = requests - int(redis.get(key))
            except (ValueError, TypeError):
                remaining = requests
                redis.set(key, 0)

            ttl = redis.ttl(key)
            if not ttl:
                redis.expire(key, window)
                ttl = window

            g.view_limits = (requests,remaining-1,time()+ttl)

            if remaining > 0:
                redis.incr(key, 1)
                return f(*args, **kwargs)
            else:
                return Response("Too Many Requests", 429)
        return wrapped
    return decorator