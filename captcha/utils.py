# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
from recaptcha.client.captcha import displayhtml as original_displayhtml
#-------------------------------------------------------------------------------
def my_displayhtml(*args, **kwargs):
    return u"<script>var RecaptchaOptions = {0};</script>{1}".format(
        unicode(kwargs),
        original_displayhtml(*args)
    )
#-------------------------------------------------------------------------------
