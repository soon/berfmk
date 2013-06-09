# -*- coding: utf-8 -*-

from django.views.generic import View
from django.views.generic.base import TemplateResponseMixin
from django.http import Http404
from django.core.exceptions import ImproperlyConfigured

from berfmk.views.generic.detail import MySingleObjectMixin
from berfmk.views.generic.list import MyMultipleObjectMixin


class SingleAndMultipleObjectMixin(MyMultipleObjectMixin, MySingleObjectMixin):
    """
    A mixin provides a way to show and handle a DetailAndList in a request

    """
    def get_context_data(self, **kwargs):
        """
        Check for allow_empty and empty list, throw an Http404 if failed

        Returns context with multiple and single context data

        """
        context = kwargs
        if 'view' not in context:
            context['view'] = self

        self.object_list = self.get_multiple_queryset()
        allow_empty  = self.get_allow_empty()
        if not allow_empty and len(self.object_list) == 0:
            raise Http404(
                _(u"Empty list and '%(class_name)s.allow_empty' is False.") % {
                    'class_name': self.__class__.__name__
                }
            )
        context.update(
            self.get_multiple_context_data(object_list = self.object_list)
        )

        self.object = self.get_object()
        context.update(self.get_single_context_data(object = self.object))

        return context


class BaseDetailAndListView(SingleAndMultipleObjectMixin, View):
    """
    A base class for displaying list of objects and detailed object both

    """
    def get(self, request, *args, **kwargs):
        """
        Returns rendered template without side effects

        """
        return self.render_to_response(self.get_context_data())


class SingleAndMultipleObjectTemplateResponseMixin(TemplateResponseMixin):
    """
    A mixin that can be used for render a sungle-multiple template

    """
    template_name_field = None
    template_name_suffix = '_detail_and_list'

    def get_template_names(self):
        """
        Returns all template names

        """
        try:
            names = super(
                SingleAndMultipleObjectTemplateResponseMixin,
                self
            ).get_template_names()
        except ImproperlyConfigured:
            names = []

        if hasattr(self.object_list, 'model'):
            opts = self.object_list.model._meta
            names.append(
                "%s/%s%s.html" % (
                    opts.app_label,
                    opts.object_name.lower(),
                    self.template_name_suffix
                )
            )

        if self.object and self.template_name_field:
            name = getattr(self.object, self.template_name_field, None)
            if name:
                names.insert(0, name)

        if hasattr(self.object, '_meta'):
            names.append("%s/%s%s.html" % (
                self.object._meta.app_label,
                self.object._meta.object_name.lower(),
                self.template_name_suffix
            ))
        elif hasattr(self, 'model') and hasattr(self.single_model, '_meta'):
            names.append("%s/%s%s.html" % (
                self.single_model._meta.app_label,
                self.single_model._meta.object_name.lower(),
                self.template_name_suffix
            ))
        return names


class DetailAndListView(
    SingleAndMultipleObjectTemplateResponseMixin,
    BaseDetailAndListView
):
    """
    Render single object and list of objects both

    """
