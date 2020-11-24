from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.shortcuts import render

from .models import NGODocument


# Create your views here.

def ngoabout(request):
    return render(request, 'ngodocs/about.html')


def ngodocs(request):
    return render(request, 'ngodocs/documents.html')


class NGODocumentListView(LoginRequiredMixin, ListView):
    model = NGODocument
    template_name = 'ngodocs/documents.html'
    context_object_name = 'docs'

    def get_queryset(self):
        # reg_docs = NGODocument.objects.filter(tag__in=[7, 8]).distinct()
        # docs = NGODocument.objects.filter(tag__in=[1,2,3,4,5,6]).distinct()
        qs = {'reg_docs': NGODocument.objects.filter(tag__in=[7, 8]).distinct(),
              'rest_docs': NGODocument.objects.filter(tag__in=[1, 2, 3, 4, 5]).distinct()}
        return qs


class MaterialsListView(LoginRequiredMixin, ListView):
    model = NGODocument
    template_name = 'ngodocs/materials.html'
    context_object_name = 'materials'

    def get_queryset(self):
        qs = super().get_queryset()
        # qs = Announcement.objects.filter(author=self.request.user)
        return qs.filter(tag__in=[6, 9]).distinct()


class UserDocsView(LoginRequiredMixin, ListView):
    model = NGODocument
    template_name = 'ngodocs/user_documents.html'
    context_object_name = 'docs'

    def get_queryset(self):
        qs = super().get_queryset()
        # qs = Announcement.objects.filter(author=self.request.user)
        return qs.filter(author=self.request.user)


class NGODocCreateView(LoginRequiredMixin, CreateView):
    model = NGODocument
    fields = ['title', 'document', 'status', 'tag']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class NGODocDetailView(LoginRequiredMixin, DetailView):
    model = NGODocument

    def get_context_data(self, **kwargs):
        context = super(NGODocDetailView, self).get_context_data(**kwargs)
        self.request.session['id'] = self.object.pk
        return context


class NGODocUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = NGODocument
    fields = ['title', 'document', 'status', 'tag']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        doc = self.get_object()
        if self.request.user == doc.author:
            return True
        return False


class NGODocDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = NGODocument
    success_url = '/'

    def test_func(self):
        doc = self.get_object()
        if self.request.user == doc.author:
            return True
        return False
