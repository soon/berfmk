# -*- coding: utf-8 -*-

from django.views.generic import ListView, DetailView, FormView, CreateView
from django.http import Http404
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator

from berfmk.views.generic import DetailAndListView, DetailAndListAndCreateView
from forum.forms import ForumForm, PostForm
from forum.models import Forum, Section, SubSection, Topic, Post


class ForumList(ListView):
    """
    Class for showing all forums

    """
    model = Forum

    template_name = 'forum/forum_list.hdt'


class ForumDetail(DetailView):
    """
    Class for showing detailed forum

    """
    model = Forum
    slug_field = 'address'
    slug_url_kwarg = 'forum'

    template_name = 'forum/forum_detail.hdt'


class ForumCreate(CreateView):
    """
    A class provides operations for creating a new forum

    """
    form_class = ForumForm

    template_name = 'forum/forum_create.hdt'

    @method_decorator(permission_required('forum.add_forum'))
    def dispatch(self, request, *args, **kwargs):
        return super(ForumCreate, self).dispatch(request, *args, **kwargs)


class SectionDetail(DetailAndListView):
    """
    Class for showing detailed section

    Also it show a list of topics in the section

    """
    single_model = Section
    single_slug_field = 'address'
    single_slug_url_kwarg = 'section'

    multiple_model = Topic

    template_name = 'forum/section_detail_and_topic_list.hdt'


    def dispatch(self, *args, **kwargs):
        """
        Check for passed forum's address, throws Http404 if failed

        """
        response = super(
            SectionDetail,
            self
        ).dispatch(*args, **kwargs)

        if not self.object.forum.address == kwargs['forum']:
            raise Http404()

        return response

    def get_multiple_queryset(self):
        """
        Returns all topics from the section sorted by the last post in topic

        """
        return sorted(
            self.get_object().topic_set.filter(sub_section = None),
            key = lambda t: t.get_last_post().id,
            reverse = True
        )


# Similar to SectionDetail
# Think about it
class SubSectionDetail(DetailAndListView):
    """
    Class for showing detailed sub_secton

    Also shows a list of topics in the sub_section

    """
    single_model = SubSection
    single_slug_field = 'address'
    single_slug_url_kwarg = 'sub_section'

    multiple_model = Topic

    template_name = 'forum/sub_section_detail_and_topic_list.hdt'


    def dispatch(self, *args, **kwargs):
        """
        Check for passed forum's and section's address, throws Http404 if failed

        """
        response = super(
            SubSectionDetail,
            self
        ).dispatch(*args, **kwargs)

        if (not self.object.section.address == kwargs['section'] or
           not self.object.section.forum.address == kwargs['forum']):
            raise Http404()

        return response

    def get_multiple_queryset(self):
        """
        Returns all topics in the sub_section sorted by the last post in topic

        """
        return sorted(
            self.get_object().topic_set.exclude(sub_section = None),
            key = lambda t: t.get_last_post().id,
            reverse = True
        )


class TopicDetail(DetailAndListAndCreateView):
    """
    Class for showing detailed topic

    Also shows a list of posts in the topic and form for sending new post

    """
    single_model = Topic
    single_slug_field = 'pk'
    single_slug_url_kwarg = 'topic'

    multiple_model = Post
    paginate_by = 10

    form_class = PostForm

    template_name = 'forum/topic.hdt'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.creator = self.request.user
        instance.topic = self.get_object()
        return super(TopicDetail, self).form_valid(instance)

    def get_multiple_queryset(self):
        """
        Returns all posts in the topic

        """
        return self.get_object().post_set.all()

    def get_success_url(self):
        """
        Returns topic's absolute url

        """
        return self.get_object().get_absolute_url()
