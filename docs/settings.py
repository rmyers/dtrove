"""
Fake settings module for the documentation.

Some of the documents refer to settings which could leak out real passwords
in the documentation. This file acts as the documentations settings so as to
prevent that.
"""

# SECRET_KEY is the only required setting
SECRET_KEY = 'do_not_tell_anyone'
