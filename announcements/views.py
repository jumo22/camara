from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Announcement, News
from .filters import AnnouncementFilter, EventFilter, NGODocumentFilter
from .forms import SearchForm
from cal.models import Event
from ngodocs.models import NGODocument
import django_filters

# def home(request):
#     announcements = Announcement.objects.all()
#     myFilter = AnnouncementFilter(request.GET, queryset=announcements)
#     announcements = myFilter.qs
#
#     context = {
#         'myFilter': myFilter,
#         'announcements': announcements
#
#     }
#     return render(request, 'announcements/home.html', context)
    # return HttpResponse('<h1>Homie</h1')


def homepage(request):
    if request.user.is_authenticated:
        return redirect('ngo-about')
    else:
        return render(request, 'announcements/homepage.html')


@login_required(login_url='login')
def search(request):
    # form = SearchForm
    if request.method == "GET":
        form = SearchForm(request.GET)
        # a = request.GET
        keyword = form['keyword'].value()
        announcements = Announcement.objects.all()
        events = Event.objects.all()
        ngodocs = NGODocument.objects.all()
        # myFilterGen = GeneralFilter(request.GET, queryset=announcements, typ=1)
        myFilterAnn = AnnouncementFilter({"content": keyword}, queryset=announcements)
        # s_keyword = myFilterAnn.data['content']
        myFilterEvents = EventFilter({"title": keyword}, queryset=events)
        myFilterNGODocs = NGODocumentFilter({"document": keyword}, queryset=ngodocs)
        announcements = myFilterAnn.qs
        events = myFilterEvents.qs
        ngodocs = myFilterNGODocs.qs

        # results = announcements | events | ngodocs
        context = {
            # 'myFilterGen': myFilterGen,
            # 'myFilterAnn': myFilterAnn,
            'form': SearchForm,
            'announcements': announcements.order_by('-date_posted'),
            # 'myFilterEvents': myFilterEvents,
            'events': events.order_by('-start_time'),
            # # 'myFilterNGODocs': myFilterNGODocs,
            'ngodocs': ngodocs.order_by('-date_posted'),
        }
        # context = {
        #     'myFilterAnn': myFilterAnn,
        #     'myFilterEvents': myFilterEvents,
        #     'myFilterNGODocs': myFilterNGODocs,
        #     'results': results,
        # }
        return render(request, 'announcements/search.html', context)


class PostListView(LoginRequiredMixin, ListView):
    model = Announcement
    template_name = 'announcements/home.html'
    context_object_name = 'announcements'
    ordering = ['-date_posted']
    paginate_by = 3


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Announcement


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Announcement
    fields = ['title', 'content', 'image', 'tag']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Announcement
    fields = ['title', 'content', 'image', 'tag']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Announcement
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class UserAnnouncementView(LoginRequiredMixin, ListView):
    model = Announcement
    template_name = 'announcements/home.html'
    context_object_name = 'announcements'
    ordering = ['-date_posted']

    def get_queryset(self):
        qs = super().get_queryset()
        # qs = Announcement.objects.filter(author=self.request.user)
        return qs.filter(author=self.request.user)


class NewsListView(LoginRequiredMixin, ListView):
    model = News
    template_name = 'announcements/news.html'
    context_object_name = 'newslist'
    ordering = ['-date_posted']
    paginate_by = 20


@login_required(login_url='login')
def about(request):
    return render(request, 'announcements/about.html')
