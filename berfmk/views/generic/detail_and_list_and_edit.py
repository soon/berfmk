# -*- coding: utf-8 -*-

from django.views.generic.edit import ModelFormMixin, ProcessFormView

from berfmk.views.generic.detail_and_list import (SingleAndMultipleObjectMixin,
                                SingleAndMultipleObjectTemplateResponseMixin)


class SingleAndMultipleAndCreateObjectMixin(
    SingleAndMultipleObjectMixin,
    ModelFormMixin
):
    """
    A mixin that provides a way to show and handle
    a single, multiple ans create form objects in a request.

    """
    object = None # This is a bad, I guess. Try to resolve it later

    def get_context_data(self, **kwargs):
        """
        Returns context data with form

        """
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if not 'form' in kwargs:
            kwargs['form'] = form
        context = super(
            SingleAndMultipleAndCreateObjectMixin, self
        ).get_context_data(**kwargs)
        return context


class BaseDetailAndListAndCreateView(
    SingleAndMultipleAndCreateObjectMixin,
    ProcessFormView
):
    """
    A base class for displaying
    list of objects, detailed object and creating form together

    """
    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data())


class DetailAndListAndCreateView(
    SingleAndMultipleObjectTemplateResponseMixin,
    BaseDetailAndListAndCreateView
):
    """
    A class for displaying detailed object, list of objects and create form,
    and rendering a template response

    """
