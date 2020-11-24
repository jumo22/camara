import django_filters
from django_filters import CharFilter
from .models import *
from cal.models import *
from ngodocs.models import *

# not useful, kept it as a structure model
# class GeneralFilter(django_filters.FilterSet):
#     title1 = django_filters.CharFilter(method='my_custom_filter')
#     cls = None
#
#     def __init__(self, data, queryset, typ, *args, **kwargs):
#         super(GeneralFilter, self).__init__(data, queryset, *args, **kwargs)
#         self.type = typ
#         cls = self
#
#     class Meta:
#         model = Announcement
#         fields = ['search']
#
#     def my_custom_filter(self, queryset, content, value):
#         if self.type == 1:
#             return queryset.filter(content__icontains=value
#                                    ) | queryset.filter(title__icontains=value
#                                                        ) | queryset.filter(author__username__icontains=value
#                                                                            )
#         return None


class AnnouncementFilter(django_filters.FilterSet):
    content = django_filters.CharFilter(method='my_custom_filter')

    # def __init__(self, value, data, queryset, *args, **kwargs):
    #     super(AnnouncementFilter, self).__init__(data, queryset, *args, **kwargs)
    #     self.value = value

    class Meta:
        model = Announcement
        fields = ['content']

    def my_custom_filter(self, queryset, content, value):
        return queryset.filter(content__icontains=value
                               ).distinct() | queryset.filter(title__icontains=value
                                                   ).distinct() | queryset.filter(author__username__icontains=value
                                                                       ).distinct() | queryset.filter(tag__name__in=[value]).distinct()


class EventFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(method='my_custom_filter')

    class Meta:
        model = Event
        fields = ['title']

    def my_custom_filter(self, queryset, title, value):
        return queryset.filter(title__icontains=value
                               ).distinct() | queryset.filter(description__icontains=value
                                                   ).distinct() | queryset.filter(author__username__icontains=value
                                                                       ).distinct() | queryset.filter(tag__name__in=[value]).distinct()


class NGODocumentFilter(django_filters.FilterSet):
    document = django_filters.CharFilter(method='my_custom_filter')

    class Meta:
        model = NGODocument
        fields = ['document']

    def my_custom_filter(self, queryset, document, value):
        return queryset.filter(title__icontains=value
                               ).distinct() | queryset.filter(author__username__icontains=value
                                                   ).distinct() | queryset.filter(tag__name__in=[value]).distinct()
