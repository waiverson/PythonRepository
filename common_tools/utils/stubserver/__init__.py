
"""A stub webserver used to enable blackbox testing of applications that call
external web urls. For example, an application that consumes data from an
external REST api. The usage pattern is intended to be very much like using
a mock framework."""
from webserver import StubServer
from ftpserver import FTPStubServer