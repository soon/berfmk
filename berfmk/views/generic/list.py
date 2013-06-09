# -*- coding: utf-8 -*-

from django.core.paginator import Paginator, InvalidPage
from django.core.exceptions import ImproperlyConfigured
from django.http import Http404
from django.utils.encoding import smart_str
from django.utils.translation import ugettext as _
from django.views.generic.base import ContextMixin


class MyMultipleObjectMixin(ContextMixin):
    """
    The reason for creating this mixin is common member methods in the
    SingleObjectMixin and the MultipleObjectMixin. Now we can mix them.
    """

    allow_empty = True
    mutliple_queryset = None
    multiple_model = None
    paginate_by = None
    multiple_context_object_name = None
    paginator_class = Paginator

    def get_multiple_queryset(self):
        if self.mutliple_queryset is not None:
            queryset = self.mutliple_queryset
            if hasattr(queryset, '_clone'):
                queryset = queryset._clone()
        elif self.multiple_model is not None:
            queryset = self.multiple_model._default_manager.all()
        else:
            raise ImproperlyConfigured(
                u"'%s' must define 'mutliple_queryset' or 'multiple_model'"
                % self.__class__.__name__
            )
        return queryset

    def paginate_queryset(self, queryset, page_size):
        paginator = self.get_paginator(
            queryset,
            page_size,
            allow_empty_first_page = self.get_allow_empty()
        )
        page = self.kwargs.get('page') or self.request.GET.get('page') or 1
        try:
            page_number = int(page)
        except ValueError:
            if page == 'last':
                page_number = paginator.num_pages
            else:
                raise Http404(
                    _(u"Page is not 'last', nor can it be converted to an int.")
                )
        try:
            page = paginator.page(page_number)
            return (paginator, page, page.object_list, page.has_other_pages())
        except InvalidPage:
            raise Http404(
                _(u'Invalid page (%(page_number)s)') % {
                    'page_number': page_number
                }
            )

    def get_paginate_by(self, queryset):
        return self.paginate_by

    def get_paginator(
        self,
        queryset,
        per_page,
        orphans = 0,
        allow_empty_first_page = True
    ):
        return self.paginator_class(
            queryset,
            per_page,
            orphans = orphans,
            allow_empty_first_page = allow_empty_first_page
        )

    def get_allow_empty(self):
        return self.allow_empty

    def get_multiple_context_object_name(self, object_list):
        if self.multiple_context_object_name:
            return self.multiple_context_object_name
        elif hasattr(object_list, 'model'):
            return smart_str(
                '%s_list' % object_list.model._meta.object_name.lower()
            )
        else:
            # The difference between this and MultipleObjectMixin mixins
            # return None
            return smart_str(
                '%s_list' % self.multiple_model._meta.object_name.lower()
            )

    def get_multiple_context_data(self, **kwargs):
        queryset = kwargs.pop('object_list')
        page_size = self.get_paginate_by(queryset)
        context_object_name = self.get_multiple_context_object_name(queryset)
        if page_size:
            paginator, page, queryset, is_paginated = self.paginate_queryset(
                queryset,
                page_size
            )
            context = {
                'paginator'     : paginator,
                'page_obj'      : page,
                'is_paginated'  : is_paginated,
                'object_list'   : queryset
            }
        else:
            context = {
                'paginator'     : None,
                'page_obj'      : None,
                'is_paginated'  : False,
                'object_list'   : queryset
            }
        context.update(kwargs)
        if context_object_name is not None:
            context[context_object_name] = queryset
        return context
