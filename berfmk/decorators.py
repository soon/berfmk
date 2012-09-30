# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
from django.contrib.auth.decorators import user_passes_test
#-------------------------------------------------------------------------------
def any_permission_required(function = None, perms = [], login_url = None):
    def wrapper(*args, **kwargs):
        actual_decorator = user_passes_test(
            lambda u: any(u.has_perm(perm) for perm in perms),
            login_url = login_url
        )
        if function:
            return actual_decorator(function)
        return actual_decorator
    return wrapper
#-------------------------------------------------------------------------------
