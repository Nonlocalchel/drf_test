from django.db.models import Q
from django_filters import rest_framework as filters

from tasks.models import Task


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class TaskFilter(filters.FilterSet):
    """Filter for Books by if books are published or not"""
    worker = CharFilterInFilter(field_name='worker', method='find_results_maybe_include_null')

    @staticmethod
    def find_results_maybe_include_null(queryset, name, value):
        filter_params = Q()

        for worker_filter_param in value:
            if worker_filter_param == 'null':
                append_param = Q(**{f'{name}__isnull': True})
            else:
                append_param = Q(**{name: worker_filter_param})

            filter_params = filter_params | append_param

        return queryset.filter(filter_params)

    class Meta:
        model = Task
        fields = ['worker', 'customer', 'status', 'title']
