# -*- coding: utf-8 -*-

from django.http import Http404

def get_number_from_param_or_404(param):
    try:
        param = int(param)
    except ValueError:
        raise Http404()

    return param;
