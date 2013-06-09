# -*- coding: utf-8 -*-

from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.http import Http404
from django.utils.encoding import smart_str
from django.utils.translation import ugettext as _
from django.views.generic.base import TemplateResponseMixin, View, ContextMixin


class MySingleObjectMixin(ContextMixin):
    """
    The reason for creating this mixin is common member methods in the
    SingleObjectMixin and the MultipleObjectMixin. Now we can mix them.
    """

    single_model = None
    single_queryset = None
    single_slug_field = 'slug'
    single_context_object_name = None
    single_slug_url_kwarg = 'slug'
    single_pk_url_kwarg = 'pk'

    def get_object(self, queryset = None):
        if queryset is None:
            queryset = self.get_single_queryset()

        pk = self.kwargs.get(self.single_pk_url_kwarg, None)
        slug = self.kwargs.get(self.single_slug_url_kwarg, None)

        if pk is not None:
            queryset = queryset.filter(pk = pk)

        elif slug is not None:
            slug_field = self.get_single_slug_field()
            queryset = queryset.filter(**{slug_field: slug})

        else:
            raise AttributeError(
                u"Generic detail view %s must be called with either an object "
                u"pk or a slug." % self.__class__.__name__
            )

        try:
            obj = queryset.get()
        except ObjectDoesNotExist:
            raise Http404(
                _(u"No %(verbose_name)s found matching the query") % {
                    'verbose_name': queryset.model._meta.verbose_name
                }
            )
        return obj

    def get_single_queryset(self):
        if self.single_queryset is None:
            if self.single_model:
                return self.single_model._default_manager.all()
            else:
                raise ImproperlyConfigured(
                    u"%(cls)s is missing a single_queryset. Define "
                    u"%(cls)s.single_model, "
                    u"%(cls)s.single_queryset, or override "
                    u"%(cls)s.get_single_object()." % {
                        'cls': self.__class__.__name__
                    }
                )
        return self.single_queryset._clone()

    def get_single_slug_field(self):
        return self.single_slug_field

    def get_single_context_object_name(self, obj):
        if self.single_context_object_name:
            return self.single_context_object_name
        elif hasattr(obj, '_meta'):
            return smart_str(obj._meta.object_name.lower())
        else:
            return None

    def get_single_context_data(self, **kwargs):
        context = kwargs
        context_object_name = self.get_single_context_object_name(self.object)
        if context_object_name:
            context[context_object_name] = self.object
        return context
