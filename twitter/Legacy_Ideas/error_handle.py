#!/usr/bin/python

'''
Date June 10, 2012
Author: www.stackoverflow.com
GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007

Disclaimer:
All software provided as is. All software covered under the GPL license and free for public redistribution.
If unintended consequences occur due to utilization of this software, user bears the resultant outcome.
The rule of thumb is to test and validate properly all solutions prior to implementation within a production environment.
All solutions should be subject to public scrutiny, and peer review.
'''

# Decorator class for Error handling within scripts so that useful
# error messages are generated when problem sets arise
# Code sample culled from www.stackoverflow.com

class ConvertExceptions(object):
    func = None
    def __init__(self, exceptions, replacement=None):
        self.exceptions = exceptions
        self.replacement = replacement
    def __call__(self, *args, **kwargs):
        if self.func is None:
            self.func = args[0]
            return self
        try:
            return self.func(*args, **kwargs)
        except self.exceptions:
            return self.replacement
